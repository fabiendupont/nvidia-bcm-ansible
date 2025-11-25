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

import atexit
import contextlib
import json
import logging
import os
import threading
import time
import typing
from uuid import UUID
from uuid import uuid4

from pythoncm.background_task_manager import BackgroundTaskManager
from pythoncm.component_certificate import ComponentCertificate
from pythoncm.device_status_waiter_manager import DeviceStatusWaiterManager
from pythoncm.entity import BootRole
from pythoncm.entity import ClusterSetup
from pythoncm.entity import CMDaemonStatus
from pythoncm.entity import FileWriteInfo
from pythoncm.entity import GuiClusterOverview
from pythoncm.entity import LicenseInfo
from pythoncm.entity import VersionInfo
from pythoncm.entity.certificate import Certificate
from pythoncm.entity.certificaterequest import CertificateRequest
from pythoncm.entity.entity import Entity
from pythoncm.entity.fspart import FSPart
from pythoncm.entity.network import Network
from pythoncm.entity.newnode import NewNode
from pythoncm.entity.node import Node
from pythoncm.entity.remotenodeinstallerinteraction import RemoteNodeInstallerInteraction
from pythoncm.entity_change import EntityChange
from pythoncm.entity_converter import EntityConverter
from pythoncm.event_handler import EventHandler
from pythoncm.ha import HA
from pythoncm.meta_data_cache import MetaDataCache
from pythoncm.monitoring.monitoring import Monitoring
from pythoncm.multi_commit_result import MultiCommitResult
from pythoncm.multi_remove_result import MultiRemoveResult
from pythoncm.node_filter import NodeFilter
from pythoncm.parallel import Parallel
from pythoncm.power_operation_manager import PowerOperationManager
from pythoncm.provisioning import Provisioning
from pythoncm.remote_execution_manager import RemoteExecutionManager
from pythoncm.rpc.rpc import RPC
from pythoncm.rpc.service import Service
from pythoncm.service_update_manager import ServiceUpdateManager
from pythoncm.settings import Settings
from pythoncm.target_source_mapping import TargetSourceMapping
from pythoncm.workload import Workload

try:
    from pythoncm.entity.metadata.api import API
except ImportError:
    API = None

if typing.TYPE_CHECKING:
    from collections.abc import Iterable

    from graceful_interrupt_handler import GracefulInterruptHandler

    from pythoncm.entity import Device
    from pythoncm.entity import Rack

EntityT = typing.TypeVar('EntityT', bound=Entity)  # Special type used for linking of argument type and return type


