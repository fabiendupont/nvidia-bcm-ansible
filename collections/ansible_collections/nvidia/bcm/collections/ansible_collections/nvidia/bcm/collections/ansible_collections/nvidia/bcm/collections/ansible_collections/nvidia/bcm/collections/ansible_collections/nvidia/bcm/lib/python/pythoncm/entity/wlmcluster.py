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

from pythoncm.entity import Entity
from pythoncm.entity import JobQueue
from pythoncm.node_filter import NodeFilter

if typing.TYPE_CHECKING:
    from pythoncm.entity.node import Node


class WlmCluster(Entity):
    @property
    def accounting_nodes(self) -> list[Node]:
        """
        List the nodes on which accounting is stored for this WLM
        """
        return []

    @property
    def submit_nodes(self) -> list[Node]:
        """
        List the nodes on which jobs can be submitted for this WLM
        """
        return []

    @property
    def server_nodes(self) -> list[Node]:
        """
        List the nodes on which the WLM server runs
        """
        return []

    @property
    def client_nodes(self) -> list[Node]:
        """
        List the nodes on which the WLM client runs
        """
        return []

    @property
    def nodes(self) -> list[Node]:
        return list(set(self.submit_nodes + self.accounting_nodes + self.server_nodes + self.client_nodes))

    @property
    def job_queues(self) -> list[JobQueue]:
        return [job_queue for job_queue in self._cluster.get_by_type(JobQueue) if job_queue.wlmCluster == self]

    def _find_by_single_role_wlm_reference(self, roles_match_function: typing.Callable) -> list[Node]:
        node_filter = NodeFilter(self._cluster)
        return [
            node
            for node, roles in node_filter.get(roles_match_function)
            if any(role.wlmCluster == self for role in roles)
        ]

    def tracked_jobs(self) -> list[tuple[Node, str, list[str]]]:
        rpc = self._cluster.get_rpc()
        nodes = self.client_nodes
        code, out = rpc.call(
            service="cmjob",
            call="pgetTrackedJobs",
            args=[self.uuid, self._cluster._entities_to_uuids(nodes)],
        )
        if code:
            raise OSError(out)
        return list(zip(nodes, out.get("info", []), out.get("job_ids", [])))
