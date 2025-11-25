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

import ipaddress
import typing

from pythoncm.entity import Entity

if typing.TYPE_CHECKING:
    from pythoncm.entity.device import Device
    from pythoncm.entity.node import Node


class Network(Entity):
    def valid_ips(
        self,
        include_base: bool = False,
        include_broadcast: bool = False,
        include_dynamic_range: bool = False,
        force_large_network: bool = False,
    ) -> set[str] | None:
        """
        Get the list of all IPs in the network
        """
        base = ipaddress.IPv4Address(self.baseAddress)
        if not base.is_unspecified and (self.netmaskBits >= 16 or force_large_network):
            ip_network = ipaddress.IPv4Network(f"{self.baseAddress}/{self.netmaskBits}")
            broadcast = ip_network.broadcast_address
            return {
                str(ip)
                for ip in ip_network
                if (include_base or ip != base)
                and (include_broadcast or ip != broadcast)
                and (include_dynamic_range or not self.inside_dynamic_range(ip))
            }
        return None

    @property
    def broadcast_address(self) -> ipaddress.IPv4Address | None:
        base = ipaddress.IPv4Address(self.baseAddress)
        if not base.is_unspecified:
            ip_network = ipaddress.IPv4Network(f"{self.baseAddress}/{self.netmaskBits}")
            return ip_network.broadcast_address
        return None

    def inside_dynamic_range(self, ip: ipaddress.IPv4Address | str) -> bool:
        if isinstance(ip, str):
            ip = ipaddress.IPv4Address(ip)
        start = ipaddress.IPv4Address(self.dynamicRangeStart)
        end = ipaddress.IPv4Address(self.dynamicRangeEnd)
        return not start.is_unspecified and not end.is_unspecified and (ip >= start) and (ip <= end)

    def dynamic_range_ips(self) -> set[str]:
        """
        Get the IPs in the dynamic range
        """
        dynamic_range = set()
        start = ipaddress.IPv4Address(self.dynamicRangeStart)
        end = ipaddress.IPv4Address(self.dynamicRangeEnd)
        if not start.is_unspecified and not end.is_unspecified:
            while start < end:
                dynamic_range.add(start)
                start += 1
        return dynamic_range

    def used_ips(self) -> set[str]:
        """
        Get the IPs used in the network
        """
        from pythoncm.entity.device import Device

        return {
            ip for device in self._cluster.get_by_type(Device) for network, ip in device.network_ips if network == self
        }

    @property
    def nodes(self) -> set[Node]:
        """
        Get the nodes that use the network
        """
        from pythoncm.entity.node import Node

        return {node for node in self._cluster.get_by_type(Node) for network, ip in node.network_ips if network == self}

    @property
    def devices(self) -> set[Device]:
        """
        Get the devices that use the network
        """
        from pythoncm.entity.device import Device

        return {
            device
            for device in self._cluster.get_by_type(Device)
            for network, ip in device.network_ips
            if network == self
        }

    def available_ips(self) -> set[str]:
        """
        Get the IPs that are not in used by devices and not part of the dynamic range
        """
        return self.valid_ips().difference(self.used_ips())

    def contains_ip(self, ip: str) -> bool:
        """
        Check if the supplied IP is part of the network range
        """
        base = ipaddress.IPv4Address(self.baseAddress)
        if not base.is_unspecified and self.netmaskBits > 0:
            ip_network = ipaddress.IPv4Network(f"{self.baseAddress}/{self.netmaskBits}")
            ip = ipaddress.IPv4Address(ip)
            return not ip.is_unspecified and ip in ip_network
        return False
