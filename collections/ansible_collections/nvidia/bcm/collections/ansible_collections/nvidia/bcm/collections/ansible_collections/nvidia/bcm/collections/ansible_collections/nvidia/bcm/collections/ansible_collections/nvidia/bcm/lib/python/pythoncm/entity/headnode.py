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


class HeadNode(Node):
    @property
    def management_network(self):
        """
        The management network of the head node
        Always the partition management network
        """
        if self.partition:
            return self.partition.managementNetwork
        return None

    @property
    def external_ip(self) -> str:
        """
        Get the most important IP on any external network
        Use the partition externally visible IP if set
        """
        if self.partition and self.partition.externallyVisibleIp != '0.0.0.0':
            return self.partition.externallyVisibleIp
        return super().external_ip

    @property
    def is_active(self) -> bool:
        if not self._cluster:
            return False
        return self._cluster.active_head_node() == self

    @property
    def is_passive(self) -> bool:
        if not self._cluster:
            return False
        return self._cluster.passive_head_node() == self
