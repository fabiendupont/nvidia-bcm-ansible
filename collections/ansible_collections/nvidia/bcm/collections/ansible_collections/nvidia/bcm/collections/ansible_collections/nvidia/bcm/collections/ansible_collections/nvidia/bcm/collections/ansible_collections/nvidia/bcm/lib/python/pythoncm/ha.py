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

from uuid import UUID

from pythoncm.entity import BlockingOperation
from pythoncm.entity import CMDaemonFailoverGroup
from pythoncm.entity import CMDaemonFailoverGroupStatus
from pythoncm.entity import CMDaemonFailoverStatus
from pythoncm.entity.node import Node


class HA:
    """
    High Availability.
    """

    def __init__(self, cluster):
        self.cluster = cluster

    @property
    def available(self) -> bool:
        """
        Check if HA is set up.
        """
        return self.cluster.passive_head_node() is not None

    def status(self) -> list[CMDaemonFailoverStatus]:
        """
        Get the current status of both headnodes in HA.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmpart',
            call='failoverFullStatus',
        )
        if code:
            raise OSError(out)
        return [CMDaemonFailoverStatus(self.cluster, it) for it in out]

    def switch_active(self) -> (bool, list[BlockingOperation]):
        """
        Perform a manual HA takeover
        """
        passive = self.cluster.passive_head_node()
        if passive is None:
            raise ValueError('No passive head node')
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmpart',
            call='failoverMakeActiveHeadNode',
            args=[passive.uuid],
        )
        if code:
            raise OSError(out)
        return out.get('success', False), [BlockingOperation(self.cluster, it) for it in out.get('operation', [])]

    def active_is_off(self) -> (bool, list[BlockingOperation]):
        """
        Inform the passive head node the active head node is really down.
        Make sure this is the case, otherwise this could lead to data corruption.
        """
        passive = self.cluster.passive_head_node()
        if passive is None:
            raise ValueError('No passive head node')
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmain',
            call='activeHeadNodeHasBeenManuallyPoweredOff',
        )
        if code:
            raise OSError(out)
        return out.get('success', False), [BlockingOperation(self.cluster, it) for it in out.get('operation', [])]

    def group_status(self) -> list[tuple[CMDaemonFailoverGroupStatus, CMDaemonFailoverGroup | None]]:
        """
        Get the status of all HA groups
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmpart',
            call='failoverGroupStatus',
        )
        if code:
            raise OSError(out)
        groups = {it.uuid: it for it in self.cluster.get_base_partition().failoverGroups}
        return [(CMDaemonFailoverGroupStatus(self, it), groups.get(UUID(it['uuid']), None)) for it in out]

    def group_switch_active(self, node: Node | int, force: bool = False) -> int:
        """
        Make the specified node active in the HA group
        """
        if isinstance(node, Node):
            key = node.uuid
        else:
            key = node
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmpart',
            call='cmdaemonGroupSwitchActive',
            args=[key, force],
        )
        if code:
            raise OSError(out)
        return out
