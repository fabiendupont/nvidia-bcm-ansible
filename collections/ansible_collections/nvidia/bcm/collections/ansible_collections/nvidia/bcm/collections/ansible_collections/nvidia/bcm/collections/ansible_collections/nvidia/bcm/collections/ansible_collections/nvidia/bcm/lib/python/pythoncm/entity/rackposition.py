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

from pythoncm.entity.entity import Entity


class RackPosition(Entity):
    def same_tray(self, other: RackPosition) -> bool:
        if other is None:
            return False
        if self.meta.Tray.NONE in {other.tray, self.tray}:
            return False
        if (other.position != self.position) or (other.height != self.height) or (other.rack != self.rack):
            return False
        return other.tray != self.tray
