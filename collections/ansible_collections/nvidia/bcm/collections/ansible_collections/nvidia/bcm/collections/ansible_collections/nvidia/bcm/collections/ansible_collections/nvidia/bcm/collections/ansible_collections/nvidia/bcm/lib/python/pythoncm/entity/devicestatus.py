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


class DeviceStatus(Entity):
    @property
    def final_status(self) -> str:
        """
        Translate the status message in case of a closed device.
        """
        if self.closed:
            return 'CLOSED'
        return self.status

    @property
    def up(self) -> bool:
        """
        Determine if the node is UP and not closed
        """
        return not self.closed and self.status == self.meta.Status.UP

    @property
    def down(self) -> bool:
        """
        Determine if the node is DOWN
        """
        return self.status == self.meta.Status.DOWN

    @property
    def device(self) -> Device:
        """
        The device associated with this status
        """
        return self._cluster.get_by_uuid(self.ref_device_uuid)
