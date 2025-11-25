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

from pythoncm.entity.node import Node


class SystemInformationManager:
    """
    Helper class for easy overview of system information for all nodes
    """

    def __init__(self, cluster, auto_load=False, basic=False):
        self.cluster = cluster
        self.cache = None
        self.basic = basic
        if auto_load:
            self.load()

    def load(self, nodes=None):
        if nodes is None:
            nodes = self.cluster.get_by_type(instance_type=Node)
        self.cache = {it.ref_node_uuid: it for it in self.cluster.parallel.system_information(nodes)}

    def get(self, node, force_update=False):
        """
        Get the cached / live system information for a node.
        """
        if self.cache is None:
            raise ValueError('System information manager not loaded yet')
        if force_update:
            self.cache[node.uuid] = node.system_information(basic=self.basic)
        return self.cache.get(node.uuid, None)
