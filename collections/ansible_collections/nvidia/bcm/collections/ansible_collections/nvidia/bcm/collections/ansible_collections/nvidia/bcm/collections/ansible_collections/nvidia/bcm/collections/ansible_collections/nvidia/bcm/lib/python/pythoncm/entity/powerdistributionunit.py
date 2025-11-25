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

from pythoncm.entity import GuiPDUOverview
from pythoncm.entity.device import Device

if typing.TYPE_CHECKING:
    from pythoncm.entity.network import Network


class PowerDistributionUnit(Device):
    def overview(self):
        """
        Get the power distribution unit overiew.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmgui',
            call='getPDUOverview',
            args=[self.uuid],
        )
        if code:
            raise OSError(out)
        if out is None:
            return out
        return GuiPDUOverview(self._cluster, out, self)

    @property
    def networks(self) -> list[Network]:
        """
        Get all networks on which the power distribution unit is connected
        """
        if self.network:
            return [self.network]
        return []

    @property
    def network_ips(self) -> list[tuple[Network, str]]:
        """
        Get all networks on which the power distribution unit is connected
        """
        if self.network:
            return [(self.network, self.ip)]
        return []
