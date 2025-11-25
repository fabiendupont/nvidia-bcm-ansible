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

from uuid import UUID

from pythoncm.entity.entity import Entity


class WillChange(Entity):
    @property
    def entity(self):
        return self._cluster.get_by_uuid(self.ref_entity_uuid)

    @property
    def message(self):
        if self.ref_entity_uuid != UUID(int=0):
            entity = self.entity
            if entity:
                return (
                    f'{self.ref_base_type} {entity.resolve_name} '
                    f'change {self.parameter}, '
                    f'auto change: {self.auto_change}'
                )

            return (
                f'{self.ref_base_type} ref_entity_uuid: {self.ref_entity_uuid} '
                f'change {self.parameter}, '
                f'auto change: {self.auto_change}'
            )
        if bool(self.parameter):
            return f'{self.ref_base_type} change {self.parameter}, auto change: {self.auto_change}'
        return f'{self.ref_base_type}, auto change: {self.auto_change}'
