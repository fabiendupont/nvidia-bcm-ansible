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

import os
import pwd
import typing
from uuid import UUID

import pythoncm.entity.metadata.devicestatus
import pythoncm.entity.metadata.poweroperation
from pythoncm.drain_status_waiter import DrainStatusWaiter
from pythoncm.entity import BlockingOperation
from pythoncm.entity import BurnConfig
from pythoncm.entity import BurnStatus
from pythoncm.entity import DrainResult
from pythoncm.entity import ExternalOperationResult
from pythoncm.entity import FirmwareInfo
from pythoncm.entity import ImexCtlNode
from pythoncm.entity import NetworkConnection
from pythoncm.entity import NVSMInfo
from pythoncm.entity import Package
from pythoncm.entity import PingResult
from pythoncm.entity import PowerOperation
from pythoncm.entity import PowerOperationHistory
from pythoncm.entity import ProgramRunnerInput
from pythoncm.entity import Route
from pythoncm.entity import VersionInfo
from pythoncm.entity.cloudnode import CloudNode
from pythoncm.entity.devicestatus import DeviceStatus
from pythoncm.entity.node import Node
from pythoncm.entity.programrunnerstatus import ProgramRunnerStatus
from pythoncm.entity.sysinfocollector import SysInfoCollector
from pythoncm.entity_converter import EntityConverter
from pythoncm.util import convert_to_uuid
from pythoncm.util import name_compare
from pythoncm.util import uuid_compare

if typing.TYPE_CHECKING:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import Device
    from pythoncm.entity import DPUNode
    from pythoncm.entity import JobQueue
    from pythoncm.entity import LiteNode
    from pythoncm.entity import MonitoringAction
    from pythoncm.entity import Switch
    from pythoncm.entity import WlmCluster


