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

from pythoncm.entity.entity import Entity

if typing.TYPE_CHECKING:
    from pythoncm.entity.computenode import CloudNode


class CloudProvider(Entity):
    @property
    def director(self) -> CloudNode:
        """
        Get the (first) node which serves as director for this provider
        """
        # CM-18430: load order issue
        from pythoncm.entity import CloudDirectorRole

        return next((node for node in self.all_nodes if node.get_role(CloudDirectorRole) is not None), None)

    @property
    def directors(self) -> list[CloudNode]:
        """
        Get all the nodes which serves as directors for this provider
        """
        # CM-18430: load order issue
        from pythoncm.entity import CloudDirectorRole

        return [node for node in self.all_nodes if node.get_role(CloudDirectorRole) is not None]

    @property
    def all_nodes(self) -> list[CloudNode]:
        """
        Get all cloud nodes defined in this provider
        """
        # CM-18430: load order issue
        from pythoncm.entity.cloudnode import CloudNode

        return [node for node in self._cluster.get_by_type(CloudNode) if node.provider == self]

    @property
    def cloud_nodes(self) -> list[CloudNode]:
        """
        Get the node which do not serve as director for this provider
        """
        return [node for node in self.all_nodes if node not in self.directors]
