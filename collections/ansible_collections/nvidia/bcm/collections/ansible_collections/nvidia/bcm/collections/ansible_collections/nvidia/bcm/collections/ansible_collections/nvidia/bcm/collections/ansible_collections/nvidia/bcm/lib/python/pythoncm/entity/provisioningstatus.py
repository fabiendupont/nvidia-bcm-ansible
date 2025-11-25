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

from pythoncm.entity import ProvisioningNodeStatus
from pythoncm.entity import ProvisioningRequestStatus
from pythoncm.entity.entity import Entity


class ProvisioningStatus(Entity):
    def node_status(self, node):
        """
        Get the provisioning status for a specific node.
        """
        if isinstance(node, Entity):
            node = node.uuid
        try:
            status = next(it for it in self.provisioningNodeStatusList if it.node_uuid == node)
            return ProvisioningNodeStatus(self._cluster, status)
        except StopIteration:
            return None

    def get_request(self, request_uuid):
        """
        Get the provisioning status for a specific request.
        """
        try:
            status = next(it for it in self.provisioningRequestStatusList if request_uuid in it.request_uuids)
            return ProvisioningRequestStatus(self._cluster, status)
        except StopIteration:
            return None
