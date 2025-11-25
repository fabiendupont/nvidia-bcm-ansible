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

from pythoncm.entity import GuiSwitchOverview
from pythoncm.entity.device import Device

if typing.TYPE_CHECKING:
    from pythoncm.entity import ExternalOperationResult
    from pythoncm.entity.network import Network


class Switch(Device):
    def overview(self):
        """
        Get the switch overiew.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmgui',
            call='getSwitchOverview',
            args=[self.uuid],
        )
        if code:
            raise OSError(out)
        if out is None:
            return out
        return GuiSwitchOverview(self._cluster, out, self)

    @property
    def networks(self) -> list[Network]:
        """
        Get all networks on which the device is connected
        """
        if self.network:
            return [self.network]
        return []

    @property
    def network_ips(self) -> list[tuple[Network, str]]:
        """
        Get all networks on which the device is connected
        """
        if self.network:
            return [(self.network, self.ip)]
        return []

    def ib_available_versions(self) -> list[str]:
        """
        Get available IB versions
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='ibswitchList',
        )
        if code:
            raise OSError(out)
        names = out.get("names", [])
        error = out.get("error_message", None)
        if not bool(names) and bool(error):
            raise OSError(error)
        return names

    def ib_images(self) -> list[ExternalOperationResult]:
        """
        Get IB switch images
        """
        from pythoncm.entity import ExternalOperationResult

        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='pibswitchImages',
            args=[[self.uuid]],
        )
        if code:
            raise OSError(out)
        return [ExternalOperationResult(self._cluster, it, parent=self) for it in out]

    def ib_interfaces(self) -> list[ExternalOperationResult]:
        """
        Get IB switch interfaces
        """
        from pythoncm.entity import ExternalOperationResult

        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='pibswitchInterfaces',
            args=[[self.uuid]],
        )
        if code:
            raise OSError(out)
        return [ExternalOperationResult(self._cluster, it, parent=self) for it in out]

    def ib_upgrade(self, version: str) -> list[ExternalOperationResult]:
        """
        Upgrade IB switch to the supplied version
        """
        from pythoncm.entity import ExternalOperationResult

        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='pibswitchUpgrade',
            args=[[self.uuid], version],
        )
        if code:
            raise OSError(out)
        return [ExternalOperationResult(self._cluster, it, parent=self) for it in out]

    def nv_config_apply(self, staged: bool = False, stage_only: bool = False) -> tuple[int, str, str]:
        rpc = self._cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='papplyDeviceCommands',
            args=[[self.uuid], staged, stage_only],
        )
        if code:
            raise OSError(out)
        out = out[0]
        return out.get("exit_code", 0), out.get("stdout", ""), out.get("stderr", "")

    def nv_config_detach(self) -> tuple[int, str, str]:
        rpc = self._cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='pdetachDeviceCommands',
            args=[[self.uuid]],
        )
        if code:
            raise OSError(out)
        out = out[0]
        return out.get("exit_code", 0), out.get("stdout", ""), out.get("stderr", "")

    def nv_config_save(self) -> tuple[int, str, str]:
        rpc = self._cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='psaveDeviceCommands',
            args=[[self.uuid]],
        )
        if code:
            raise OSError(out)
        out = out[0]
        return out.get("exit_code", 0), out.get("stdout", ""), out.get("stderr", "")

    def nv_config_show(self) -> str:
        rpc = self._cluster.get_rpc()
        code, out = rpc.call(
            service='cmdevice',
            call='pshowDeviceCommandsYAML',
            args=[[self.uuid]],
        )
        if code:
            raise OSError(out)
        return out.get("yaml", [""])[0]

    def lite_daemon_package_status(self) -> list[tuple[bool, str, str]] | None:
        """
        Get the status of cm-lite-daemon packages
        """
        result = self._cluster.parallel.lite_daemon_package_status([self])
        if bool(result):
            return result[0]
        return None

    def lite_daemon_install(self, update: bool = True, force: bool = False) -> list[tuple[bool, str, str]] | None:
        """
        Install/update cm-lite-daemon packages
        """
        result = self._cluster.parallel.lite_daemon_install([self])
        if bool(result):
            return result[0]
        return None

    def lite_daemon_remove(self) -> list[tuple[bool, str, str]] | None:
        """
        Remove cm-lite-daemon packages
        """
        result = self._cluster.parallel.lite_daemon_remove([self])
        if bool(result):
            return result[0]
        return None