class Cluster:
    """
    The pythoncm connection to the active head node cmdaemon
    """

    CLIENT_TYPE_PYTHON = 6
    WAIT_FOR_EVENT_TIMEOUT = 10

    REDIRECT_NONE = 0
    REDIRECT_ACTIVE_HEAD = 1
    REDIRECT_SHARED_IP = 2
    REDIRECT_ACTIVE_HEAD_IN_HA = 3

    EVENT_SEVERITY_DEBUG = -2000
    EVENT_SEVERITY_INFO = -1000
    EVENT_SEVERITY_NOTICE = 0
    EVENT_SEVERITY_WARNING = 1000
    EVENT_SEVERITY_ERROR = 2000
    EVENT_SEVERITY_ALERT = 3000

    zero_uuid = UUID(int=0)
    zero_uuid_str = str(UUID(int=0))

    def __init__(
        self,
        settings=None,
        auto_connect: bool = True,
        follow_redirect=REDIRECT_ACTIVE_HEAD_IN_HA,
        check_api: bool = True,
        allow_no_wait_commit: bool = False,
        event_handler: EventHandler | None = None,
        signal_handler: GracefulInterruptHandler | None = None,
        signal_on_event: list[str] | None = None,
        auto_reconnect: bool | int = False,
    ):
        if settings is None:
            home = os.path.expanduser('~')
            cert_paths = [f'{home}/{path}' for path in ('.cm', '.cm/cmsh')]
            cert_path = None
            for path in cert_paths:
                if os.path.exists(f'{path}/admin.pem') and os.path.exists(f'{path}/admin.key'):
                    cert_path = path
                    break
            assert cert_path
            self.settings = Settings(
                cert_file=f'{cert_path}/admin.pem',
                key_file=f'{cert_path}/admin.key',
                ca_file='/cm/local/apps/cmd/etc/cacert.pem',
            )
        else:
            self.settings = settings

        self.logger = logging.getLogger(__name__)

        self._all_services = [
            Service('cmauth', 'CMService', 'CMServices'),
            Service('cmauth', 'Profile', 'Profiles'),
            Service('cmcloud', 'CloudProvider', 'CloudProviders', by_uuids=True),
            Service('cmcloud', 'CloudRegion', 'CloudRegions', by_uuids=True),
            Service('cmcloud', 'CloudType', 'CloudTypes', by_uuids=True),
            Service('cmcloud', 'OCIInstancePool', 'OCIInstancePools', by_uuids=True),
            Service('cmcloud', 'OCIGPUMemoryCluster', 'OCIGPUMemoryClusters', by_uuids=True),
            Service('cmdevice', 'Category', 'Categories', by_uuids=True, multi=True),
            Service('cmdevice', 'ConfigurationOverlay', 'ConfigurationOverlays', by_uuids=True),
            Service('cmdevice', 'Device', 'Devices', by_uuids=True, multi=True),
            Service('cmdevice', 'NodeGroup', 'NodeGroups', by_uuids=True, multi=True),
            Service('cmdevice', 'NodeHierarchyRule', 'NodeHierarchyRules', by_uuids=True),
            Service('cmdevice', 'ReportQuery', 'ReportQueries', by_uuids=True, multi=True),
            Service('cmetcd', 'EtcdCluster', 'EtcdClusters'),
            Service('cmjob', 'JobQueue', 'JobQueues', owner=True, by_uuids=True, get_one_extra_args=[UUID(int=0)]),
            Service('cmjob', 'WlmCluster', 'WlmClusters', by_uuids=True),
            Service('cmjob', 'ChargeBackRequest', 'ChargeBackRequests', by_uuids=True),
            Service('cmkube', 'KubeCluster', 'KubeClusters', by_uuids=True),
            Service('cmmon', 'LabeledEntity', 'LabeledEntities', by_uuids=True),
            Service('cmmon', 'MonitoringAction', 'MonitoringActions', by_uuids=True),
            Service('cmmon', 'MonitoringConsolidator', 'MonitoringConsolidators', by_uuids=True),
            Service('cmmon', 'MonitoringDataProducer', 'MonitoringDataProducers', by_uuids=True),
            Service('cmmon', 'MonitoringMeasurable', 'MonitoringMeasurables', by_uuids=True),
            Service('cmmon', 'MonitoringTrigger', 'MonitoringTriggers', by_uuids=True),
            Service('cmmon', 'PrometheusQuery', 'PrometheusQueries', by_uuids=True),
            Service('cmmon', 'StandaloneMonitoredEntity', 'StandaloneMonitoredEntities', by_uuids=True, multi=True),
            Service('cmnet', 'Network', 'Networks', by_uuids=True, multi=True),
            Service('cmpart', 'Partition', 'Partitions'),
            Service('cmpart', 'Rack', 'Racks', by_uuids=True),
            Service('cmpart', 'EdgeSite', 'EdgeSites', by_uuids=True, multi=True),
            Service('cmpart', 'SoftwareImage', 'SoftwareImages', by_uuids=True, multi=True),
            Service('cmpart', 'SoftwareImageFileSelection', 'SoftwareImageFileSelections'),
            Service('cmpart', 'PowerCircuit', 'PowerCircuits', by_uuids=True),
            Service('cmprov', 'FSPart', 'FSParts', by_uuids=True),
            Service('cmuser', 'Group', 'Groups', by_uuids=True),
            Service('cmuser', 'User', 'Users', by_uuids=True),
            Service('cmbeegfs', 'BeeGFSCluster', 'BeeGFSClusters', by_uuids=True),
        ]
        self.entities = None
        self._entities_condition = threading.Condition()
        if allow_no_wait_commit:
            self._recently_committed_entities = {}
        else:
            self._recently_committed_entities = None
        self._recently_converted_entities = {}
        self.fetch_errors = None
        self.connected = False
        self.session_uuid = self.zero_uuid
        self.warnings = None
        self.cmdaemon_stopped = False
        self.auto_reconnect = auto_reconnect
        self._event_thread = None
        if bool(event_handler):
            event_handler.cluster = self
            self._event_handler = event_handler
        else:
            self._event_handler = EventHandler(self, signal_handler, signal_on_event)
        self._active_passive_uuids = None
        self._status_waiters = []
        self.monitoring = Monitoring(self)
        self.background_task_manager = BackgroundTaskManager(self)
        self.device_status_waiter_manager = DeviceStatusWaiterManager(self)
        self.power_operation_manager = PowerOperationManager(self)
        self.remote_execution_manager = RemoteExecutionManager(self)
        self.meta_data_cache = MetaDataCache(self)
        self.provisioning = Provisioning(self)
        self.parallel = Parallel(self)
        self.workload = Workload(self)
        self.component_certificate = ComponentCertificate(self)
        self.entity_change = EntityChange()
        self.service_update_manager = ServiceUpdateManager()
        self.ha = HA(self)
        self.certificate = None
        self.profile = None
        self.edition_disabled_features = None
        if bool(self.settings) and self.settings.check_certificate_files():
            self.certificate = Certificate()
            self.certificate.cluster = self
            self.certificate.load(self.settings.cert_file)
        if auto_connect:
            self.connect(
                follow_redirect=follow_redirect,
                check_api=check_api,
            )
        atexit.register(self.disconnect)

    def check_api(self):
        """
        Check if the cmdaemon is running the same API.
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmmain',
            call='verifyAPI',
            args=['pythoncm', API.hash],
        )
        if code:
            raise OSError(out)
        return out

    def follow_redirect(self, follow_redirect):
        """
        Connect to the shared IP in case of a HA setup.
        """
        if follow_redirect == self.REDIRECT_NONE:
            self.logger.info("No redirection, using: {self.settings.host}")
            return True
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service="cmmain",
            call="getHeadNodeIPs",
        )
        if code:
            raise OSError(out)
        active_ip = out.get("active_head_node_ip", None)
        passive_ip = out.get("passive_head_node_ip", None)
        shared_ip = out.get("shared_head_node_ip", None)
        if follow_redirect == self.REDIRECT_ACTIVE_HEAD and bool(active_ip):
            if self.settings.update_host(active_ip):
                self.logger.info(f"Follow redirection to active head IP: {active_ip}")
                return True
        elif follow_redirect == self.REDIRECT_ACTIVE_HEAD_IN_HA:
            if bool(active_ip) and bool(passive_ip):
                if self.settings.update_host(active_ip):
                    self.logger.info(f"Follow redirection to active head (HA) IP: {active_ip}")
            return True
        elif follow_redirect == self.REDIRECT_SHARED_IP and bool(shared_ip):
            if self.settings.update_host(shared_ip):
                self.logger.info(f"Follow redirection to shared IP: {shared_ip}")
                return True
        else:
            self.logger.info(f"No redirection required, using: {self.settings.host}")
        return False

    def connect(
        self,
        follow_redirect=REDIRECT_ACTIVE_HEAD_IN_HA,
        check_api: bool = True,
        force_reconnect: bool = False,
        reconnecting: bool = False,
    ):
        """
        Connect to the cluster and load all entities.
        """
        if self.connected and not force_reconnect:
            self.logger.info('Already connected to cluster')
            return True
        if check_api:
            if not self.check_api():
                raise ValueError('Invalid API hash')
            self.logger.debug('Cluster API compatibile')
        else:
            self.logger.warning('API compatibility not checked')
        if not self.follow_redirect(follow_redirect):
            return False
        self._refresh_all()
        self._register_session()
        self.cmdaemon_stopped = False
        self.connected = True
        if not reconnecting:
            self._start_event_thread()
        self._status_waiters = []
        self.monitoring.connect()
        if self.certificate is not None:
            self.profile = self.get_by_name(self.certificate.profile, 'Profile')
            if self.profile is None:
                self.logger.warning('Unable to find profile: %s', self.certificate.profile)
        return True

    def _refresh_all(self, types: list[str] | None = None):
        entities, self.fetch_errors = self._fetch(types)
        if len(entities) == 0:
            names = {str(it) for it in self.fetch_errors}
            raise OSError(f"Unable to connect: {', '.join(names)}")
        with self._entities_condition:
            self.entities = {it.uuid: it for it in entities}
            for entity in entities:
                entity._set_is_committed()
                entity._resolve_uuids()

    def disconnect(self, throw=False):
        """
        Disconnect from the cluster.
        """
        if self.connected:
            exception: BaseException | None = None
            for waiter in self._status_waiters:
                waiter.stop()
            self._status_waiters = []
            with contextlib.suppress(Exception):
                self._unregister_session()
            self._stop_event_thread()
            self.entity_change.stop()
            self.fetch_errors = None
            self.connected = False
            with self._entities_condition:
                self.entities = None
                self._recently_converted_entities = {}
            if throw and exception is not None:
                raise exception

    def _register_session(self):
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmsession',
            call='registerSession',
            args=[self.CLIENT_TYPE_PYTHON],
        )
        if code:
            raise OSError(out)
        self.warnings = []
        self.session_uuid = UUID(out)
        self.logger.debug('Registered session %s', str(self.session_uuid))
        return self.session_uuid != self.zero_uuid

    def _unregister_session(self):
        if self.session_uuid == self.zero_uuid:
            return False
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmsession',
            call='unregisterSession',
            args=[str(self.session_uuid)],
        )
        if code:
            raise OSError(out)
        self.logger.debug('Unregistered session %s', str(self.session_uuid))
        self.session_uuid = self.zero_uuid
        return out

    def _start_event_thread(self):
        if self.session_uuid == self.zero_uuid:
            raise ValueError('No valid session')
        if self._event_thread is not None:
            self._stop_event_thread()
        self.logger.info('Start event thread for session %s', str(self.session_uuid))
        self._event_thread = threading.Thread(target=self._wait_for_events)
        self._event_thread.daemon = True
        self._event_thread.start()

    def _stop_event_thread(self):
        if self._event_thread is None:
            raise ValueError('Event thread not running')
        self._event_thread.join()
        self._event_thread = None

    def _wait_for_events(self):
        rpc = self.get_rpc()
        while self.session_uuid != self.zero_uuid:
            if self.connected:
                code, out = rpc.call(
                    service="cmsession",
                    call="waitForEvents",
                    args=[str(self.session_uuid), self.WAIT_FOR_EVENT_TIMEOUT],
                )
                if code:
                    self.logger.debug("End waiting for events, code: %d", code)
                    break
                if self._event_handler.handle(out):
                    self.connected = False
                    if not self.auto_reconnect or not self.cmdaemon_stopped:
                        self.logger.info("End waiting for events, needed to stop")
                        break
                    self.logger.info("End waiting for events, reconnect to cmd")
            else:
                time.sleep(5 if isinstance(self.auto_reconnect, bool) else self.auto_reconnect)
                try:
                    if self.connect(reconnecting=True):
                        self.logger.info("Resume waiting for events, reconnected to cmd")
                except OSError as e:
                    self.logger.info(f"Hold waiting events, reconnect error: {e}")

    def _end_of_session(self, reason):
        self.logger.debug('Session ended, reason: %s', reason)
        self.cmdaemon_stopped = reason.startswith("CMDaemon")

    def _add_warning(self, uuid, message, extended_message):
        self.warnings.append((uuid, message, extended_message))
        self.logger.debug('New warning: "%s", total: %d', message, len(self.warnings))

    def get_rpc(self) -> RPC:
        return RPC(self.settings)

    def next_local_uuid(self) -> UUID:
        return uuid4()

    def add(self, entity, force_uuids: bool = False, replace_existing: bool = True) -> int:
        """
        Add a new entity to the cluster.
        """
        if self.entities is None:
            return entity.uuid
        if not isinstance(entity, Entity):
            raise TypeError(f'No valid entity supplied: {type(entity).__name__}')
        if not entity.meta.top_level:
            raise ValueError('Not a top level entity')
        if replace_existing and entity._cluster is not None and entity._cluster != self:
            raise ValueError('Already added to a different cluster')
        if entity.is_committed and not force_uuids:
            raise ValueError('Already added and committed')
        if replace_existing and entity.uuid != self.zero_uuid and not force_uuids:
            raise ValueError('Already added')
        if entity._cluster is None:
            entity._cluster = self
        if entity._service is None:
            entity._service = self._find_service(entity.meta.service_type)
        with self._entities_condition:
            if replace_existing or entity.uuid not in self.entities:
                entity._set_uuids(self, force=force_uuids)
                self.entities[entity.uuid] = entity
        return entity.uuid

    def _find_service(self, service_type: str):
        return next((it for it in self._all_services if it.name == service_type), None)

    def _remove(self, uuid):
        with self._entities_condition:
            self.entities.pop(uuid, None)

    def _fetch(self, types: list[str] | None = None):
        if types is None:
            types = []
        fetch_errors = []
        entities = []
        threads = []
        condition = threading.Condition()
        for service in self._all_services:
            if (len(types) == 0) or (service.name in types):
                args = {
                    'service': service,
                    'entities': entities,
                    'fetch_errors': fetch_errors,
                    'condition': condition,
                }
                thread = threading.Thread(target=self.__fetch_one, kwargs=args)
                threads.append(thread)
        [it.start() for it in threads]
        [it.join() for it in threads]
        return entities, fetch_errors

    def __fetch_one(self, service, entities, fetch_errors, condition):
        self.logger.debug('Fetching %s via %s.%s', service.plural, service.proxy, service.get_all())
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service=service.proxy,
            call=service.get_all(),
        )
        if code == 0:
            converter = EntityConverter(self, service)
            converted = [converter.convert(it) for it in out if it is not None]
            converted = [it for it in converted if it is not None]
            self.logger.debug('Fetched %d / %d %s', len(converted), len(out), service.plural)
            with condition:
                entities += converted
        else:
            self.logger.warning('Failed to fetch %s, error: %s', service.plural, out)
            with condition:
                fetch_errors.append(out)
        return code, out

    def load_from_file(self, filename: str) -> EntityT:
        self.logger.info('Load %s', filename)
        with open(filename, encoding="utf-8") as fd:
            entity = json.load(fd)
        converter = EntityConverter(self, None)
        return converter.convert(entity)

    @property
    def all_entities(self):
        with self._entities_condition:
            return list(self.entities.values())

    def get_by_uuid(self, uuids: list[str] | list[UUID] | str | UUID | None) -> list[EntityT] | None:
        """
        Get entities by uuid or list of uuids
        """
        if uuids is None or uuids == self.zero_uuid:
            return None
        if uuids == []:
            return []
        with self._entities_condition:
            if self.entities is None:
                raise ValueError('No entities, not connected to cluster?')

            if isinstance(uuids, list):
                uuids = [UUID(it) if isinstance(it, str) else it for it in uuids]
                found = [self.entities.get(uuid, None) for uuid in uuids]
            elif isinstance(uuids, str):
                found = self.entities.get(UUID(uuids), None)
            else:
                found = self.entities.get(uuids, None)
            return found

    def get_by_name(self, name, instance_type=None):
        """
        Get the best matching entity by name over all possible types
        When instance_type is specified their is only one possible match
        """
        with self._entities_condition:
            if self.entities is None:
                raise ValueError('No entities, not connected to cluster?')
            lookup = [
                (entity.lookup(name, instance_type), entity)
                for entity in self.entities.values()
                if entity.lookup(name, instance_type) is not None
            ]
        if len(lookup) == 0:
            if instance_type is None or (
                isinstance(instance_type, str) and instance_type.lower() in {'device', 'node', 'headnode'}
            ):
                if name == 'active':
                    return self.active_head_node()
                if name == 'passive':
                    return self.passive_head_node()
            return None
        lookup.sort()
        return lookup[0][1]

    def get_by_type(
        self,
        instance_type: str | type[EntityT] | None,
        also_to_be_removed: bool = False,
    ) -> list[EntityT]:
        """
        Get all entities with the specified type
        """
        with self._entities_condition:
            if self.entities is None:
                raise ValueError('No entities, not connected to cluster?')
            return [
                entity
                for entity in self.entities.values()
                if (
                    ((instance_type is None) or entity.check_type(instance_type))
                    and (also_to_be_removed or not entity.to_be_removed)
                )
            ]

    def resolve_name_by_uuid(self, uuid, type_name='entity'):
        """
        Map an entity uuid to name.
        """
        entity = self.get_by_uuid(uuid)
        if entity is None:
            return f'unknown {type_name} with uuid: {uuid}'
        return entity.resolve_name

    def get_by_mac(self, mac: str):
        """
        Get all a device by mac.
        """
        with self._entities_condition:
            if self.entities is None:
                raise ValueError('No entities, not connected to cluster?')
            try:
                mac = mac.lower()
                return next(
                    (
                        entity
                        for entity in self.entities.values()
                        if ((e_mac := getattr(entity, 'mac', None)) is not None and e_mac.lower() == mac)
                    ),
                    None,
                )
            except Exception:
                return None

    def _entities_to_uuids(self, entities: Iterable[UUID | str | Entity | None]) -> list[UUID]:
        # TODO: perhaps we can do something clever here. Options are
        #       - Entity list   (works)
        #       - Key list      (works)
        #       - String list   (TODO)
        #       - Range syntax  (TODO: device only)
        return [Entity._convert_to_uuid(it) for it in entities]

    def register_recently_committed(self, uuid: UUID | list[UUID]) -> None:
        with self._entities_condition:
            if self._recently_committed_entities is not None:
                now = time.monotonic()
                if isinstance(uuid, list):
                    for it in uuid:
                        self._recently_committed_entities[it] = now
                else:
                    self._recently_committed_entities[uuid] = now

    def _process_update_removed(self, base_type: str, updated_uuids: list[UUID], removed_uuids: list[UUID]) -> None:
        self.logger.info(
            "Update %d, remove %d of type %s",
            len(updated_uuids),
            len(removed_uuids),
            base_type,
        )
        service = self._find_service(base_type)
        code = 0
        if bool(updated_uuids):
            with self._entities_condition:
                if self._recently_committed_entities is not None:
                    now = time.monotonic()
                    # KDR: keep cache of the last 5 seconds of commited entities, exclude from update
                    self._recently_committed_entities = {
                        uuid: timestamp
                        for uuid, timestamp in self._recently_committed_entities.items()
                        if now - timestamp < 5
                    }
                    updated_uuids = [it for it in updated_uuids if it not in self._recently_committed_entities]
        if bool(updated_uuids):
            rpc = self.get_rpc()
            get_by_uuids = service.get_by_uuids()
            if get_by_uuids is None:
                get_all = [
                    rpc.call(
                        service=service.proxy,
                        call=service.get_one(),
                        args=[it],
                    )
                    for it in updated_uuids
                ]
                code = max(it[0] for it in get_all)
                out = [it[1] for it in get_all if it[1] is not None]
            else:
                code, out = rpc.call(
                    service=service.proxy,
                    call=get_by_uuids,
                    args=[updated_uuids],
                )
            if code == RPC.OK and bool(out):
                with self._entities_condition:
                    now = time.monotonic()
                    # KDR: keep cache of the last 5 seconds of changed entities, to cope with changed event order
                    self._recently_converted_entities = {
                        uuid: (timestamp, entity)
                        for uuid, (timestamp, entity) in self._recently_converted_entities.items()
                        if now - timestamp < 5
                    }
                    converter = EntityConverter(self, service)
                    for entity in out:
                        if 'uuid' not in entity:
                            continue
                        converted = converter.convert(entity)
                        if converted is None:
                            self.logger.warning('Unable to convert entity during update')
                        else:
                            existing = self.entities.get(converted.uuid, None)
                            if existing is not None:
                                existing._merge_updated(converted, resolve_uuids=False)
                                self.logger.debug('Update, merged: %s', existing.resolve_name)
                                self._recently_converted_entities[existing.uuid] = (now, existing)
                            else:
                                converted._set_is_committed()
                                self.entities[converted.uuid] = converted
                                self.logger.debug('Update, added: %s', converted.resolve_name)
                                self._recently_converted_entities[converted.uuid] = (now, converted)
                    for _, entity in self._recently_converted_entities.values():
                        entity._resolve_uuids()
        if len(removed_uuids) > 0:
            with self._entities_condition:
                for remove_uuid in removed_uuids:
                    entity = self.entities.get(remove_uuid, None)
                    if entity is not None:
                        if entity.modified:
                            self.logger.debug(f'Removed, keep: {entity.resolve_name}')
                            entity._set_is_committed(False)
                        else:
                            self.entities.pop(remove_uuid, None)
                            self.logger.debug(f'Removed, drop {entity.resolve_name}')
        self.entity_change.notify(base_type, updated_uuids + removed_uuids)
        if code not in {RPC.OK, RPC.HTTP_SERVICE_RESTRICTED, RPC.HTTP_RPC_RESTRICTED}:
            raise OSError(out)

    def _update_active_passive_head_node(self):
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmmain',
            call='getActivePassiveUuids',
        )
        if code:
            raise OSError(out)
        self._active_passive_uuids = [UUID(it) if isinstance(it, str) else it for it in out]

    def active_head_node(self, force_update=False):
        """
        Get the active head node.
        """
        if self._active_passive_uuids is None or force_update:
            self._update_active_passive_head_node()
        if len(self._active_passive_uuids) > 0:
            return self.get_by_uuid(self._active_passive_uuids[0])
        return None

    def passive_head_node(self, force_update=False):
        """
        Get the passive head node.
        """
        if self._active_passive_uuids is None or force_update:
            self._update_active_passive_head_node()
        if len(self._active_passive_uuids) > 1:
            return self.get_by_uuid(self._active_passive_uuids[1])
        return None

    @property
    def name(self):
        """
        Get the cluster name
        """
        base_partition = self.get_base_partition()
        if base_partition is None:
            return None
        return base_partition.clusterName

    def get_base_partition(self):
        """
        Get the base partition.
        """
        return self.get_by_name('base', 'Partition')

    def version_info(self):
        """
        Get cmdaemon version information.
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmmain',
            call='getVersion',
        )
        if code:
            raise OSError(out)
        if out is None:
            return out
        return VersionInfo(self, out)

    def license_info(self):
        """
        Get cmdaemon license information.
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmmain',
            call='getLicenseInfo',
        )
        if code:
            raise OSError(out)
        if out is None:
            return out
        return LicenseInfo(self, out)

    def cluster_setup(self):
        """
        Get cmdaemon cluster setup.
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmmain',
            call='getClusterSetup',
        )
        if code:
            raise OSError(out)
        if out is None:
            return out
        return ClusterSetup(self, out)

    def server_status(self):
        """
        Get cmdaemon server status.
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmmain',
            call='getServerStatus',
        )
        if code:
            raise OSError(out)
        if out is None:
            return out
        return CMDaemonStatus(self, out)

    def overview(self, basic: bool = True):
        """
        Get cluster overview

        Basic: do not add per gpu, switch, power shelf information
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmgui',
            call='getClusterOverview',
            args=[basic],
        )
        if code:
            raise OSError(out)
        if out is None:
            return out
        return GuiClusterOverview(self, out, self)

    def dns_node_mapping(self):
        """
        Get DNS server node mapping
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='getAllDnsNodeServerPairs',
        )
        if code:
            raise OSError(out)
        return TargetSourceMapping(self, out['nodes'], out['servers'])

    def dhcp_node_mapping(self):
        """
        Get DHCP server node mapping
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='getAllDhcpNodeServerPairs',
        )
        if code:
            raise OSError(out)
        return TargetSourceMapping(self, out['nodes'], out['servers'])

    def get_all_certificates(self):
        """
        Get all known certificates.
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmcert',
            call='getCertificates',
        )
        if code:
            raise OSError(out)
        return [Certificate(self, it) for it in out]

    def get_all_certificate_requests(self):
        """
        Get all current certificate requests.
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmcert',
            call='getCertificateRequests',
        )
        if code:
            raise OSError(out)
        return [CertificateRequest(self, it) for it in out]

    def get_disk_setups(self):
        """
        Get all predefined disk setup templates
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='getDiskSetups',
        )
        if code:
            raise OSError(out)
        return dict(list(zip(out['names'], out['templates'])))

    def get_raid_setups(self):
        """
        Get all predefined raid setup templates
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='getRaidSetups',
        )
        if code:
            raise OSError(out)
        return dict(list(zip(out['names'], out['templates'])))

    @property
    def new_nodes(self):
        """
        Get nodes which are booted but have no configuration.
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='getNewNodes',
        )
        if code:
            raise OSError(out)
        return [NewNode(self, it) for it in out]

    def hardware_overview(self, grouped=True):
        """
        Get the hardware overview for the nodes in the cluster
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmmain',
            call='getHardwareOverview',
            args=[grouped],
        )
        if code:
            raise OSError(out)
        return [dict(attr_to_value.split("=", 1) for attr_to_value in item.get("list", [])) for item in out]

    @property
    def head_in_the_cloud(self):
        """
        Determine if the head node runs in the cloud
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmmain',
            call='masterOnCloud',
        )
        if code:
            raise OSError(out)
        return out

    def report_critical_error(
        self,
        recipients=None,
        message='Critical error report from pythoncm',
        body='',
    ):
        """
        Report a critical error to all e-mail recipients.
        If none are spcecified all cluster administrators will be used.
        """
        if recipients is None:
            recipients = []
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmmain',
            call='reportCriticalError',
            args=[recipients, message, body],
        )
        if code:
            raise OSError(out)
        return out

    def regenerate_user_certificates(self):
        """
        Regenerate all user certificates
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmuser',
            call='regenerateUserCertificates',
            args=[[]],
        )
        if code:
            raise OSError(out)
        return out.get('success', False), out.get('info', ''), out.get('errors', '')

    def import_entity_from_json(self, file_name):
        """
        Import entity from a file that exists on the head node
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmmain',
            call='importEntity',
            args=[file_name, 0],
        )
        if code:
            raise OSError(out)
        return (
            out.get('updated', False),
            out.get('new_uuid', self.zero_uuid),
            out.get('task_uuid', self.zero_uuid),
            out.get('validation', []),
        )

    def get_all_cm_shared_paths(self):
        all_fspart = self.get_by_type(FSPart)
        return [it.path for it in all_fspart if it.type == it.meta.Type.CM_SHARED]

    def get_all_cm_node_installer_paths(self):
        all_fspart = self.get_by_type(FSPart)
        return [it.path for it in all_fspart if it.type == it.meta.Type.CM_NODE_INSTALLER]

    def get_arch_os_fspart_images(self):
        """
        Get all arch/os shared/installer image information
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmpart',
            call='getArchOSFSPartImages',
        )
        if code:
            raise OSError(out)
        info = []
        for arch_os, head_node, shared, installer, primary_image, secondary_images in zip(
            out.get('archOS', []),
            out.get('headNode', []),
            out.get('shared', []),
            out.get('installer', []),
            out.get('primaryImage', []),
            out.get('secondaryImages', []),
        ):
            info.append(
                {
                    'ArchOS': arch_os,
                    'head_node': head_node,
                    'shared': self.get_by_uuid(shared),
                    'installer': self.get_by_uuid(installer),
                    'primary_image': self.get_by_uuid(primary_image),
                    'secondary_images': [self.get_by_uuid(it) for it in secondary_images],
                }
            )
        return info

    def commit(
        self,
        entities: list[Entity],
        wait_for_task: bool = False,
        force: typing.SupportsInt = False,
        local_validate_check: bool = True,
        wait_for_remote_update: bool = False,
        timeout: int = 3600,
    ) -> tuple[MultiCommitResult, MultiCommitResult]:
        service = None
        entity_type = None
        add = []
        update = []
        add_check_result = []
        update_check_result = []
        for entity in entities:
            if not entity.meta.allow_commit:
                raise TypeError(f'The {entity.baseType} {entity.resolve_name} is read only and cannot be committed')
            if not entity.meta.top_level:
                raise TypeError(f'The {entity.baseType} {entity.resolve_name} cannot be committed by itself')
            if entity_type is None:
                service = entity._service
                entity_type = entity.baseType
            elif not entity.check_type(entity_type):
                raise TypeError(f'Entity types do not match: {entity_type}, {entity.baseType}')
            entity._set_uuids()
            entity._update_modified()
            if not entity.is_committed:
                add.append(entity)
                if local_validate_check:
                    add_check_result += entity.check()
            else:
                update.append(entity)
                if local_validate_check:
                    update_check_result += entity.check()

        if bool(add):
            if wait_for_remote_update:
                self.entity_change.reset()
            rpc = self.get_rpc()
            try:
                from pythoncm.entity.metadata.validation import Validation

                code, out = rpc.call(
                    service=service.proxy,
                    call=service.add_multi(),
                    args=[[it.to_dict() for it in add], int(force)],
                    timeout=timeout,
                )
                if code:
                    raise OSError(out)
                add_commit_result = MultiCommitResult(self, **out)
                add_commit_result.add(add_check_result, severity=Validation.Severity.WARNING)
            except Exception:
                if add_check_result == []:
                    raise
                add_commit_result = MultiCommitResult(self, success=[False] * len(add))
                add_commit_result.add(add_check_result)
            successfully_committed_uuid = []
            if bool(add_commit_result.extra_entities):
                for extra_entity in add_commit_result.extra_entities:
                    self.logger.debug('Add extra: %s', extra_entity.resolve_name)
                    self.add(extra_entity, replace_existing=False)
            for entity, success in zip(add, add_commit_result.success):
                if success:
                    entity._set_is_committed()
                    entity._clear_modified()
                    updated_entity = add_commit_result.updated_entity(entity.uuid)
                    if updated_entity:
                        self.logger.debug('Merge updated entity: %s', entity.resolve_name)
                        entity._merge_updated(updated_entity)
                    successfully_committed_uuid.append(entity.uuid)
                    self.logger.debug('Added: %s', entity.resolve_name)
                else:
                    self.logger.info('Failed to add: %s', entity.resolve_name)
            if bool(successfully_committed_uuid):
                if wait_for_remote_update:
                    self.entity_change.wait(successfully_committed_uuid)
                else:
                    self.register_recently_committed(successfully_committed_uuid)
        else:
            add_commit_result = None

        if bool(update):
            if wait_for_remote_update:
                self.entity_change.reset()
            rpc = self.get_rpc()
            try:
                from pythoncm.entity.metadata.validation import Validation

                code, out = rpc.call(
                    service=service.proxy,
                    call=service.update_multi(),
                    args=[[it.to_dict() for it in update], int(force)],
                    timeout=timeout,
                )
                if code:
                    raise OSError(out)
                update_commit_result = MultiCommitResult(self, **out)
                update_commit_result.add(update_check_result, severity=Validation.Severity.WARNING)
                for entity, success in zip(update, update_commit_result.success):
                    if success:
                        updated_entity = update_commit_result.updated_entity(entity.uuid)
                        if updated_entity:
                            entity._merge_updated(updated_entity)
                        entity._clear_modified()
                        self.logger.debug('Updated: %s', entity.resolve_name)
                    else:
                        self.logger.info('Failed to update: %s', entity.resolve_name)
            except Exception:
                if update_check_result == []:
                    raise
                update_commit_result = MultiCommitResult(self, success=[False] * len(update))
                update_commit_result.add(update_check_result)
            uuids = [entity.uuid for entity, success in zip(update, update_commit_result.success) if success]
            if bool(uuids):
                if wait_for_remote_update:
                    self.entity_change.wait(uuids)
                else:
                    self.register_recently_committed(uuids)
        else:
            update_commit_result = None

        if wait_for_task:
            if add_commit_result is not None:
                add_commit_result.wait_for_task()
            if update_commit_result is not None:
                update_commit_result.wait_for_task()
        return add_commit_result, update_commit_result

    def remove(
        self,
        entities: list[Entity],
        force: typing.SupportsInt = False,
        *args,
    ) -> MultiRemoveResult:
        service = None
        entity_type = None
        if not bool(entities):
            return MultiRemoveResult(self)
        remove_uuids = []
        for entity in entities:
            if not entity.meta.allow_commit:
                raise TypeError(f'The {entity.baseType} {entity.resolve_name} is read only and cannot be removed')
            if not entity.meta.top_level:
                raise TypeError(f'The {entity.baseType} {entity.resolve_name} cannot be removed by itself')
            if entity_type is None:
                service = entity._service
                entity_type = entity.baseType
            elif not entity.check_type(entity_type):
                raise TypeError(f'Entity types do not match: {entity_type}, {entity.baseType}')
            remove_uuids.append(entity.uuid)
        rpc = self.get_rpc()
        code, out = rpc.call(
            service=service.proxy,
            call=service.remove_multi(),
            args=[remove_uuids, *args, int(force)],
        )
        if code:
            raise OSError(out)
        return MultiRemoveResult(self, **out)

    def installer_interactions(self) -> list[RemoteNodeInstallerInteraction]:
        """
        Get all remote node installer interactions
        """
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='getRemoteNodeInstallerInteractions',
        )
        if code:
            raise OSError(out)
        return [RemoteNodeInstallerInteraction(self.cluster, it) for it in out]

    def file_write_info(
        self,
        nodes: str | type[EntityT] | None = None,
        path: str | list[str] | None = None,
        history: bool = False,
    ) -> list[FileWriteInfo]:
        """
        Get files that have been written
        """
        if nodes is None:
            nodes = []
        if path is None:
            path = []
        elif isinstance(path, str):
            path = [path]
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='getFileWriteInfo',
            args=[self._entities_to_uuids(nodes), path, history],
        )
        if code:
            raise OSError(out)
        return [FileWriteInfo(self, it) for it in out]

    def report_file_write(
        self,
        path: str | list[str],
        frozen: bool | list[bool] = False,
        cm_setup: bool = True,
        node: UUID | Node | None = None,
    ) -> None:
        """
        Report files that have been written so cmd can keep track
        """
        if node is None:
            node = self.active_head_node().uuid
        elif isinstance(node, Node):
            node = node.uuid
        added = []
        for index, _filename in enumerate(path):
            info = FileWriteInfo()
            info.ref_device_uuid = node
            info.path = path
            info.actor = info.meta.Actor.CM_SETUP if cm_setup else info.meta.Actor.PYTHONCM
            info.timestamp = int(time.time())
            if isinstance(frozen, list):
                info.frozen = frozen[index] if index < len(frozen) else False
            else:
                info.frozen = frozen
            added.append(info.to_dict())
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='addFileWriteInfo',
            args=[added],
        )
        if code:
            raise OSError(out)
        return out

    def get_network_for_ip(self, ip: str) -> Network | None:
        """
        Find the network that contains the given IP
        """
        for network in self.get_by_type(Network):
            if network.contains_ip(ip):
                return network
        return None

    def dhcpd_leases(self, nodes: list[Node | UUID] | None) -> list[dict[str, bool | str | dict[str, str | int]]]:
        """
        Gets dhcpd leases
        """
        if nodes is None:
            node_filter = NodeFilter(self)
            nodes = [node for node, _ in node_filter.get(lambda role: isinstance(role, BootRole))]
        rpc = self.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='pgetDhcpdLeases',
            args=[nodes],
        )
        if code:
            raise OSError(out)
        return out

    def list_user_data(self, all_users: bool = False) -> list[tuple[str, str]]:
        """
        List all (user, key) pairs for user data
        """
        rpc = self.get_rpc()
        code, out = rpc.call(
            service='cmsession',
            call='listClientUserData',
            args=[all_users],
        )
        if code:
            raise OSError(out)
        return list(zip(out.get("users", []), out.get("keys", [])))

    def get_user_data(self, key: str) -> str:
        """
        Get for user data for a specific key
        """
        rpc = self.get_rpc()
        code, out = rpc.call(
            service='cmsession',
            call='getClientUserData',
            args=[key],
        )
        if code:
            raise OSError(out)
        return out

    def set_user_data(self, key: str, data: str) -> bool:
        """
        Set for user data for a specific key
        """
        rpc = self.get_rpc()
        code, out = rpc.call(
            service='cmsession',
            call='setClientUserData',
            args=[key, data],
        )
        if code:
            raise OSError(out)
        return out

    def start_request_remote_assistance(self, ticket_number: str, message: str) -> tuple[bool, str]:
        """
        Start a new request-remote-assistance if not already running
        """
        rpc = self.get_rpc()
        code, out = rpc.call(
            service='cmmain',
            call='startRequestRemoteAssistanceData',
            args=[ticket_number, message],
        )
        if code:
            raise OSError(out)
        return out.get("result", False), out.get("info", "")

    def stop_request_remote_assistance(self) -> tuple[bool, str]:
        """
        Stop request-remote-assistance
        """
        rpc = self.get_rpc()
        code, out = rpc.call(
            service='cmmain',
            call='stopRequestRemoteAssistanceData',
        )
        if code:
            raise OSError(out)
        return out.get("result", False), out.get("info", "")

    def status_request_remote_assistance(self) -> tuple[bool, str]:
        """
        Status of request-remote-assistance
        """
        rpc = self.get_rpc()
        code, out = rpc.call(
            service='cmmain',
            call='statusRequestRemoteAssistanceData',
        )
        if code:
            raise OSError(out)
        return out.get("result", False), out.get("info", "")

    def send_warning_event(
        self, message: str, extended_message: str = "", severity: int = EVENT_SEVERITY_WARNING
    ) -> bool:
        """
        Send a warning event to the head node that will be broadcast to all clients
        """
        event = {
            "uuid": str(self.next_local_uuid()),
            "baseType": "Event",
            "childType": "WarningEvent",
            "msg": message,
            "extendedMsg": extended_message,
            "creation_time": int(time.time()),
            "severity": severity,
            "broadcast": True,
        }
        rpc = self.get_rpc()
        code, out = rpc.call(
            service="cmsession",
            call="handleEvent",
            args=[event],
        )
        if code:
            raise OSError(out)
        return out

    def network_topology(
        self,
        devices: list[Device | UUID] | None = None,
        racks: list[Rack | UUID] | None = None,
        link: bool = False,
        cached: bool = True,
    ) -> list[dict[str, str | int]]:
        """
        Get the network topology
        """
        if devices is None:
            devices = []
        else:
            devices = self._entities_to_uuids(devices)
        if racks is None:
            racks = []
        else:
            racks = self._entities_to_uuids(racks)
        rpc = self.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='networkTopology',
            args=[devices, racks, link, cached],
        )
        if code:
            raise OSError(out)
        return out

    def check_edition_disabled_feature(self, name: str) -> bool:
        """
        Check if a feature is disabled based on the license edition
        """
        if self.edition_disabled_features is None:
            rpc = self.get_rpc()
            code, out = rpc.call(
                service='cmmain',
                call='getEditionDisabledFeatures',
            )
            if code:
                raise OSError(out)
            self.edition_disabled_features = out
        return any(name.lower() == it.lower for it in self.edition_disabled_features)

    def lite_daemon_download_packages(self) -> bool:
        """
        Update the cached downloaded cm-lite-daemon packages for switches and lite nodes
        """
        rpc = self.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='liteDaemonDownloadPackages',
        )
        if code:
            raise OSError(out)
        return out.get("success", False), out.get("stdout", ""), out.get("stderr", "")
