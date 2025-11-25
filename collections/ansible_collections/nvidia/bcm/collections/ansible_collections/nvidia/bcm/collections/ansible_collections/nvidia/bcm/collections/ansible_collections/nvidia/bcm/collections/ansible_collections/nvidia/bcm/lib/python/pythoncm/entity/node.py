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

import typing

from pythoncm.entity import GuiNodeOverview
from pythoncm.entity.device import Device

if typing.TYPE_CHECKING:
    from uuid import UUID

    from pythoncm.entity.category import Category
    from pythoncm.entity.configurationoverlay import ConfigurationOverlay
    from pythoncm.entity.externaloperationresult import ExternalOperationResult
    from pythoncm.entity.nodearchosinfo import NodeArchOSInfo
    from pythoncm.entity.nvsminfo import NVSMInfo
    from pythoncm.entity.package import Package
    from pythoncm.entity.role import Role


class Node(Device):
    SYNC_MODE_FULL = 0
    SYNC_MODE_SYNC = 1
    SYNC_MODE_UPDATE = 2
    SYNC_MODE_GRAB = 3
    SYNC_MODE_GRABNEW = 4
    SYNC_MODE_ANY = 0xFFFFFFFF

    def wait_for_provisioning(self, timeout=None, source=True, destination=True):
        """
        Wait for all provisioning tasks for this node to be completed
        """
        return self._cluster.provisioning.wait(
            nodes=[self.uuid],
            timeout=timeout,
            source=source,
            destination=destination,
        )

    def get_category(self) -> Category | None:
        """
        Get the category if it exists.
        """
        return getattr(self, 'category', None)

    @property
    def need_ramdisk(self) -> bool:
        return False

    def get_configuration_overlays(
        self, also_disabled: bool = False, also_to_be_removed: bool = False
    ) -> list[ConfigurationOverlay]:
        """
        Get all configuration overlays the node is a part of
        """

        # CM-18430: load order issue
        from pythoncm.entity.configurationoverlay import ConfigurationOverlay
        from pythoncm.entity.headnode import HeadNode

        return [
            it
            for it in self._cluster.get_by_type(ConfigurationOverlay, also_to_be_removed)
            if (
                also_disabled
                or (
                    not it.disabled
                    and (
                        (self in it.nodes)
                        or (it.allHeadNodes and isinstance(self, HeadNode))
                        or (self.get_category() in it.categories)
                    )
                )
            )
        ]

    def get_role(
        self,
        instance_type: type[Role],
        also_to_be_removed: bool = False,
    ) -> Role | None:
        return next(
            (role for role in self.get_all_roles(True, also_to_be_removed) if isinstance(role, instance_type)), None
        )

    def get_role_by_name(
        self,
        role_name: str,
        also_to_be_removed: bool = False,
    ) -> Role | None:
        return next(
            (role for role in self.get_all_roles(True, also_to_be_removed) if role.name.lower() == role_name.lower()),
            None,
        )

    @typing.overload
    def get_all_roles(
        self,
        roles_only: bool = True,
        also_to_be_removed: bool = False,
    ) -> list[Role]:
        """Get all roles."""

    @typing.overload
    def get_all_roles(
        self,
        roles_only: bool = False,
        also_to_be_removed: bool = False,
    ) -> dict[int, tuple[UUID, Category | Node | ConfigurationOverlay, Role]]:
        """Get all roles."""

    def get_all_roles(
        self,
        roles_only: bool = True,
        also_to_be_removed: bool = False,
    ) -> list[Role] | dict[int, tuple[UUID, Category | Node | ConfigurationOverlay, Role]]:
        """
        Get all roles
        """

        # CM-18430: load order issue
        from pythoncm.entity.role import Role

        category = self.get_category()
        if category is not None:
            role_priority = {
                it.unique_identifier(): (Role.CATEGORY_PRIORITY, self.category, it)
                for it in self.category.roles
                if also_to_be_removed or not it.to_be_removed
            }
        else:
            role_priority = {}

        role_priority.update(
            {
                it.unique_identifier(): (Role.NODE_PRIORITY, self, it)
                for it in self.roles
                if also_to_be_removed or not it.to_be_removed
            }
        )

        for overlay in self.get_configuration_overlays(also_to_be_removed=also_to_be_removed):
            for role in overlay.roles:
                if not also_to_be_removed and role.to_be_removed:
                    continue
                if (role.unique_identifier() in role_priority) and (
                    role_priority[role.unique_identifier()][0] > overlay.priority
                ):
                    continue
                role_priority[role.unique_identifier()] = (overlay.priority, overlay, role)

        if roles_only:
            return [role for (priority, source, role) in role_priority.values()]
        return role_priority

    def update_provisioner(self, images=None, wait=False, timeout=None):
        """
        Update all images on the provisioning node.
        """
        if images is None:
            images = []
        images = [self._convert_to_uuid(it) for it in images]
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='updateProvisioners',
            args=[[self.uuid], images, self._cluster.session_uuid],
        )
        if code:
            raise OSError(out)
        if wait and len(out) and any(it != str(self._cluster.zero_uuid) for it in out):
            return self.wait_for_provisioning(timeout=timeout, source=False, destination=True)
        return out

    def is_mounted(self, path: str = '/cm/shared') -> bool:
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='isMountOk',
            args=[path],
        )
        if code:
            raise OSError(out)
        return out

    def overview(self):
        """
        Get the node overview.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmgui',
            call='getNodeOverview',
            args=[self._cluster.session_uuid, self.uuid],
        )
        if code:
            raise OSError(out)
        if out is None:
            return out
        return GuiNodeOverview(self._cluster, out, self)

    def arch_os_info(self) -> NodeArchOSInfo | None:
        """
        Get the node overview.
        """

        # CM-18430: load order issue
        from pythoncm.entity.nodearchosinfo import NodeArchOSInfo

        rpc = self._cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='getNodeArchOSInfo',
            args=[self.uuid],
        )
        if code:
            raise OSError(out)
        if out is None:
            return out
        return NodeArchOSInfo(self._cluster, out, self)

    def accelerators(self):
        """
        Get the number accelerators
        """
        result = self._cluster.parallel.accelerators(nodes=[self])
        if len(result) == 0:
            return None
        return result[0][0]

    def reload_managers(self):
        """
        Reload the cmd entity managers on the nodes, use only when they are out of sync
        """
        result = self._cluster.parallel.reload_managers(nodes=[self])
        if len(result) == 0:
            return None
        return result[0]

    def monitoring_system_information(self):
        """
        Get the monitoring system information.
        """
        result = self._cluster.monitoring.system_information(nodes=[self])
        if len(result) == 0:
            return None
        return result[0]

    def reboot(self, run_pre_halt_operations=True, pre_halt_operations_timeout=300):
        """
        Reboot.
        """
        result = self._cluster.parallel.reboot(
            nodes=[self],
            run_pre_halt_operations=run_pre_halt_operations,
            pre_halt_operations_timeout=pre_halt_operations_timeout,
        )
        if len(result) == 0:
            return None
        return result.get(self, (False, None))

    def shutdown(self, run_pre_halt_operations=True, pre_halt_operations_timeout=300):
        """
        Shutdown.
        """
        result = self._cluster.parallel.shutdown(
            nodes=[self],
            run_pre_halt_operations=run_pre_halt_operations,
            pre_halt_operations_timeout=pre_halt_operations_timeout,
        )
        if len(result) == 0:
            return None
        return result.get(self, (False, None))

    def service_status(self, name=None):
        """
        Get the status of a service running on the node.
        """
        result = self._cluster.parallel.service_status(
            nodes=[self],
            name=name,
        )
        if name is None:
            return result
        if len(result) == 0:
            return None
        return result[0]

    def service_start(self, name, args=None):
        """
        Start a service on the node.
        """
        if args is None:
            args = []
        result = self._cluster.parallel.service_start(
            nodes=[self],
            name=name,
            args=args,
        )
        if len(result) == 0:
            return None
        return result[0]

    def service_stop(self, name, args=None):
        """
        Stop a service on the node.
        """
        if args is None:
            args = []
        result = self._cluster.parallel.service_stop(nodes=[self], name=name, args=args)
        if len(result) == 0:
            return None
        return result[0]

    def service_restart(self, name, args=None):
        """
        Restart a service on the node.
        """
        if args is None:
            args = []
        result = self._cluster.parallel.service_restart(nodes=[self], name=name, args=args)
        if len(result) == 0:
            return None
        return result[0]

    def service_reload(self, name, args=None):
        """
        Reload a service on the node.
        """
        if args is None:
            args = []
        result = self._cluster.parallel.service_reload(nodes=[self], name=name, args=args)
        if len(result) == 0:
            return None
        return result[0]

    def service_reset(self, name, args=None):
        """
        Reset the failed state of a service on the node.
        """
        if args is None:
            args = []
        result = self._cluster.parallel.service_reset(nodes=[self], name=name, args=args)
        if len(result) == 0:
            return None
        return result[0]

    def service_action(self, name, action, args=None):
        """
        Run a action on a service on the node.
        """
        if args is None:
            args = []
        result = self._cluster.parallel.service_action(
            nodes=[self],
            name=name,
            action=action,
            args=args,
        )
        if len(result) == 0:
            return

    def service_update(self, name: str, wait: bool = False) -> bool | None:
        """
        Update a service and request an event to be send in response on the node.
        """
        result = self._cluster.parallel.service_update(
            nodes=[self],
            name=name,
            wait=wait,
        )
        if len(result) == 0:
            return None
        return result[0]

    def execute(
        self,
        command,
        args=None,
        env=None,
        user=None,
        run_in_shell=True,
        stdin=None,
        merge_stdout_stderr=False,
        max_run_time=None,
        wait=True,
        timeout=None,
        info=None,
    ):
        """
        Execute a command on the node.

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
        (done, program_runner_status) = self._cluster.parallel.execute(
            nodes=[self],
            command=command,
            args=args,
            env=env,
            user=user,
            run_in_shell=run_in_shell,
            info=info,
            stdin=stdin,
            merge_stdout_stderr=merge_stdout_stderr,
            max_run_time=max_run_time,
            wait=wait,
            timeout=timeout,
        )
        if done:
            return (
                program_runner_status.get_output(self.uuid),
                program_runner_status.get_error(self.uuid),
            )
        return done, program_runner_status

    def drain_status(self, wlms=None):
        """
        Get the workload drain status.
        """
        return self._cluster.parallel.drain_status(nodes=[self], wlms=wlms)

    def drain(
        self,
        wlms=None,
        queues=None,
        add_actions=None,
        remove_actions=None,
        clear_actions=False,
        reason='',
    ):
        """
        Prevent the node from running future jobs.
        """
        return self._cluster.parallel.drain(
            nodes=[self],
            wlms=wlms,
            queues=queues,
            add_actions=add_actions,
            remove_actions=remove_actions,
            clear_actions=clear_actions,
            reason=reason,
        )

    def undrain(self, wlms=None, queues=None):
        """
        Allow the node from running future jobs.
        """
        return self._cluster.parallel.undrain(
            nodes=[self],
            wlms=wlms,
            queues=queues,
        )

    def drain_wait(self, interval: int = 60, timeout: int | None = None) -> bool:
        """
        Wait for a set of nodes to be completely drained
        Returns false if the timeout was reached
        """
        return self._cluster.parallel.drain_wait([self], interval, timeout)

    def drain_status_kube(self):
        """
        Get the workload drain status.
        """
        return self._cluster.parallel.drain_status_kube(nodes=[self])

    def drain_kube(
        self,
        add_actions=None,
        remove_actions=None,
        clear_actions=False,
    ):
        """
        Prevent the node from running future jobs.
        """
        return self._cluster.parallel.drain_kube(
            nodes=[self],
            add_actions=add_actions,
            remove_actions=remove_actions,
            clear_actions=clear_actions,
        )

    def undrain_kube(self):
        """
        Allow the node from running future jobs.
        """
        return self._cluster.parallel.undrain_kube(nodes=[self])

    def provisioning_rsync_log(self, path=False):
        """
        Get the provisioning rsync log.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='syncLog',
            args=[self.uuid, path],
        )
        if code:
            raise OSError(out)
        return out

    def provisioning_info(self):
        """
        Get all provisioning sources and targets.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='getExcludeList',
            args=[self.uuid, self.SYNC_MODE_ANY, ''],
        )
        if code:
            raise OSError(out)
        return list(zip(out['sourcePaths'], out['destinationPaths']))

    def provisioning_exclude_list(self, path='/', mode=SYNC_MODE_FULL):
        """
        Get the exclude list for a rsync target.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='getExcludeList',
            args=[self.uuid, mode, path],
        )
        if code:
            raise OSError(out)
        return out['excludeLists'][0]

    def routes(self):
        """
        Get the routes.
        """
        return self._cluster.parallel.routes(nodes=[self])

    def bios_apply(self) -> ExternalOperationResult | None:
        """
        Apply the configured BIOS setup
        """
        result = self._cluster.parallel.bios_apply(nodes=[self])
        if len(result):
            return result[0]
        return None

    def bios_check(self) -> ExternalOperationResult | None:
        """
        Check the configured BIOS setup matches the live version
        """
        result = self._cluster.parallel.bios_apply(nodes=[self])
        if len(result):
            return result[0]
        return None

    def bios_fetch(self) -> ExternalOperationResult | None:
        """
        Fetch the live BIOS setup
        """
        result = self._cluster.parallel.bios_apply(nodes=[self])
        if len(result):
            return result[0]
        return None

    def network_connections(self, tcp=True, udp=True, tcp6=True, udp6=True):
        """
        Get the network connections
        """
        return self._cluster.parallel.network_connections(
            nodes=[self],
            tcp=tcp,
            udp=udp,
            tcp6=tcp6,
            udp6=udp6,
        )

    def additional_information(self, name=None, run_on_active_head_node=False):
        """
        Get additional node information
        Specify None to get a list of all know commands
        """
        info = self._cluster.parallel.additional_information(
            nodes=[self],
            name=name,
            run_on_active_head_node=run_on_active_head_node,
        )
        if len(info) > 0:
            return info[0]
        return None

    def get_all_installed_packages(self, root: str = '') -> list[Package]:
        """
        Get all installed packages on the node
        """
        return self._cluster.parallel.get_all_installed_packages(nodes=[self], root=root)

    def find_installed_packages(
        self,
        names: str | list[str],
        root: str = '',
    ) -> list[Package]:
        """
        Find one or more installed packages on the node
        """
        return self._cluster.parallel.find_installed_packages(nodes=[self], names=names, root=root)

    @property
    def terminated(self) -> bool:
        return False

    def nvsm_alerts(self, start: int = 0, limit: int = 0, debug: bool = False) -> ExternalOperationResult | None:
        """
        Get the NVSM alerts
        """
        result = self._cluster.parallel.nvsm_alerts([self.uuid], start, limit, debug)
        if len(result):
            return result[0]
        return None

    def nvsm_versions(self, debug: bool = False) -> ExternalOperationResult | None:
        """
        Get the NVSM versions
        """
        result = self._cluster.parallel.nvsm_versions([self.uuid], debug)
        if len(result):
            return result[0]
        return None

    def nvsm_start_health_dump(
        self, quick: bool = False, tags: list[str] | None = None, debug: bool = False
    ) -> ExternalOperationResult | None:
        """
        Start a NVSM health dump
        """
        result = self._cluster.parallel.nvsm_start_health_dump([self.uuid], quick, tags, debug)
        if len(result):
            return result[0]
        return None

    def nvsm_stop_health_dump(self, debug: bool = False) -> ExternalOperationResult | None:
        """
        Stop a running NVSM health dump
        """
        result = self._cluster.parallel.nvsm_stop_health_dump([self.uuid], debug)
        if len(result):
            return result[0]
        return None

    def nvsm_status_health_dump(self, debug: bool = False) -> ExternalOperationResult | None:
        """
        Get the NVSM health dump status
        """
        result = self._cluster.parallel.nvsm_status_health_dump([self.uuid], debug)
        if len(result):
            return result[0]
        return None

    def nvsm_info_health_dump(self, history: bool = False, debug: bool = False) -> NVSMInfo | None:
        """
        Get the NVSM health dump information
        """
        result = self._cluster.parallel.nvsm_info_health_dump([self.uuid], history, debug)
        if len(result):
            return result[0]
        return None

    def nvdomain_nodes(self, all_gpus: bool = False) -> dict | None:
        """
        Get the NV domain information for the node
            all_gpus=True requires all GPU in the node to have the same domain
        """
        rpc = self._cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='getNVDomainInfoForNode',
            args=[self.uuid, all_gpus],
        )
        if code:
            raise OSError(out)
        return out

    def get_gpu_workload_power_profile_names(self) -> list[tuple[int, str]] | None:
        """
        Get the GPU workload power profiles for a list of nodes
        """
        mapping = self._cluster.parallel.get_gpu_workload_power_profile_names([self.uuid])
        return mapping.get(self.uuid, None)

    def get_gpu_workload_power_profiles(self) -> list[tuple[int, list[int]]] | None:
        """
        Get the GPU workload power profiles for a list of nodes
        """
        mapping = self._cluster.parallel.get_gpu_workload_power_profile_names([self.uuid])
        return mapping.get(self.uuid, None)

    def set_gpu_workload_power_profiles(self, gpus: list[int], profiles: list[int]) -> tuple[int, str]:
        """
        Set the GPU workload power profiles for a list of nodes
        """
        _, result, message = self._cluster.parallel.set_gpu_workload_power_profile_names([self.uuid], gpus, profiles)
        return (result, message)

    def gpu_reset(self, gpus: list[int] | None = None) -> list[bool] | None:
        """
        Reset the GPUs
        """
        result = self._cluster.parallel.gpu_reset(nodes=[self.uuid], gpus=gpus)
        if len(result):
            return result[0]
        return None
