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

if typing.TYPE_CHECKING:
    from pythoncm.entity.device import Device


class Rack(Entity):
    @property
    def all_devices(self) -> list[Device]:
        """
        Get all devices contained in the rack.
        """

        # CM-18430: load order issue
        from pythoncm.entity.device import Device

        return [
            device
            for device in self._cluster.get_by_type(Device)
            if device.rackPosition is not None and device.rackPosition.rack == self
        ]