class Parallel:
    """
    Wrapper class around all parallel RPC
    """

    def __init__(self, cluster: Cluster):
        self.cluster = cluster

    def device_status(self, devices: list[Device | UUID]):
        """
        Get the device status for one or more devices.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmstatus',
            call='getStatusForDevices',
            args=[self.cluster._entities_to_uuids(devices)],
        )
        if code:
            raise OSError(out)
        return [
            DeviceStatus(
                self.cluster, it, parent=self.cluster.get_by_uuid(it.get('ref_device_uuid', self.cluster.zero_uuid))
            )
            for it in out
            if it is not None
        ]

    def _power_operation(
        self,
        devices: list[Device | UUID],
        operation,
        force: bool = False,
        wait: bool = False,
        timeout: float | None = None,
    ) -> bool:
        power_operation = PowerOperation()
        power_operation.devices = self.cluster._entities_to_uuids(devices)
        power_operation.session_uuid = self.cluster.session_uuid
        power_operation.force = force
        power_operation.operation = operation
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='powerOperation',
            args=[power_operation.to_dict()],
        )
        if code:
            raise OSError(out)
        count = out.get('count', 0)
        if count == 0:
            return False
        if wait:
            index = out.get('index', 0)
            return self.cluster.power_operation_manager.wait(
                devices=power_operation.devices,
                index=index,
                count=count,
                timeout=timeout,
            )
        return True

    def power_status(
        self,
        devices: list[Device | UUID],
        force: bool = False,
        wait: bool = True,
        timeout: float | None = None,
    ):
        """
        Get the power status for one or more devices.

        force: include closed devices
        wait: wait for completion
        """
        return self._power_operation(
            operation=pythoncm.entity.metadata.poweroperation.PowerOperation.Operation.STATUS,
            devices=devices,
            force=force,
            wait=wait,
            timeout=timeout,
        )

    def power_on(
        self,
        devices: list[Device | UUID],
        force: bool = False,
        wait: bool = False,
        timeout: float | None = None,
    ):
        """
        Power on for one or more devices.

        force: include closed devices
        wait: wait for completion
        """
        return self._power_operation(
            operation=pythoncm.entity.metadata.poweroperation.PowerOperation.Operation.ON,
            devices=devices,
            force=force,
            wait=wait,
            timeout=timeout,
        )

    def power_off(
        self,
        devices: list[Device | UUID],
        force: bool = False,
        wait: bool = False,
        timeout: float | None = None,
    ):
        """
        Power off for one or more devices.

        force: include closed devices
        wait: wait for completion
        """
        return self._power_operation(
            operation=pythoncm.entity.metadata.poweroperation.PowerOperation.Operation.OFF,
            devices=devices,
            force=force,
            wait=wait,
            timeout=timeout,
        )

    def power_reset(
        self,
        devices: list[Device | UUID],
        force: bool = False,
        wait: bool = False,
        timeout: float | None = None,
    ):
        """
        Power reset for one or more devices.

        force: include closed devices
        wait: wait for completion
        """
        return self._power_operation(
            operation=pythoncm.entity.metadata.poweroperation.PowerOperation.Operation.RESET,
            devices=devices,
            force=force,
            wait=wait,
            timeout=timeout,
        )

    def open(self, devices: list[Device | UUID], message: str | None = None):
        """
        Open for one or more devices.

        message: update the current status user message
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmstatus',
            call='open',
            args=[
                self.cluster._entities_to_uuids(devices),
                '' if message is None else message,
                message is not None,
            ],
        )
        if code:
            raise OSError(out)
        return out

    def close(self, devices: list[Device | UUID], message: str | None = None):
        """
        Close for one or more devices.

        message: update the current status user message
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmstatus',
            call='close',
            args=[
                self.cluster._entities_to_uuids(devices),
                '' if message is None else message,
                message is not None,
            ],
        )
        if code:
            raise OSError(out)
        return out

    def mute(self, devices: list[Device | UUID], message: str | None = None):
        """
        Mute for one or more devices, no more monitorring actions will be triggered

        message: update the current status user message
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmstatus',
            call='mute',
            args=[
                self.cluster._entities_to_uuids(devices),
                '' if message is None else message,
                message is not None,
            ],
        )
        if code:
            raise OSError(out)
        return out

    def unmute(self, devices: list[Device | UUID], message: str | None = None):
        """
        Unmute for one or more devices.

        message: update the current status user message
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmstatus',
            call='unmute',
            args=[
                self.cluster._entities_to_uuids(devices),
                '' if message is None else message,
                message is not None,
            ],
        )
        if code:
            raise OSError(out)
        return out

    def restart_required(self, devices: list[Device | UUID], reasons=None):
        """
        Set restart required for one or more devices.

        reasons: list of reasons, or single reason, restart is required
        """
        if reasons is None:
            reasons = []
        elif isinstance(reasons, str):
            reasons = [reasons]
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmstatus',
            call='setRestartRequired',
            args=[
                self.cluster._entities_to_uuids(devices),
                reasons,
            ],
        )
        if code:
            raise OSError(out)
        return out

    def clear_restart_required(self, devices):
        """
        Set restart required for one or more devices.

        message: update the current status user message
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmstatus',
            call='clearRestartRequired',
            args=[self.cluster._entities_to_uuids(devices)],
        )
        if code:
            raise OSError(out)
        return out

    def set_info_message(self, devices: list[Device | UUID], message, low_level_update: bool = False):
        """
        Set the info message for one or more devices.

        message: update the current status user message
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmstatus',
            call='setInfoMessage',
            args=[
                self.cluster._entities_to_uuids(devices),
                message,
                low_level_update,
            ],
        )
        if code:
            raise OSError(out)
        return out

    def set_user_message(self, devices: list[Device | UUID], message, low_level_update: bool = False):
        """
        Set the info message for one or more devices.

        message: update the current status user message
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmstatus',
            call='setUserMessage',
            args=[
                self.cluster._entities_to_uuids(devices),
                message,
                low_level_update,
            ],
        )
        if code:
            raise OSError(out)
        return out

    def set_tool_message(self, devices: list[Device | UUID], message, low_level_update: bool = False):
        """
        Set the info message for one or more devices.

        message: update the current status tool message
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmstatus',
            call='setToolMessage',
            args=[
                self.cluster._entities_to_uuids(devices),
                message,
                low_level_update,
            ],
        )
        if code:
            raise OSError(out)
        return out

    def image_update(
        self,
        nodes: list[Node | UUID],
        dry_run: bool = False,
        wait: bool = False,
        timeout: float | None = None,
        include_paths=None,
        selections=None,
    ):
        """
        Perform an image update on one or more devices.
        """
        if include_paths is None:
            include_paths = []
        if selections is None:
            selections = []
        node_uuids = self.cluster._entities_to_uuids(nodes)
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='imageUpdate',
            args=[
                node_uuids,
                dry_run,
                self.cluster.session_uuid,
                include_paths,
                selections,
            ],
        )
        if code:
            raise OSError(out)
        out = convert_to_uuid(out)
        if wait and bool(out):
            self.cluster.provisioning.wait_requests(
                [uuid for uuid in out if uuid != self.cluster.zero_uuid],
                timeout=timeout,
            )
        return out

    def accelerators(self, nodes: list[Node | UUID] | None) -> list[tuple[Node | UUID, int]]:
        """
        Get the number accelerators
        """
        if nodes is None:
            nodes = self.cluster.get_by_type(Node)
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='getNodeAcceleratorCounts',
            args=[self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return list(zip(nodes, out))

    def system_information(
        self, nodes: list[Node | UUID] | None, basic: bool = False, add_empty: bool = False
    ) -> list[SysInfoCollector]:
        """
        Get the system information for one or more nodes.
        """
        if nodes is None:
            nodes = self.cluster.get_by_type(Node)
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='getSysInfoCollectors',
            args=[self.cluster._entities_to_uuids(nodes), basic, add_empty],
        )
        if code:
            raise OSError(out)
        return [
            SysInfoCollector(
                self.cluster,
                it,
                parent=self.cluster.get_by_uuid(it['ref_device_uuid']),
            )
            for it in out
        ]

    def update_system_information(self, nodes: list[Node | UUID] | None) -> list[bool]:
        """
        Get the system information for one or more nodes.
        """
        if nodes is None:
            nodes = self.cluster.get_by_type(Node)
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='pupdateSysInfoCollectors',
            args=[self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return out

    def reload_managers(self, nodes: list[Node | UUID] | None) -> list[bool]:
        """
        Reload the entity managers on the nodes, use only when they are out of sync
        """
        if nodes is None:
            nodes = self.cluster.get_by_type(Node)
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='preload',
            args=[self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return out

    def reboot(
        self, nodes: list[Node | UUID], run_pre_halt_operations: bool = True, pre_halt_operations_timeout: int = 300
    ):
        """
        Reboot one or more nodes.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='preboot',
            args=[
                run_pre_halt_operations,
                int(pre_halt_operations_timeout * 1000),
                self.cluster._entities_to_uuids(nodes),
            ],
        )
        if code:
            raise OSError(out)
        operations = [BlockingOperation(self.cluster, it) for it in out['operations']]
        return {
            it[0]: (it[1], [jt for jt in operations if uuid_compare(jt.ref_node_uuid, it[0])])
            for it in zip(nodes, out['success'])
        }

    def shutdown(
        self, nodes: list[Node | UUID], run_pre_halt_operations: bool = True, pre_halt_operations_timeout: int = 300
    ):
        """
        Shutdown one or more nodes.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='pshutdown',
            args=[
                run_pre_halt_operations,
                int(pre_halt_operations_timeout * 1000),
                self.cluster._entities_to_uuids(nodes),
            ],
        )
        if code:
            raise OSError(out)
        operations = [BlockingOperation(self.cluster, it) for it in out['operations']]
        return {
            it[0]: (it[1], [jt for jt in operations if uuid_compare(jt.ref_node_uuid, it[0])])
            for it in zip(nodes, out['success'])
        }

    def service_status(self, nodes: list[Node | UUID], name: str | None = None):
        """
        Get the status of all or one service on one or more nodes.
        """
        rpc = self.cluster.get_rpc()
        if name is None:
            (code, out) = rpc.call(
                service='cmserv',
                call='pgetOSServices',
                args=[self.cluster._entities_to_uuids(nodes)],
            )
        else:
            (code, out) = rpc.call(
                service='cmserv',
                call='pgetOSService',
                args=[
                    name,
                    self.cluster._entities_to_uuids(nodes),
                ],
            )
        if code:
            raise OSError(out)
        converter = EntityConverter(self.cluster, service=None)
        return [converter.convert(it) for it in out]

    def service_start(self, nodes: list[Node | UUID], name: str, args=None):
        """
        Start a service on one or more nodes.
        """
        if args is None:
            args = []
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmserv',
            call='pstartOSService',
            args=[
                name,
                args,
                self.cluster._entities_to_uuids(nodes),
            ],
        )
        if code:
            raise OSError(out)
        return out

    def service_stop(self, nodes: list[Node | UUID], name: str, args=None):
        """
        Stop a service on one or more nodes.
        """
        if args is None:
            args = []
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmserv',
            call='pstopOSService',
            args=[
                name,
                args,
                self.cluster._entities_to_uuids(nodes),
            ],
        )
        if code:
            raise OSError(out)
        return out

    def service_restart(self, nodes: list[Node | UUID], name: str, args=None):
        """
        Restart a service on one or more nodes.
        """
        if args is None:
            args = []
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmserv',
            call='prestartOSService',
            args=[
                name,
                args,
                self.cluster._entities_to_uuids(nodes),
            ],
        )
        if code:
            raise OSError(out)
        return out

    def service_reload(self, nodes: list[Node | UUID], name: str, args=None):
        """
        Reload a service on one or more nodes.
        """
        if args is None:
            args = []
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmserv',
            call='preloadSService',
            args=[
                name,
                args,
                self.cluster._entities_to_uuids(nodes),
            ],
        )
        if code:
            raise OSError(out)
        return out

    def service_reset(self, nodes: list[Node | UUID], name: str, args=None):
        """
        Reset the failed count for a service on one or more nodes.
        """
        if args is None:
            args = []
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmserv',
            call='presetOSService',
            args=[
                name,
                args,
                self.cluster._entities_to_uuids(nodes),
            ],
        )
        if code:
            raise OSError(out)
        return out

    def service_update(self, nodes: list[Node | UUID], name: str, wait: bool = False) -> list[bool]:
        """
        Update a service and request an event to be send in response
        """
        rpc = self.cluster.get_rpc()
        nodes = self.cluster._entities_to_uuids(nodes)
        (code, out) = rpc.call(
            service='cmserv',
            call='pupdateOSService',
            args=[
                name,
                self.cluster.session_uuid,
                nodes,
            ],
        )
        if code:
            raise OSError(out)
        if wait and sum(out):
            self.cluster.service_update_manager.wait(
                [node for node, updated in zip(nodes, out) if updated],
                name,
            )
        return out

    def active_command_status(
        self,
        internal: bool = False,
        ids: list[UUID] | None = None,
        nodes: list[Node | UUID] | None = None,
        command: str | None = None,
    ):
        """
        Get all active remote execute programmer runner status

        internal: also return programmer runners started by cmdaemon
        ids: return only status with matching IDs
        nodes: return only status if running on at least one node
        command: return only status if the command matches
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmproc',
            call='listCommands',
            args=[internal],
        )
        if code:
            raise OSError(out)
        status = [ProgramRunnerStatus(self.cluster, it) for it in out]
        if ids:
            status = [it for it in status if it.uuid in ids]
        if nodes:
            status = [it for it in status if set(it.nodes) & set(nodes)]
        if command:
            status = [it for it in status if set(it.input.cmd) == command]
        return status

    def execute(
        self,
        nodes: list[Node | UUID],
        command: str,
        args: list[str] | None = None,
        env: dict[str, str] | None = None,
        user: str | None = None,
        run_in_shell: bool = True,
        stdin: str | None = None,
        merge_stdout_stderr: bool = False,
        max_run_time=None,
        wait: bool = True,
        timeout=None,
        info=None,
    ):
        """
        Execute a command on one or more nodes.

        nodes: list of nodes to execute the command.
        command: command to be executes.
        args: additional arguments to the command.
        env: extra environment variables to be set.
        user: execute the command as a specific user.
        run_in_shell: run the command inside the users default shell.
        stdin: data to be passed to the processes standard in.
        merge_stdout_stderr: merge standard out and error into one.
        max_run_time: maximal runtime before the script gets killed.
        wait: wait for completion.
        timeout: time for python to wait, the script will continue to run.
        info: additional info for debugging purposes
        """
        program_runner_input = ProgramRunnerInput()
        program_runner_input.cmd = command
        program_runner_input.mergeCoutCerr = merge_stdout_stderr
        program_runner_input.startInShell = run_in_shell
        if args is not None:
            program_runner_input.args = args
        if env is not None:
            program_runner_input.env = env
        if info is not None:
            program_runner_input.info = info
        if stdin is not None:
            program_runner_input.datacin = stdin
        if max_run_time is not None:
            program_runner_input.maxruntime = max_run_time
        if user is None:
            program_runner_input.user = pwd.getpwuid(os.getuid())[0]
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmproc',
            call='runCommand',
            args=[
                self.cluster._entities_to_uuids(nodes),
                program_runner_input,
                self.cluster.session_uuid,
            ],
        )
        if code:
            raise OSError(out)
        program_runner_status = ProgramRunnerStatus(self.cluster, out)
        self.cluster.remote_execution_manager.register(program_runner_status)
        done = None
        if wait:
            done = program_runner_status.wait(timeout)
            if done:
                self.cluster.remote_execution_manager.unregister(program_runner_status)
        return done, program_runner_status

    def drain_status(
        self,
        nodes: list[Node | UUID],
        wlms: list[WlmCluster | UUID] | None = None,
    ):
        """
        Get the workload managers drain status for one or more nodes.
        """
        if wlms is None:
            wlms = []
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmjob',
            call='drainOverview',
            args=[
                self.cluster._entities_to_uuids(wlms),
                self.cluster._entities_to_uuids(nodes),
            ],
        )
        if code:
            raise OSError(out)
        return [DrainResult(self.cluster, it) for it in out]

    def drain(
        self,
        nodes: list[Node | UUID],
        wlms: list[WlmCluster | UUID] | None = None,
        queues: list[JobQueue | UUID] | None = None,
        add_actions: list[MonitoringAction | UUID] | None = None,
        remove_actions: list[MonitoringAction | UUID] | None = None,
        clear_actions: bool = False,
        reason: str = '',
        drain: bool = True,
    ):
        """
        Drain one or more nodes in workload managers.
        """
        if wlms is None:
            wlms = []
        if queues is None:
            queues = []
        if add_actions is None:
            add_actions = []
        if remove_actions is None:
            remove_actions = []
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmjob',
            call='drainNodes',
            args=[
                self.cluster._entities_to_uuids(wlms),
                self.cluster._entities_to_uuids(queues),
                self.cluster._entities_to_uuids(nodes),
                drain,
                add_actions,
                remove_actions,
                clear_actions,
                reason,
            ],
        )
        if code:
            raise OSError(out)
        return [DrainResult(self.cluster, it) for it in out.get('results', [])]

    def undrain(
        self,
        nodes: list[Node | UUID],
        wlms: list[WlmCluster | UUID] | None = None,
        queues: list[JobQueue | UUID] | None = None,
    ):
        """
        Undrain one or more nodes.
        """
        return self.drain(
            nodes=nodes,
            wlms=wlms,
            queues=queues,
            drain=False,
        )

    def drain_wait(self, nodes: list[Node | UUID], interval: int = 60, timeout: int | None = None) -> bool:
        """
        Wait for a set of nodes to be completely drained
        Returns false if the timeout was reached
        """
        drain_status_waiter = DrainStatusWaiter(self.cluster, nodes)
        self.cluster._status_waiters.append(drain_status_waiter)
        return drain_status_waiter.wait(interval, timeout)

    def drain_status_kube(self, nodes: list[Node | UUID]):
        """
        Get the workload managers drain status for one or more nodes.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmkube',
            call='drainOverview',
            args=[self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return [DrainResult(self.cluster, it) for it in out]

    def drain_kube(
        self,
        nodes: list[Node | UUID],
        add_actions: list[MonitoringAction | UUID] | None = None,
        remove_actions: list[MonitoringAction | UUID] | None = None,
        clear_actions: bool = False,
        drain: bool = True,
    ):
        """
        Drain one or more nodes in workload managers.
        """
        if add_actions is None:
            add_actions = []
        if remove_actions is None:
            remove_actions = []
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmkube',
            call='drainNodes',
            args=[
                self.cluster._entities_to_uuids(nodes),
                drain,
                add_actions,
                remove_actions,
                clear_actions,
            ],
        )
        if code:
            raise OSError(out)
        return [DrainResult(self.cluster, it) for it in out.get('results', [])]

    def undrain_kube(self, nodes: list[Node | UUID]):
        """
        Undrain one or more nodes.
        """
        return self.drain_kube(nodes=nodes, drain=False)

    def terminate(self, nodes: list[Node | UUID]):
        """
        Terminate one or more cloud nodes.
        """
        cloud_nodes = []
        for node in nodes:
            if isinstance(node, UUID):
                node = self.cluster.get_by_uuid(node)
            if isinstance(node, CloudNode):
                cloud_nodes.append(node)
        out_cloud = None
        out_virtual = None
        if cloud_nodes:
            rpc = self.cluster.get_rpc()
            (code, out_cloud) = rpc.call(
                service='cmcloud',
                call='terminate',
                args=[self.cluster._entities_to_uuids(cloud_nodes)],
            )
            if code:
                raise OSError(out_cloud)
        return out_cloud, out_virtual

    def connectivity(
        self,
        nodes: list[Node | UUID],
        count: int = 1,
        delay: float = 1.0,
        ping_timeout: float = 1.0,
        global_timeout: float = 350.0,
    ):
        """
        Terminate one or more cloud nodes.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='parallelPingAllToAll',
            args=[
                self.cluster._entities_to_uuids(nodes),
                count,
                int(delay * 1000),
                int(ping_timeout * 1000),
                int(global_timeout * 1000),
            ],
        )
        if code:
            raise OSError(out)
        return [PingResult(self.cluster, it) for it in out]

    def burn_start(
        self,
        nodes: list[Node | UUID],
        drain: bool = True,
        undrain: bool = True,
        information: str = "",
        configuration: [BurnConfig | str | UUID | None] = None,
    ) -> list[bool]:
        """
        Start a burn on a set of nodes
        """
        if not bool(nodes):
            return []
        if isinstance(configuration, BurnConfig):
            configuration = configuration.uuid
        elif isinstance(configuration, str):
            for it in self.cluster.get_base_partition().burnConfigs:
                if name_compare(it.name, configuration):
                    configuration = it.uuid
                    break
            else:
                # If no `break` in cycle - `else` will be executed
                raise LookupError(f"Unable to find burn config: {configuration}")
        elif configuration is None:
            configuration = self.cluster.get_base_partition().defaultBurnConfig.uuid

        rpc = self.cluster.get_rpc()
        nodes = self.cluster._entities_to_uuids(nodes)
        (code, out) = rpc.call(
            service='cmdevice',
            call='requestBurn',
            args=[nodes, drain, undrain, information, configuration],
        )
        if code:
            raise OSError(out)
        return [str(node) in out for node in nodes]

    def burn_stop(self, nodes: list[Node | UUID]) -> list[bool]:
        """
        Stop the burn on a set of nodes
        """
        rpc = self.cluster.get_rpc()
        nodes = self.cluster._entities_to_uuids(nodes)
        (code, out) = rpc.call(
            service='cmdevice',
            call='stopBurn',
            args=[nodes],
        )
        if code:
            raise OSError(out)
        return [str(node) in out for node in nodes]

    def burn_status(self, nodes: list[Node | UUID]):
        """
        Get the burn status for one or more nodes.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='getBurnStatus',
            args=[self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return [BurnStatus(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid'])) for it in out]

    def version_info(self, nodes: list[Node | UUID]) -> list[VersionInfo]:
        """
        Get the version information for one or more nodes.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmain',
            call='pgetVersion',
            args=[self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return [VersionInfo(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid'])) for it in out]

    def update_GNSS_location(self, nodes: list[Node | UUID]) -> list[bool]:
        """
        Asynchronously update the GNSS locations for one or more nodes.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmpart',
            call='pupdateGNSSLocation',
            args=[self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return out

    def routes(self, nodes: list[Node | UUID]):
        """
        Get the routes one or more nodes.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='proutes',
            args=[self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return [Route(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid'])) for it in out]

    def imex_ctl_node_status(self, nodes: list[Node | UUID]):
        """
        Get the routes one or more nodes.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='pimexCtlNode',
            args=[self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return [ImexCtlNode(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid'])) for it in out]

    def bios_apply(self, nodes: list[Node | UUID]) -> list[ExternalOperationResult]:
        """
        Apply the configured BIOS setup for one or more nodes.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='biosApply',
            args=[self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid']))
            for it in out
        ]

    def bios_check(self, nodes: list[Node | UUID]) -> list[ExternalOperationResult]:
        """
        Check the configured BIOS setup matches the live version for one or more nodes.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='biosCheck',
            args=[self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid']))
            for it in out
        ]

    def bios_fetch(self, nodes: list[Node | UUID]) -> list[ExternalOperationResult]:
        """
        Fetch the live BIOS setup for one or more nodes.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='biosFetch',
            args=[self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid']))
            for it in out
        ]

    def firmware_info(self, nodes: list[Node | UUID]) -> list[FirmwareInfo]:
        """
        Get information on the available firmware files for one or more nodes.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='firmwareFileInfo',
            args=[self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return [FirmwareInfo(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid'])) for it in out]

    def firmware_repository_info(
        self,
        nodes: list[Node | UUID],
        debug: bool = False,
    ) -> list[ExternalOperationResult]:
        """
        Get information on the firmware files on the iLO repository for one or more nodes.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='firmwareRepositoryInfo',
            args=[self.cluster._entities_to_uuids(nodes), debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid']))
            for it in out
        ]

    def firmware_upload(
        self,
        nodes: list[Node | UUID],
        files: list[str],
        debug: bool = False,
    ) -> list[ExternalOperationResult]:
        """
        Upload firmware onto the iLO repository for one or more nodes
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='firmwareUpload',
            args=[self.cluster._entities_to_uuids(nodes), files, debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid']))
            for it in out
        ]

    def firmware_flash(
        self,
        nodes: list[Node | UUID],
        files: list[str],
        debug: bool = False,
    ) -> list[ExternalOperationResult]:
        """
        Flash firmware from the iLO repository for one or more nodes
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='firmwareFlash',
            args=[
                self.cluster._entities_to_uuids(nodes),
                files,
                debug,
            ],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid']))
            for it in out
        ]

    def firmware_status(
        self,
        nodes: list[Node | UUID],
        debug: bool = False,
    ) -> list[ExternalOperationResult]:
        """
        Get information on the firmware status for one or more nodes.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='firmwareStatus',
            args=[self.cluster._entities_to_uuids(nodes), debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid']))
            for it in out
        ]

    def firmware_remove(
        self,
        nodes: list[Node | UUID],
        files: list[str],
        debug: bool = False,
    ) -> list[ExternalOperationResult]:
        """
        Remove firmware from the iLO repository for one or more nodes
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='firmwareRemove',
            args=[self.cluster._entities_to_uuids(nodes), files, debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid']))
            for it in out
        ]

    def network_connections(
        self, nodes: list[Node | UUID], tcp: bool = True, udp: bool = True, tcp6: bool = True, udp6: bool = True
    ):
        """
        Get the network connections one or more nodes.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='pnetworkConnections',
            args=[tcp, udp, tcp6, udp6, self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return [NetworkConnection(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid'])) for it in out]

    def additional_information(
        self, nodes: list[Node | UUID], name: str | None = None, run_on_active_head_node: bool = False
    ):
        """
        Get the network connections one or more nodes.
        """
        command = '' if name is None else name
        rpc = self.cluster.get_rpc()
        if run_on_active_head_node:
            (code, out) = rpc.call(
                service='cmdevice',
                call='getAdditionalNodeInfoForNodes',
                args=[command, self.cluster._entities_to_uuids(nodes)],
            )
        else:
            (code, out) = rpc.call(
                service='cmdevice',
                call='pgetAdditionalNodeInfo',
                args=[command, self.cluster._entities_to_uuids(nodes)],
            )
        if code:
            raise OSError(out)
        if len(out) == 0:
            return None
        if name is None:
            return list({it for jt in out['path'] for it in jt.split(',')})
        result = []
        for node, path, stdout, stderr, exit_code in zip(
            nodes, out['path'], out['stdout'], out['stdout'], out['exit_code']
        ):
            result.append(
                {
                    'node': node,
                    'path': path,
                    'stdout': stdout,
                    'stderr': stderr,
                    'exit_code': exit_code,
                }
            )
        return result

    def get_all_installed_packages(self, nodes: list[Node | UUID], root: str = '') -> list[Package]:
        """
        Get all installed packages
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='pallPackages',
            args=[root, self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return [Package(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid'])) for it in out]

    def find_installed_packages(
        self,
        nodes: list[Node | UUID],
        names: str | list[str],
        root: str = '',
    ) -> list[Package]:
        """
        Find one or more installed packages
        """
        if isinstance(names, str):
            names = [names]
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='pgetPackages',
            args=[root, names, self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return [Package(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid'])) for it in out]

    def power_history(self, devices: list[UUID], last: bool = False) -> list[PowerOperationHistory]:
        """
        Get the power history for one or more devices.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='powerOperationHistory',
            args=[self.cluster._entities_to_uuids(devices), last],
        )
        if code:
            raise OSError(out)
        return [
            PowerOperationHistory(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def bmc_identify(self, nodes: list[Node | UUID], debug: bool = False) -> list[ExternalOperationResult]:
        """
        Identify nodes via the BMC led
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='bmcIdentify',
            args=[self.cluster._entities_to_uuids(nodes), True, debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def bmc_unidentify(self, nodes: list[Node | UUID], debug: bool = False) -> list[ExternalOperationResult]:
        """
        Unidentify nodes via the BMC led
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='bmcIdentify',
            args=[self.cluster._entities_to_uuids(nodes), False, debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def bmc_is_identified(self, nodes: list[Node | UUID], debug: bool = False) -> list[ExternalOperationResult]:
        """
        Check if nodes are indentfied via the BMC led
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='bmcIsIdentified',
            args=[self.cluster._entities_to_uuids(nodes), debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def bmc_reset(self, nodes: list[Node | UUID], debug: bool = False) -> list[ExternalOperationResult]:
        """
        Reset the BMC controller
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='bmcReset',
            args=[self.cluster._entities_to_uuids(nodes), debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def bmc_event_logs(self, nodes: list[Node | UUID], debug: bool = False) -> list[ExternalOperationResult]:
        """
        Get the event logs from a BMC controller
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='bmcEventLogs',
            args=[self.cluster._entities_to_uuids(nodes), debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def mig_enable(
        self, nodes: list[Node | UUID], gpus: list[int] | None = None, debug: bool = False
    ) -> list[ExternalOperationResult]:
        """
        Enable MIG
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='migEnable',
            args=[self.cluster._entities_to_uuids(nodes), [] if gpus is None else gpus, debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def mig_disable(
        self, nodes: list[Node | UUID], gpus: list[int] | None = None, debug: bool = False
    ) -> list[ExternalOperationResult]:
        """
        Disable MIG
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='migDisable',
            args=[self.cluster._entities_to_uuids(nodes), [] if gpus is None else gpus, debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def mig_status(self, nodes: list[Node | UUID], debug: bool = False) -> list[ExternalOperationResult]:
        """
        Get the current enabled/disabled status of MIG
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='migStatus',
            args=[self.cluster._entities_to_uuids(nodes), debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def mig_profoles(
        self, nodes: list[Node | UUID], gpus: list[int] | None = None, debug: bool = False
    ) -> list[ExternalOperationResult]:
        """
        Get MIG profiles
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='migProfiles',
            args=[self.cluster._entities_to_uuids(nodes), [] if gpus is None else gpus, debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def mig_apply(
        self,
        nodes: list[Node | UUID],
        gpus: list[int] | None = None,
        profiles: list[str] | None = None,
        debug: bool = False,
    ) -> list[ExternalOperationResult]:
        """
        Apply configured or supplied MIG profiles
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='migApply',
            args=[
                self.cluster._entities_to_uuids(nodes),
                [] if gpus is None else gpus,
                [] if profiles is None else profiles,
                debug,
            ],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def mig_clear(
        self, nodes: list[Node | UUID], gpus: list[int] | None = None, debug: bool = False
    ) -> list[ExternalOperationResult]:
        """
        Clear applied MIG profiles
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='migClear',
            args=[self.cluster._entities_to_uuids(nodes), [] if gpus is None else gpus, debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def mig_show(
        self, nodes: list[Node | UUID], gpus: list[int] | None = None, debug: bool = False
    ) -> list[ExternalOperationResult]:
        """
        Show applied MIG profiles
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='migShow',
            args=[self.cluster._entities_to_uuids(nodes), [] if gpus is None else gpus, debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def dpu_push_bfb(
        self, dpu_nodes: list[DPUNode | UUID], path: str, debug: bool = False
    ) -> list[ExternalOperationResult]:
        """
        Push a BFB to DPU nodes
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service="cmdevice",
            call="dpuPushBfb",
            args=[self.cluster._entities_to_uuids(dpu_nodes), path, debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def dpu_apply(self, dpu_nodes: list[DPUNode | UUID], debug: bool = False) -> list[ExternalOperationResult]:
        """
        Apply settings to DPU nodes
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service="cmdevice",
            call="dpuApply",
            args=[self.cluster._entities_to_uuids(dpu_nodes), debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def dpu_discover(self, dpu_nodes: list[DPUNode | UUID], debug: bool = False) -> list[ExternalOperationResult]:
        """
        Discover the basic info for DPU nodes
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service="cmdevice",
            call="dpuDiscover",
            args=[self.cluster._entities_to_uuids(dpu_nodes), debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def dpu_boot_order(self, dpu_nodes: list[DPUNode | UUID], debug: bool = False) -> list[ExternalOperationResult]:
        """
        Change the boot order of DPU nodes according to the DPU settings
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service="cmdevice",
            call="dpuBootOrder",
            args=[self.cluster._entities_to_uuids(dpu_nodes), debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def get_capi_node_versions(
        self, nodes: list[Node | UUID], keep_empty: bool = False
    ) -> dict[UUID, tuple[UUID, str]]:
        """
        Get CAPI versions for a list of nodes
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmkube',
            call='getCapiNodeVersions',
            args=[self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return {
            node: (kube, version)
            for node, kube, version in zip(nodes, out["kube_clusters"], out["versions"])
            if keep_empty or bool(version)
        }

    def initialize(self, devices: list[Device | UUID]) -> list[bool]:
        """
        Initialze the devices
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service="cmdevice",
            call="initialize",
            args=[self.cluster._entities_to_uuids(devices)],
        )
        if code:
            raise OSError(out)
        return out

    def set_mac_via_switch_port(
        self,
        devices: list[Device | UUID],
        dry_run: bool = False,
        force: bool = False,
        index: int = -1,
    ) -> list[tuple[bool, str]]:
        """
        Set the MAC of a device via switch port information

        index : the index in case the switch port has multiple MAC (-1: auto => allow only 1 switch port)
        """
        rpc = self._cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='setMacForDevicesViaSwitchPort',
            args=[self.cluster._entities_to_uuids(devices), dry_run, force, index],
        )
        if code:
            raise OSError(out)
        return list(zip(out.get('success'), out.get('result')))

    def nvsm_alerts(
        self, nodes: list[Node | UUID], start: int = 0, limit: int = 0, debug: bool = False
    ) -> list[ExternalOperationResult]:
        """
        Get the NVSM alerts
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service="cmdevice",
            call="nvsmAlerts",
            args=[self.cluster._entities_to_uuids(nodes), start, limit, debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def nvsm_versions(self, nodes: list[Node | UUID], debug: bool = False) -> list[ExternalOperationResult]:
        """
        Get the NVSM versions
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service="cmdevice",
            call="nvsmVersions",
            args=[self.cluster._entities_to_uuids(nodes), debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def nvsm_start_health_dump(
        self, nodes: list[Node | UUID], quick: bool = False, tags: list[str] | None = None, debug: bool = False
    ) -> list[ExternalOperationResult]:
        """
        Start a NVSM health dump
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service="cmdevice",
            call="nvsmHealth",
            args=[self.cluster._entities_to_uuids(nodes), quick, [] if tags is None else tags, debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def nvsm_stop_health_dump(self, nodes: list[Node | UUID], debug: bool = False) -> list[ExternalOperationResult]:
        """
        Stop a running NVSM health dump
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service="cmdevice",
            call="nvsmHealthStop",
            args=[self.cluster._entities_to_uuids(nodes), debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def nvsm_status_health_dump(self, nodes: list[Node | UUID], debug: bool = False) -> list[ExternalOperationResult]:
        """
        Get the NVSM health dump status
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service="cmdevice",
            call="nvsmHealthStatus",
            args=[self.cluster._entities_to_uuids(nodes), debug],
        )
        if code:
            raise OSError(out)
        return [
            ExternalOperationResult(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_device_uuid']))
            for it in out
        ]

    def nvsm_info_health_dump(
        self, nodes: list[Node | UUID], history: bool = False, debug: bool = False
    ) -> list[NVSMInfo]:
        """
        Get the NVSM health dump information
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service="cmdevice",
            call="nvsmInfo",
            args=[self.cluster._entities_to_uuids(nodes), history, debug],
        )
        if code:
            raise OSError(out)
        return [NVSMInfo(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid'])) for it in out]

    def get_device_power_config(self, nodes: list[Node | UUID] | None = None) -> list[dict[str, UUID | str | float]]:
        """
        Get all device power config
        """
        if nodes is None:
            nodes = self.cluster.get_by_type(Node)
        nodes = self.cluster._entities_to_uuids(nodes)
        data = [
            {
                "device": node,
                "kind": kind,
                "index": index,
                "power_limit": 0,
            }
            for node in nodes
            for kind in ("GPU", "CPU")
            for index in range(16)
        ]
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service="cmdevice",
            call="updateDevicePowerConfig",
            args=[data],
        )
        if code:
            raise OSError(out)
        return out

    def update_device_power_config(
        self, data: list[dict[str, UUID | str | float]]
    ) -> list[dict[str, UUID | str | float]]:
        """
        Update device power config

        Dict fields:
        * device: uuid
        * kind: CPU, DPU, GPU, NIC
        * index: relative index of the hardware inside the target node
        * power_limit (W)

        set power_limit to 0 to query only
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service="cmdevice",
            call="updateDevicePowerConfig",
            args=[data],
        )
        if code:
            raise OSError(out)
        return out

    def update_device_power_config_tuple(
        self, device_power_config: list[tuple[Node | UUID, str, int, float]]
    ) -> list[dict[str, UUID | str | float]]:
        """
        Update the node GPU config

        Fields:
        * node: uuid
        * kind: CPU, DPU, GPU, NIC
        * index: relative index of the hardware inside the target node
        * power_limit (W)

        set power_limit to 0 to query only
        """
        data = [
            {
                "device": node if isinstance(node, UUID | str) else node.uuid,
                "kind": kind,
                "index": index,
                "power_limit": power_limit,
            }
            for (node, kind, index, power_limit) in device_power_config
        ]
        return self.update_device_power_config(data)

    def update_device_power_config_uniform(
        self, nodes: list[Node | UUID], indexes: list[int] | None = None, power_limit: int = 0, kind: str = "GPU"
    ) -> list[dict[str, UUID | str | int]]:
        """
        Update the node GPU config

        * node: uuid
        * index: relative index of the hardware inside the target node
        * power_limit (W)
        * kind: CPU, GPU

        set power_limit to 0 to query only
        """
        if indexes is None:
            indexes = list(range(16))
        data = [
            {
                "device": node if isinstance(node, UUID | str) else node.uuid,
                "kind": kind,
                "index": index,
                "power_limit": power_limit,
            }
            for node in nodes
            for index in indexes
        ]
        return self.update_device_power_config(data)

    def get_gpu_workload_power_profile_names(self, nodes: list[Node | UUID]) -> dict[UUID, list[tuple[int, str]]]:
        """
        Get the GPU workload power profiles for a list of nodes
        """
        nodes = self.cluster._entities_to_uuids(nodes)
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service="cmdevice",
            call="pgetGpuWorkloadPowerProfileNames",
            args=[nodes],
        )
        if code:
            raise OSError(out)
        names = out.get("names", [])
        profiles = out.get("profiles", [])
        return {node: [(p, n) for p, n in zip(pp, nn)] for node, pp, nn in zip(nodes, profiles, names)}

    def get_gpu_workload_power_profiles(self, nodes: list[Node | UUID]) -> dict[UUID, list[tuple[int, list[int]]]]:
        """
        Get the GPU workload power profiles for a list of nodes
        """
        nodes = self.cluster._entities_to_uuids(nodes)
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service="cmdevice",
            call="pgetGpuWorkloadPowerProfileNames",
            args=[nodes],
        )
        if code:
            raise OSError(out)
        gpus = out.get("gpus", [])
        profiles = out.get("profiles", [])
        return {node: [(g, p) for g, p in zip(gg, pp)] for node, gg, pp in zip(nodes, gpus, profiles)}

    def set_gpu_workload_power_profiles(
        self, nodes: list[Node | UUID], gpus: list[int], profiles: list[int]
    ) -> list[tuple[UUID, int, str]]:
        """
        Set the GPU workload power profiles for a list of nodes
        """
        nodes = self.cluster._entities_to_uuids(nodes)
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service="cmdevice",
            call="psetGpuWorkloadPowerProfileNames",
            args=[nodes, gpus, profiles],
        )
        if code:
            raise OSError(out)
        results = out.get("result", [])
        messages = out.get("message", [])
        return [(node, result, message) for node, result, message in zip(nodes, results, messages)]

    def get_hardware_inventory_info(
        self,
        devices: list[Node | UUID],
        cached: bool = True,
        first: int = 0,
        limit: int = 0xFFFFFFFF,
    ) -> list[dict[str, UUID | str]]:
        """
        Get harware inventory info for a list of devices
        """
        devices = self.cluster._entities_to_uuids(devices)
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service="cmdevice",
            call="deviceHardwareInventoryInfo",
            args=[devices, cached, first, limit],
        )
        if code:
            raise OSError(out)
        return out

    def gpu_reset(self, nodes: list[Node | UUID], gpus: list[int] | None = None) -> list[list[bool]]:
        """
        Reset the GPUs
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='pgpuReset',
            args=[self.cluster._entities_to_uuids(nodes), [] if gpus is None else gpus],
        )
        if code:
            raise OSError(out)
        return out

    def lite_daemon_package_status(self, devices: list[Switch | LiteNode | UUID]) -> list[tuple[bool, str, str]]:
        """
        Get the status of cm-lite-daemon packages
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='liteDaemonPackagesStatus',
            args=[self.cluster._entities_to_uuids(devices)],
        )
        if code:
            raise OSError(out)
        return [
            {
                'device': device,
                'success': success,
                'stdout': stdout,
                'stderr': stderr,
            }
            for device, success, stdout, stderr in zip(devices, out['success'], out['stdout'], out['stdout'])
        ]

    def lite_daemon_install(
        self, devices: list[Switch | LiteNode | UUID], update: bool = True, force: bool = False
    ) -> list[tuple[bool, str, str]]:
        """
        Install/update cm-lite-daemon packages
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='liteDaemonInstall',
            args=[self.cluster._entities_to_uuids(devices), update, force],
        )
        if code:
            raise OSError(out)
        return [
            {
                'device': device,
                'success': success,
                'stdout': stdout,
                'stderr': stderr,
            }
            for device, success, stdout, stderr in zip(devices, out['success'], out['stdout'], out['stdout'])
        ]

    def lite_daemon_remove(self, devices: list[Switch | LiteNode | UUID]) -> list[tuple[bool, str, str]]:
        """
        Remove cm-lite-daemon packages
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='liteDaemonRemove',
            args=[self.cluster._entities_to_uuids(devices)],
        )
        if code:
            raise OSError(out)
        return [
            {
                'device': device,
                'success': success,
                'stdout': stdout,
                'stderr': stderr,
            }
            for device, success, stdout, stderr in zip(devices, out['success'], out['stdout'], out['stdout'])
        ]
