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

from pythoncm.entity import SlurmAccountingRole
from pythoncm.entity import SlurmClientRole
from pythoncm.entity import SlurmServerRole
from pythoncm.entity import SlurmSubmitRole
from pythoncm.entity import WlmCluster
from pythoncm.node_filter import NodeFilter

if typing.TYPE_CHECKING:
    from pythoncm.entity.node import Node


class SlurmWlmCluster(WlmCluster):
    @property
    def accounting_nodes(self) -> list[Node]:
        """
        List the nodes on which accounting is stored for this WLM
        """
        node_filter = NodeFilter(self._cluster)
        return [
            node
            for node, roles in node_filter.get(lambda role: isinstance(role, SlurmAccountingRole))
            if any(self in role.slurmWlmClusters for role in roles)
        ]

    @property
    def submit_nodes(self) -> list[Node]:
        """
        List the nodes on which jobs can be submitted for this WLM
        """
        node_filter = NodeFilter(self._cluster)
        return [
            node
            for node, roles in node_filter.get(lambda role: isinstance(role, SlurmSubmitRole))
            if any(access.wlmCluster == self for role in roles for access in role.slurmJobQueueAcccessList)
        ]

    @property
    def server_nodes(self) -> list[Node]:
        """
        List the nodes on which the WLM server runs
        """
        return self._find_by_single_role_wlm_reference(lambda role: isinstance(role, SlurmServerRole))

    @property
    def client_nodes(self) -> list[Node]:
        """
        List the nodes on which the WLM client runs
        """
        return self._find_by_single_role_wlm_reference(lambda role: isinstance(role, SlurmClientRole))
