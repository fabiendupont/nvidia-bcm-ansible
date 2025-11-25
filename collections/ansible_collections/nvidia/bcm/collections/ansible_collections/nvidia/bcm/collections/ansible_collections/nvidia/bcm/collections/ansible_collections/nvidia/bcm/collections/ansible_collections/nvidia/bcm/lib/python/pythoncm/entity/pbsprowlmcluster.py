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

from pythoncm.entity import PbsProClientRole
from pythoncm.entity import PbsProServerRole
from pythoncm.entity import PbsProSubmitRole
from pythoncm.entity import WlmCluster
from pythoncm.node_filter import NodeFilter

if typing.TYPE_CHECKING:
    from pythoncm.entity.node import Node


class PbsProWlmCluster(WlmCluster):
    @property
    def submit_nodes(self) -> list[Node]:
        """
        List the nodes on which jobs can be submitted for this WLM
        """
        node_filter = NodeFilter(self._cluster)
        return [
            node
            for node, roles in node_filter.get(lambda role: isinstance(role, PbsProSubmitRole))
            if any(self in role.pbsProWlmClusters for role in roles)
        ]

    @property
    def server_nodes(self) -> list[Node]:
        """
        List the nodes on which the WLM server runs
        """
        return self._find_by_single_role_wlm_reference(lambda role: isinstance(role, PbsProServerRole))

    @property
    def client_nodes(self) -> list[Node]:
        """
        List the nodes on which the WLM client runs
        """
        return self._find_by_single_role_wlm_reference(lambda role: isinstance(role, PbsProClientRole))
