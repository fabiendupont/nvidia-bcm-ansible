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

from pythoncm.entity import Group
from pythoncm.entity.entity import Entity


class User(Entity):
    def remove(self, wait_for_task=False, force=False, home_directory=False):
        """
        Remove the user.
        """
        return super().remove(wait_for_task, force, home_directory)

    @property
    def groups(self):
        return [group for group in self._cluster.get_by_type(Group) if self.name in group.members]
