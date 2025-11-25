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

import time
import typing
import uuid

from pythoncm.entity.entity import Entity
from pythoncm.entity.metadata.network import Network as NetworkMetadata

if typing.TYPE_CHECKING:
    from pythoncm.entity.computenode import ComputeNode


class EdgeSite(Entity):
    def cleanup(self) -> list[ComputeNode | EdgeSite]:
        """
        Remove all nodes and the edge site itself
        """
        node_status = self._cluster.parallel.device_status(self.nodes)
        if any(it.up for it in node_status):
            raise ValueError('One or more nodes are still up')
        entities = [*self.nodes, self]
        return [it.remove() for it in entities]

    @property
    def director(self) -> ComputeNode | None:
        """
        Get the node which serves as active (or only) director for the edge site
        """
        directors = self.directors
        if len(directors) == 1:
            return directors[0]
        if len(directors) > 1:
            group = directors[0].ha_group
            if group is None:
                raise ValueError('Mutliple edge directors defined without an HA group')
            active_node = group.status().ref_active_node_uuid
            return next((it for it in directors if it.uuid == active_node), None)
        return None

    @property
    def worker_nodes(self) -> list[ComputeNode]:
        """
        Get the node which do not serve as director for the edge site
        """
        return [node for node in self.nodes if node not in self.directors]

    @property
    def external_network(self):
        return self.director.managementNetwork if self.director else None

    @property
    def internal_networks(self):
        all_nets = (
            iface.network
            for node in self.nodes
            for iface in node.interfaces
            if iface.network and iface.network.type == NetworkMetadata.Type.EDGE_INTERNAL
        )
        return list(set(all_nets))

    @property
    def directors(self) -> list[ComputeNode]:
        """
        Get the nodes which serves as director for the edge site
        """
        from pythoncm.entity import EdgeDirectorRole

        return [node for node in self.nodes if node.get_role(EdgeDirectorRole) is not None]

    @property
    def is_pre_staged(self) -> bool:
        """
        Check if the edge site has already been pre-staged
        """
        return any(it not in {'0', '-'} for it in self.preStageRequestID)

    def clear_pre_stage_request(self) -> bool:
        """
        Clear the pre-stage request, so it can be requested again
        """
        if not self.is_pre_staged:
            return False
        self.preStageRequestID = str(uuid.UUID(int=0))
        self.preStageRequestIDCreationTime = 0
        return True

    def request_pre_stage(self) -> bool:
        """
        Check if the edge site has already been pre-staged
        """
        if self.is_pre_staged:
            return False
        self.preStageRequestID = str(uuid.uuid4())
        self.preStageRequestIDCreationTime = int(time.time())
        return True
