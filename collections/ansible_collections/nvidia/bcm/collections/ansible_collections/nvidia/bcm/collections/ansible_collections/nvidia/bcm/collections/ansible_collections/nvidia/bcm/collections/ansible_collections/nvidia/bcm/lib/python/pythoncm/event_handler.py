#
# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
#

from __future__ import annotations

import logging
import typing
from uuid import UUID

if typing.TYPE_CHECKING:
    from graceful_interrupt_handler import GracefulInterruptHandler


class EventHandler:
    """
    Handles all events received from cmdaemon.
    """

    def __init__(
        self,
        cluster=None,
        signal_handler: GracefulInterruptHandler | None = None,
        signal_on_event: list[str] | None = None,
    ):
        self.cluster = cluster
        self.logger = logging.getLogger(__name__)
        self.certificate_issue_callback = None
        self.signal_handler = signal_handler
        self.signal_on_event = signal_on_event

    def handle(self, events):
        signal_event = False
        stop_handling_events = False
        for event in events:
            event_type = event.get("childType", "Undefined")
            signal_event |= self.signal_on_event is None or event_type in self.signal_on_event
            handler = f'_{event_type}_handler'
            handler = getattr(self, handler, None)
            if handler is None:
                self.logger.info(f"Not implemented: {event_type} handler")
                needs_stop = self._UnknownEvent_handler(event)
            else:
                needs_stop = handler(event)
            stop_handling_events |= (needs_stop is not None) and needs_stop
        if bool(self.signal_handler) and (stop_handling_events or signal_event):
            self.signal_handler.wakeup()
        return stop_handling_events

    def _NullEvent_handler(self, event):
        return False

    def _KeepAliveEvent_handler(self, event):
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmsession',
            call='acknowledgeKeepAlive',
            args=[self.cluster.session_uuid, 0],
        )
        return code or not out

    def _EndOfSessionEvent_handler(self, event):
        self.cluster._end_of_session(event.get('reason', ''))
        return True

    def _WarningEvent_handler(self, event):
        self.cluster._add_warning(
            event.get('uuid', self.cluster.zero_uuid),
            event.get('msg', ''),
            event.get('extendedMsg', ''),
        )

    def _UnknownEvent_handler(self, event):
        self.logger.info("Unknown event not handled: %s", event.get('childType', 'Undefined'))

    def _UndefinedEvent_handler(self, event):
        self.logger.info("Undefined event not handled")

    def _InitrdStartEvent_handler(self, event):
        self.logger.info(event.get('message', 'Initrd start, no message'))

    def _InitrdUpdateEvent_handler(self, event):
        self.logger.info(event.get('message', 'Initrd update, no message'))

    def _CMDaemonBackgroundTaskEvent_handler(self, event):
        self.cluster.background_task_manager.process(
            event.get('source_device', self.cluster.zero_uuid),
            [UUID(it) for it in event.get('updatedTasks', [])],
            [UUID(it) for it in event.get('removedTasks', [])],
        )

    def _DeviceStatusChangedEvent_handler(self, event):
        for status in event.get('status', []):
            self.cluster.device_status_waiter_manager.process(status)

    def _ProvisioningEvent_handler(self, event):
        self.cluster.provisioning.update()

    def _PowerStatusChangedEvent_handler(self, event):
        self.cluster.power_operation_manager.update(event.get('status', []))

    def _ParExecEvent_handler(self, event):
        self.cluster.remote_execution_manager.update(
            pid=event.get('pid', 0),
            tracker=event.get('tracker', UUID(int=0)),
            node=event.get('source_device', self.cluster.zero_uuid),
            output=event.get('output', ''),
            error=event.get('error', ''),
        )

    def _ServiceDiedEvent_handler(self, event):
        self.logger.info(
            'The service %s died on %s',
            event.get('service', 'unknown'),
            self.cluster.resolve_name_by_uuid(
                uuid=event.get('source_device', self.cluster.zero_uuid), type_name='node'
            ),
        )

    def _ServiceEvent_handler(self, event):
        hostname = self.cluster.resolve_name_by_uuid(
            uuid=event.get('source_device', self.cluster.zero_uuid),
            type_name='node',
        )
        message = f'The service {event.get("service", "unknown")} on {hostname} was'
        if event.get('result', False):
            message += ' not'
        message += ' ' + event.get('operation', 'undefined operation')
        info = event.get('info', '')
        self.logger.info(message)
        if len(info):
            self.logger.info(info)

    def _UpdateProcessedEvent_handler(self, event):
        self.cluster.service_update_manager.process(
            node=event.get('source_device', self.cluster.zero_uuid),
            name=event.get('service', ''),
        )

    # All changed events below this point
    # Add other events above this comment

    def _EntitiesChangedEvent_handler(self, event):
        self.cluster._process_update_removed(
            event.get('entityTypeName', ''),
            [UUID(it) for it in event.get('updateUuids', [])],
            [UUID(it) for it in event.get('removeUuids', [])],
        )

    def _SysInfoChangedEvent_handler(self, event):
        # TODO: not implemented on server side
        pass

    def _NewCertificateEvent_handler(self, event):
        if self.certificate_issue_callback is not None:
            self.certificate_issue_callback(event.get('certificate', None))
            self.certificate_issue_callback = None

    def _CertificateDeniedEvent_handler(self, event):
        if self.certificate_issue_callback is not None:
            self.certificate_issue_callback(None)
            self.certificate_issue_callback = None

    def _ModifiedConfigFileEvent_handler(self, event):
        self.logger.info(
            "Configuration file '%s' was overwritten, a backup was saved in '%s'",
            event.get('filename', ''),
            event.get('backupfilename', ''),
        )

    def _NewCertificateRequestEvent_handler(self, event):
        # TODO: create a manager?
        pass
