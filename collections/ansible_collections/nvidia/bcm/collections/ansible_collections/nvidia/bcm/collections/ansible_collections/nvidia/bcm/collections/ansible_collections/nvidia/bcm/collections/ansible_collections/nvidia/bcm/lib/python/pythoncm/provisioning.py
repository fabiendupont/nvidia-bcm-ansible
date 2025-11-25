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
import threading
import typing
from time import monotonic

from pythoncm.entity import ProvisioningRole
from pythoncm.entity.node import Node
from pythoncm.entity.provisioningstatus import ProvisioningStatus
from pythoncm.target_source_mapping import TargetSourceMapping
from pythoncm.util import convert_to_uuid

if typing.TYPE_CHECKING:
    from uuid import UUID

    from pythoncm.cluster import Cluster


class Provisioning:
    """
    Provisioning
    """

    def __init__(self, cluster: Cluster):
        self.cluster = cluster
        self.logger = logging.getLogger(__name__)
        self._condition = threading.Condition()
        self._watchers = 0
        self._source_nodes = set()
        self._destination_nodes = set()
        self._any_path = set()
        self._active_paths = set()
        self._active_requests = set()

    def status(self):
        """
        Get the status of the provisioning system.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='getProvisioningStatus',
            args=[[]],
        )
        if code:
            return OSError(out)
        return ProvisioningStatus(self.cluster, out)

    def drain(self, nodes):
        """
        Prevent nodes from performing future provisioning jobs.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='drainProvisioningNodes',
            args=[self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            return OSError(out)
        return out

    def undrain(self, nodes):
        """
        Allow nodes from performing future provisioning jobs.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='undrainProvisioningNodes',
            args=[self.cluster._entities_to_uuids(nodes)],
        )
        if code:
            return OSError(out)
        return out

    def _update_node_lists(self, status):
        self._active_requests = set()
        for it in status.provisioningRequestStatusList:
            self._active_requests.update(it.request_uuids)
        self._source_nodes = {
            it.sourceNode for it in status.provisioningRequestStatusList if it.sourceNode != self.cluster.zero_uuid
        }
        self._destination_nodes = {
            it.destinationNode
            for it in status.provisioningRequestStatusList
            if it.destinationNode != self.cluster.zero_uuid
        }
        self._active_paths = {
            it.sourcePath
            for it in status.provisioningRequestStatusList
            if self.cluster.zero_uuid not in {it.sourceNode, it.destinationNode}
        }
        source_path = {
            it.sourcePath
            for it in status.provisioningRequestStatusList
            if (
                it.sourceNode != self.cluster.zero_uuid
                if bool(it.sourcePath)
                else it.destinationNode != self.cluster.zero_uuid
            )
        }
        destination_path = {
            it.destinationPath
            for it in status.provisioningRequestStatusList
            if (
                it.sourceNode != self.cluster.zero_uuid
                if bool(it.destinationPath)
                else it.destinationNode != self.cluster.zero_uuid
            )
        }
        self._any_path = source_path | destination_path
        self.logger.info(
            "Update provisioning status, source nodes: %d, destination nodes: %d",
            len(self._source_nodes),
            len(self._destination_nodes),
        )

    def update(self):
        """
        Update the internal state from an event
        """
        self.logger.info("Update provisioning status due to event")
        with self._condition:
            if self._watchers == 0:
                return
        self._update()

    def start(self):
        """
        Update the internal state from an event
        """
        self.logger.info("Update provisioning status")
        self._watchers += 1
        self._update(False)

    def _update(self, notify=True):
        """
        Update the internal state from an event or after a long delay
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='getProvisioningStatus',
            args=[[]],
        )
        if code:
            return False
        status = ProvisioningStatus(self.cluster, out)
        if notify:
            with self._condition:
                self._update_node_lists(status)
                self._condition.notify_all()
                return None
        else:
            self._update_node_lists(status)
            return None

    def wait(
        self, nodes: list[str | UUID], timeout: float | None = None, source: bool = True, destination: bool = True
    ) -> bool:
        """
        Wait for a set of nodes to be finished with provisioning
        """
        if not bool(nodes) or (not source and not destination):
            return True
        nodes = set(convert_to_uuid(nodes))
        with self._condition:
            self.start()
            start_time = monotonic()
            time_left = timeout
            while (time_left is None) or (time_left > 0):
                if (not source or len(nodes & self._source_nodes) == 0) and (
                    not destination or len(nodes & self._destination_nodes) == 0
                ):
                    break
                maximum_wait = 120
                if time_left is not None:
                    maximum_wait = min(maximum_wait, time_left)
                if self._condition.wait(maximum_wait):
                    self._update(False)
                if time_left is not None:
                    time_left = timeout + start_time - monotonic()
            self._watchers -= 1
            return (time_left is None) or (time_left > 0)

    def wait_requests(self, requests: list[str | UUID], timeout: float | None = None) -> bool:
        """
        Wait for a set of requests to be finished with provisioning
        """
        if not bool(requests):
            return True
        requests = set(convert_to_uuid(requests))
        with self._condition:
            self.start()
            start_time = monotonic()
            time_left = timeout
            while (time_left is None) or (time_left > 0):
                if len(requests & self._active_requests) == 0:
                    break
                maximum_wait = 120
                if time_left is not None:
                    maximum_wait = min(maximum_wait, time_left)
                if self._condition.wait(maximum_wait):
                    self._update(False)
                if time_left is not None:
                    time_left = timeout + start_time - monotonic()
            self._watchers -= 1
            return (time_left is None) or (time_left > 0)

    def wait_path(self, path: str, timeout: float | None = None, include_pending: bool = True) -> bool:
        """
        Wait until there are no active provisioning requests using the specified path
        """
        with self._condition:
            self.start()
            start_time = monotonic()
            time_left = timeout
            while (time_left is None) or (time_left > 0):
                if (not include_pending and path not in self._active_paths) or (
                    include_pending and path not in self._any_path
                ):
                    break
                maximum_wait = 120
                if time_left is not None:
                    maximum_wait = min(maximum_wait, time_left)
                if self._condition.wait(maximum_wait):
                    self._update(False)
                if time_left is not None:
                    time_left = timeout + start_time - monotonic()
            self._watchers -= 1
            return (time_left is None) or (time_left > 0)

    def mapping(self, no_cache: bool = False):
        """
        Get the provisioning source, target node mapping.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='getAllProvisioningSourceDestinationPairs',
            args=[no_cache],
        )
        if code:
            raise OSError(out)
        return TargetSourceMapping(self.cluster, out['targetNodes'], out['provisioningNodes'])

    def trigger_scheduler(self):
        """
        Trigger a restart of provisioning scheduler
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='triggerMainLoopRestart',
        )
        if code:
            raise OSError(out)
        return out

    def update_provisioners(self, nodes=None, images=None, wait=False, timeout=None):
        """
        Update all images on the provisioning node.
        """
        if nodes is None:
            nodes = []
        else:
            nodes = self.cluster._entities_to_uuids(nodes)
        if images is None:
            images = []
        else:
            images = self.cluster._entities_to_uuids(images)
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='updateProvisioners',
            args=[nodes, images, self.cluster.session_uuid],
        )
        if code:
            raise OSError(out)
        if wait and (len(out) != self.cluster.zero_uuid):
            return self.wait(
                nodes=nodes,
                timeout=timeout,
                source=False,
                destination=True,
            )
        return out

    def nodes(self, only_up=False):
        nodes = [node for node in self.cluster.get_by_type(Node) if node.get_role(ProvisioningRole) is not None]
        if only_up and len(nodes) != self.cluster.zero_uuid:
            nodes = [status.parent for status in self.cluster.device_status(nodes) if status.up]
        return nodes
