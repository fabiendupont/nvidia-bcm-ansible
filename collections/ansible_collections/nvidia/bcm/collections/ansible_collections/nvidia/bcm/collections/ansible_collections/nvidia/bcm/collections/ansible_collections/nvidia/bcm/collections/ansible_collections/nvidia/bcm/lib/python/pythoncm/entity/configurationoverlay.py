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

import logging
import typing
from uuid import UUID

from pythoncm.entity.entity import Entity

if typing.TYPE_CHECKING:
    from pythoncm.entity.node import Node
    from pythoncm.entity.role import Role


LOGGER = logging.getLogger(__name__)


class ConfigurationOverlay(Entity):
    MIN_PRIORITY = -1
    CATEGORY_PRIORITY = 250
    NODE_PRIORITY = 750
    MAX_PRIORITY = 1000

    @property
    def disabled(self):
        """
        Check if the configuration overlay is disabled.
        """
        return self.priority <= self.MIN_PRIORITY

    @property
    def valid_priority(self):
        """
        Check if the priority has a valid value.
        """
        return self.MIN_PRIORITY <= self.priority <= self.MAX_PRIORITY and self.priority not in {
            self.CATEGORY_PRIORITY,
            self.NODE_PRIORITY,
        }

    @property
    def all_nodes(self) -> list[Node]:
        """
        Get all nodes contained in the configuration overlay.
        """
        try:
            if self.disabled:
                return []
            categories = [it for it in self.categories if not isinstance(it, UUID)] + self._cluster.get_by_uuid(
                [it for it in self.categories if isinstance(it, UUID)]
            )
            nodes = set(self.nodes) | {node for category in categories for node in category.nodes}
            resolved = self._cluster.get_by_uuid([it for it in nodes if isinstance(it, UUID)])
            nodes = {it for it in nodes if not isinstance(it, UUID)}
            nodes.update(resolved)
            if self.allHeadNodes:
                from pythoncm.entity import HeadNode

                nodes.update(self._cluster.get_by_type(HeadNode))

            return list(nodes)
        except AttributeError as e:
            LOGGER.error(str(e), exc_info=True)
            raise

    def get_role(
        self,
        instance_type: type[Role],
        also_to_be_removed: bool = False,
    ) -> Role | None:
        for role in self.roles:
            if isinstance(role, instance_type) and (also_to_be_removed or not role.to_be_removed):
                return role

        return None

    def get_role_by_name(self, role_name: str, also_to_be_removed=False) -> Role | None:
        for role in self.roles:
            if role.name.lower() == role_name.lower() and (also_to_be_removed or not role.to_be_removed):
                return role
        return None
