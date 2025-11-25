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

from pythoncm.entity.entity import Entity
from pythoncm.entity.metadata.devicestatus import DeviceStatus  # pylint: disable=import-error
from pythoncm.entity.metadata.poweroperation import PowerOperation  # pylint: disable=import-error

if typing.TYPE_CHECKING:
    from uuid import UUID

    from pythoncm.entity.bmcsettings import BMCSettings
    from pythoncm.entity.chassis import Chassis
    from pythoncm.entity.devicestatus import DeviceStatus as EDeviceStatus
    from pythoncm.entity.externaloperationresult import ExternalOperationResult
    from pythoncm.entity.firmwareinfo import FirmwareInfo
    from pythoncm.entity.network import Network
    from pythoncm.entity.networkinterface import NetworkInterface
    from pythoncm.entity.rack import Rack
    from pythoncm.entity.versioninfo import VersionInfo


class Device(Entity):
    def version_info(self) -> list[VersionInfo] | None:
        """
        Get cmdaemon version information.
        """
        info = self._cluster.parallel.version_info(nodes=[self])
        if len(info) == 1:
            return info[0]
        return None

    def status(self) -> EDeviceStatus:
        """
        Get the status for the device.
        """

        # CM-18430: load order issue
        from pythoncm.entity.devicestatus import DeviceStatus

        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmstatus',
            call='getStatus',
            args=[self.uuid],
        )
        if code:
            raise OSError(out)
        return DeviceStatus(self._cluster, out, parent=self)

    def wait_for_states(self, states, timeout=None):
        """
        Wait until the devices is in the desired state.
        """
        waiter = self._cluster.device_status_waiter_manager.create(self.uuid, states)
        return waiter.wait(timeout)

    def wait_for_up(self, timeout=None):
        """
        Wait for the device to be UP.
        """
        return self.wait_for_states(DeviceStatus.Status.UP, timeout)

    def wait_for_down_up(self, timeout=None):
        """
        Wait for the device to be DOWN and go UP after.
        """
        return self.wait_for_states([DeviceStatus.Status.DOWN, DeviceStatus.Status.UP], timeout)

    def wait_for_state_flag(self, field: str = "burning", value: bool = False, timeout=None):
        """
        Wait for the device state to have a field in the specified value
        """
        return self.wait_for_states(lambda it: getattr(it, field) == value, timeout)

    def _power_operation(self, operation, force=False, wait=False, timeout=None):
        return self._cluster.parallel._power_operation(
            devices=[self],
            operation=operation,
            force=force,
            wait=wait,
            timeout=timeout,
        )

    def power_status(self, force=False, wait=True, timeout=None):
        """
        Get the power status of the device.
        """
        return self._power_operation(
            operation=PowerOperation.Operation.STATUS,
            force=force,
            wait=wait,
            timeout=timeout,
        )

    def power_on(self, force=False, wait=False, timeout=None):
        """
        Power on the device.
        """
        return self._power_operation(
            operation=PowerOperation.Operation.ON,
            force=force,
            wait=wait,
            timeout=timeout,
        )

    def power_off(self, force=False, wait=False, timeout=None):
        """
        Power off the device.
        """
        return self._power_operation(
            operation=PowerOperation.Operation.OFF,
            force=force,
            wait=wait,
            timeout=timeout,
        )

    def power_reset(self, force=False, wait=False, timeout=None):
        """
        Power reset the device.
        """
        return self._power_operation(
            operation=PowerOperation.Operation.RESET,
            force=force,
            wait=wait,
            timeout=timeout,
        )

    def open(self, message=None):
        """
        Open the device.

        message: update the current status user message
        """
        result = self._cluster.parallel.open(devices=[self], message=message)
        if len(result) == 0:
            return None
        return result[0]

    def close(self, message=None):
        """
        Open the device.

        message: update the current status user message
        """
        result = self._cluster.parallel.close(devices=[self], message=message)
        if len(result) == 0:
            return None
        return result[0]

    def mute(self, message=None):
        """
        Mute the device, no more monitorring actions will be triggered

        message: update the current status user message
        """
        result = self._cluster.parallel.mute(devices=[self], message=message)
        if len(result) == 0:
            return None
        return result[0]

    def unmute(self, message=None):
        """
        Unmute the device.

        message: update the current status user message
        """
        result = self._cluster.parallel.unmute(devices=[self], message=message)
        if len(result) == 0:
            return None
        return result[0]

    def set_info_message(self, message: str):
        """
        Set the info message

        message: update the current status user message
        """
        result = self._cluster.parallel.set_info_message(devices=[self], message=message)
        if len(result) == 0:
            return None
        return result[0]

    def set_user_message(self, message: str):
        """
        Set the user message

        message: update the current status user message
        """
        result = self._cluster.parallel.set_user_message(devices=[self], message=message)
        if len(result) == 0:
            return None
        return result[0]

    def set_tool_message(self, message: str):
        """
        Set the tool message

        message: update the current status tool message
        """
        result = self._cluster.parallel.set_tool_message(devices=[self], message=message)
        if len(result) == 0:
            return None
        return result[0]

    def restart_required(self, reasons=None):
        """
        Set restart required for the device

        reasons: list of reasons, or single reason, restart is required
        """
        result = self._cluster.parallel.restart_required(devices=[self], reasons=reasons)
        if len(result) == 0:
            return None
        return result[0]

    def clear_restart_required(self):
        """
        Set restart required for the device

        message: update the current status user message
        """
        result = self._cluster.parallel.clear_restart_required(devices=[self])
        if len(result) == 0:
            return None
        return result[0]

    def power_history(self, last: bool = False):
        """
        Get the power history for the device

        message: update the current status user message
        """
        result = self._cluster.parallel.power_history(devices=[self], last=last)
        if last:
            if len(result) == 0:
                return None
            if len(result) == 1:
                return result[0]
        return result

    def get_last_tftpboot_file(self, path: str) -> tuple[int, bool, bool]:
        """
        Get the last fetch information for the /tftpboot service for a single file
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='getLastTftpbootFirmwareInformation',
            args=[str(self.uuid), path],
        )
        if code:
            raise OSError(out)
        return out.get('timestamp', 0), out.get('completed', False), out.get('success', False)

    def get_last_tftpboot_files(self) -> list[tuple[str, int, bool, bool]]:
        """
        Get the last fetch information for the /tftpboot service
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='getAllLastTftpbootFirmwareInformation',
            args=[str(self.uuid)],
        )
        if code:
            raise OSError(out)
        path = out.get('path', [])
        return list(
            zip(
                path,
                out.get('timestamp', [0] * len(path)),
                out.get('completed', [False] * len(path)),
                out.get('success', [False] * len(path)),
            )
        )

    def clear_tftpboot_file(self, path: str = '') -> tuple[int, int]:
        """
        Clear information for the /tftpboot service
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='clearTftpbootFirmwareInformation',
            args=[str(self.uuid), path],
        )
        if code:
            raise OSError(out)
        return out.get('servers', 0), out.get('files', 0)

    def initialize(self) -> bool | None:
        """
        Initialze the device
        """
        result = self._cluster.parallel.initialize(devices=[self])
        if len(result) == 0:
            return None
        return result[0]

    def set_mac_via_switch_port(
        self, dry_run: bool = False, force: bool = False, index: int = -1
    ) -> tuple[bool, str] | None:
        """
        Set the MAC of a device via switch port information

        index : the index in case the switch port has multiple MAC (-1: auto => allow only 1 switch port)
        """
        result = self._cluster.parallel.initialize(devices=[self])
        if len(result) == 0:
            return None
        return result[0]

    @property
    def chassis(self) -> Chassis | None:
        """
        Get the rack in which this device is part of
        """
        if self.chassisPosition is None:
            return None
        return self.chassisPosition.chassis

    @property
    def rack(self) -> Rack | None:
        """
        Get the rack in which this device is located
        """
        if self.rackPosition is not None:
            return self.rackPosition.rack
        if self.chassisPosition is not None:
            if self.chassisPosition.chassis is not None:
                return self.chassisPosition.chassis.rack
        return None

    def get_hardware_inventory_info(self, cached: bool = True) -> dict[str, UUID | str] | None:
        """
        Get harware inventory info for the device
        """
        result = self._cluster.parallel.get_hardware_inventory_info(devices=[self], cached=cached)
        if len(result) == 0:
            return None
        return result[0]

    def system_information(self, basic=False, add_empty=False):
        """
        Get the system information.
        """
        result = self._cluster.parallel.system_information(nodes=[self], basic=basic, add_empty=add_empty)
        if len(result) == 0:
            return None
        return result[0]

    def update_system_information(self):
        """
        Update the system information.
        This could take several seconds.
        """
        result = self._cluster.parallel.update_system_information(nodes=[self])
        if len(result) == 0:
            return None
        return result[0]

    def update_GNSS_location(self) -> bool | None:
        """
        Asynchronously update the GNSS location
        """
        success = self._cluster.parallel.update_GNSS_location(nodes=[self])
        if len(success) == 1:
            return success[0]
        return None

    def bmc_settings(self) -> BMCSettings | None:
        for source in (self, self.get_category(), self.partition):
            if bool(source) and bool(source.bmcSettings) and source.bmcSettings.defined:
                return source.bmcSettings
        return None

    def bmc_identify(self, debug: bool = False) -> ExternalOperationResult | None:
        """
        Identify a node via the BMC led
        """
        result = self._cluster.parallel.bmc_identify(nodes=[self.uuid], debug=debug)
        if len(result):
            return result[0]
        return None

    def bmc_unidentify(self, debug: bool = False) -> ExternalOperationResult | None:
        """
        Unidentify a node via the BMC led
        """
        result = self._cluster.parallel.bmc_unidentify(nodes=[self.uuid], debug=debug)
        if len(result):
            return result[0]
        return None

    def bmc_is_identified(self, debug: bool = False) -> ExternalOperationResult | None:
        """
        Check if a node is ondentfied via the BMC led
        """
        result = self._cluster.parallel.bmc_is_identified(nodes=[self.uuid], debug=debug)
        if len(result):
            return result[0]
        return None

    def bmc_reset(self, debug: bool = False) -> ExternalOperationResult | None:
        """
        Reset the BMC controller
        """
        result = self._cluster.parallel.bmc_reset(nodes=[self.uuid], debug=debug)
        if len(result):
            return result[0]
        return None

    def bmc_event_logs(self, debug: bool = False) -> ExternalOperationResult | None:
        """
        Get the event logs from a BMC controller
        """
        result = self._cluster.parallel.bmc_event_logs(nodes=[self.uuid], debug=debug)
        if len(result):
            return result[0]
        return None

    def firmware_info(self, debug: bool = False) -> list[FirmwareInfo]:
        """
        Get information on the available firmware files for one or more nodes.
        """
        return self._cluster.firmware_info(nodes=[self.uuid], debug=debug)

    def firmware_repository_info(self, debug: bool = False) -> ExternalOperationResult | None:
        """
        Get information on the firmware files on the iLO repository for one or more nodes.
        """
        result = self._cluster.firmware_repository_info(nodes=[self.uuid], debug=debug)
        if len(result):
            return result[0]
        return None

    def firmware_upload(self, files: list[str], debug: bool = False) -> ExternalOperationResult | None:
        """
        Upload firmware onto the iLO repository for one or more nodes
        """
        result = self._cluster.firmware_upload(nodes=[self.uuid], files=files, debug=debug)
        if len(result):
            return result[0]
        return None

    def firmware_flash(self, files: list[str], debug: bool = False) -> ExternalOperationResult | None:
        """
        Flash firmware from the iLO repository for one or more nodes
        """
        result = self._cluster.firmware_flash(nodes=[self.uuid], files=files, debug=debug)
        if len(result):
            return result[0]
        return None

    def firmware_status(self, debug: bool = False) -> ExternalOperationResult | None:
        """
        Get information on the firmware status for one or more nodes.
        """
        result = self._cluster.firmware_status(nodes=[self.uuid], debug=debug)
        if len(result):
            return result[0]
        return None

    def firmware_remove(self, files: list[str], debug: bool = False) -> ExternalOperationResult | None:
        """
        Remove firmware from the iLO repository for one or more nodes
        """
        result = self._cluster.firmware_remove(nodes=[self.uuid], files=files, debug=debug)
        if len(result):
            return result[0]
        return None

    @property
    def networks(self) -> list[Network]:
        """
        Get all networks on which the node has an interface
        """
        return [it.network for it in self.interfaces if it.network is not None]

    @property
    def network_ips(self) -> list[tuple[Network, str]]:
        """
        Get all network and IP on which the node has an interface
        """
        return [(it.network, it.ip) for it in self.interfaces if it.network is not None]

    @property
    def external_ip(self) -> str:
        """
        Get the most important IP on any external network
        """
        interface = self.external_interface
        if interface is not None:
            return interface.ip
        return '0.0.0.0'

    @property
    def external_headnode_ip(self) -> str:
        """
        Get the most important head node IP on any external network
        """
        ip = self.partition.externallyVisibleIp
        if ip == '0.0.0.0':
            # TODO: handle HA in some clean way
            active = self._cluster.active_head_node()
            ip = active.external_ip
        return ip

    @property
    def management_interface(self):
        """
        The management interface of the node
        The most important interface on the mangement network
        """
        management_network = self.management_network
        if management_network is None:
            return None
        interfaces = [it for it in self.interfaces if it.network == management_network]
        if len(interfaces) == 0:
            return None
        return max(interfaces, key=lambda it: it.onNetworkPriority)

    @property
    def internal_interface(self) -> NetworkInterface:
        """
        Get the most important interface on any internal network (fallback to management interface)
        """
        from pythoncm.entity.metadata.network import Network as NetworkMeta

        internal_network_types = [
            NetworkMeta.Type.INTERNAL,
            NetworkMeta.Type.EDGE_INTERNAL,
            NetworkMeta.Type.CLOUD,
        ]
        interface = self.management_interface
        if interface is not None and interface.network.type in internal_network_types:
            return interface
        interfaces = [it for it in self.interfaces if it.network and it.network.type in internal_network_types]
        if not bool(interfaces):
            return interface
        return max(interfaces, key=lambda it: it.onNetworkPriority)

    @property
    def external_interface(self) -> NetworkInterface | None:
        """
        Get the most important interface on any external network
        """
        from pythoncm.entity.metadata.network import Network as NetworkMeta

        external_network_types = [
            NetworkMeta.Type.EXTERNAL,
            NetworkMeta.Type.EDGE_EXTERNAL,
        ]
        interfaces = [it for it in self.interfaces if it.network and it.network.type in external_network_types]
        if len(interfaces) == 0:
            return None
        return max(interfaces, key=lambda it: it.onNetworkPriority)
