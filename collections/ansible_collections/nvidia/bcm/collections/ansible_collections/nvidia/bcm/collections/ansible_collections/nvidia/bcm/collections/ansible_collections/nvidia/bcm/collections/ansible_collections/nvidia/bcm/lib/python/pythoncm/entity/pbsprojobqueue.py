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

from pythoncm.entity import PBSJobQueue
from pythoncm.node_filter import NodeFilter

if typing.TYPE_CHECKING:
    from pythoncm.entity.node import Node


class PbsProJobQueue(PBSJobQueue):
    @property
    def nodes(self) -> list[Node]:
        """
        List of nodes used by this job queue
        """
        from pythoncm.entity import PbsProClientRole

        node_filter = NodeFilter(self._cluster)
        return [
            node
            for node, roles in node_filter.get(lambda role: isinstance(role, PbsProClientRole))
            if any(role.wlmCluster == self.wlmCluster if role.allQueues else self in role.queues for role in roles)
        ]
