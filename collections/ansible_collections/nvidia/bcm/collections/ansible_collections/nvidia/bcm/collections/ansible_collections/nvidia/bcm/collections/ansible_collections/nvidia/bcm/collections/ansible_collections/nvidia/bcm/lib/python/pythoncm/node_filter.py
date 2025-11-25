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

from pythoncm.entity.configurationoverlay import ConfigurationOverlay
from pythoncm.entity.headnode import HeadNode
from pythoncm.entity.node import Node
from pythoncm.entity.role import Role

if typing.TYPE_CHECKING:
    from pythoncm.cluster import Cluster


class NodeFilter:
    """
    Helper class to quickly find all nodes with a certain role
    """

    def __init__(self, cluster: Cluster):
        self.cluster = cluster

    def get(self, check_function: typing.Callable | None = None) -> list[tuple[Node, list[Role]]]:
        """
        Get the nodes with corresponding roles that match the check function
        """

        class State:
            def __init__(self):
                self.node_role_priority = {}

            def add(self, node: Node, role: Role, priority: int) -> None:
                find_node = self.node_role_priority.get(node, None)
                if find_node is None:
                    self.node_role_priority[node] = {type(role): (role, priority)}
                else:
                    find_role = find_node.get(type(role), None)
                    if find_role is None or find_role[1] < priority:
                        find_node[type(role)] = (role, priority)

            def get(self) -> list[tuple[Node, list[Role]]]:
                """
                Sorted to make sure the unit test
                """
                return [
                    (node, [role for _, (role, _) in role_types.items()])
                    for node, role_types in self.node_role_priority.items()
                ]

        state = State()
        categories = {}
        head_nodes = []
        for node in self.cluster.get_by_type(Node):
            for role in node.roles:
                if check_function is None or check_function(role):
                    state.add(node, role, Role.NODE_PRIORITY)
            if isinstance(node, HeadNode):
                head_nodes.append(node)
            elif node.category is not None:
                categories.setdefault(node.category, []).append(node)
                for role in node.category.roles:
                    if check_function is None or check_function(role):
                        state.add(node, role, Role.CATEGORY_PRIORITY)
        for overlay in self.cluster.get_by_type(ConfigurationOverlay):
            if not overlay.disabled:
                for role in overlay.roles:
                    if check_function is None or check_function(role):
                        for node in overlay.nodes:
                            state.add(node, role, overlay.priority)
                        for category in overlay.categories:
                            for node in categories.get(category, []):
                                state.add(node, role, overlay.priority)
                        if overlay.allHeadNodes:
                            for node in head_nodes:
                                state.add(node, role, overlay.priority)

        return state.get()
