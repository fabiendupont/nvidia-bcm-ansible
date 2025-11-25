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
import typing
from uuid import UUID

from pythoncm.entity.node import Node

if typing.TYPE_CHECKING:
    from pythoncm.entity import BurnConfig
    from pythoncm.entity.edgesite import EdgeSite
    from pythoncm.entity.softwareimage import SoftwareImage


LOGGER = logging.getLogger(__name__)


class ComputeNode(Node):
    def clone(self, cluster=None, add_to_cluster=True, clear_cloned=True):
        """
        Special clone function
        """
        cloned_node = super().clone(cluster, add_to_cluster, clear_cloned)
        if self.templateNode:
            cloned_node.fromTemplateNode = self.uuid
        return cloned_node

    def burn_start(
        self,
        drain: bool = True,
        undrain: bool = True,
        information: str = "",
        configuration: [BurnConfig | str | UUID | None] = None,
    ) -> bool:
        """
        Get the burn status
        """
        result = self._cluster.parallel.burn_start([self], drain, undrain, information, configuration)
        if len(result) == 0:
            return None
        return result[0]

    def burn_stop(self):
        """
        Get the burn status
        """
        result = self._cluster.parallel.burn_stop(nodes=[self])
        if len(result) == 0:
            return None
        return result[0]

    def burn_status(self):
        """
        Get the burn status
        """
        result = self._cluster.parallel.burn_status(nodes=[self])
        if len(result) == 0:
            return None
        return result[0]

    def image_update(self, dry_run=False, wait=False, timeout=None, include_paths=None, selections=None):
        """
        Update the running image on the node.
        """
        if include_paths is None:
            include_paths = []
        if selections is None:
            selections = []
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='imageUpdate',
            args=[
                [self.uuid],
                dry_run,
                self._cluster.session_uuid,
                include_paths,
                selections,
            ],
        )
        if code:
            raise OSError(out)
        if wait and bool(out) and out[0] != self._cluster.zero_uuid:
            self._cluster.provisioning.wait(
                [self.uuid],
                timeout=timeout,
                source=False,
                destination=True,
            )
        return out[0]

    def grab_image(
        self,
        image: SoftwareImage | str | UUID,
        dry_run=False,
        wait=False,
        timeout=None,
        include_paths=None,
        selections=None,
    ):
        """
        Grab the image from the node onto an image on the active head node
        """

        # CM-18430: load order issue
        from pythoncm.entity.softwareimage import SoftwareImage

        if include_paths is None:
            include_paths = []
        if selections is None:
            selections = []

        if image is None:
            raise ValueError('Image not specified')
        if isinstance(image, SoftwareImage):
            image = image.uuid
        elif isinstance(image, str):
            image_name = image
            image = self._cluster.get_by_name(image, SoftwareImage)
            if image is None:
                raise LookupError(f'Image {image_name!r} not found')
            image = image.uuid
        elif not isinstance(image, UUID):
            raise TypeError('Invalid image specified')
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='grabImage',
            args=[
                self.uuid,
                image,
                dry_run,
                self._cluster.session_uuid,
                include_paths,
                selections,
            ],
        )
        if code:
            raise OSError(out)
        if wait and len(out) and any(it != str(self._cluster.zero_uuid) for it in out):
            return self.wait_for_provisioning(timeout=timeout, source=False, destination=True)
        return out

    @property
    def software_image(self) -> SoftwareImage | None:
        """
        Get the software image associated to this node
        """
        try:
            if self.softwareImageProxy is None or self.softwareImageProxy.software_image is None:
                if isinstance(self.category, UUID):
                    category = self._cluster.get_by_uuid(self.category)
                else:
                    category = self.category
                if category is None:
                    return None
                return category.software_image
            return self.softwareImageProxy.software_image
        except AttributeError as e:
            LOGGER.error(str(e), exc_info=True)
            raise

    @software_image.setter
    def software_image(self, image: SoftwareImage | None) -> None:
        """
        Set or clear the software image associated to this node
        """
        if image is None:
            if self.softwareImageProxy is not None:
                self.softwareImageProxy.remove()
        else:
            if self.softwareImageProxy is None:
                # CM-18430: load order issue
                from pythoncm.entity.softwareimageproxy import SoftwareImageProxy

                self.softwareImageProxy = SoftwareImageProxy(cluster=self._cluster)
            self.softwareImageProxy.software_image = image

    @property
    def need_ramdisk(self) -> bool:
        return (
            bool(self.kernelVersion)
            or bool(self.modules)
            or (self.softwareImageProxy is not None and self.softwareImageProxy.software_image is not None)
        )

    @property
    def ha_group(self):
        """
        Get the HA group the node belongs to
        """
        for group in self.partition.failoverGroups:
            if self in group.nodes:
                return group
        return None

    @property
    def management_network(self):
        """
        The management network of the node
        Fallback to category / partition management network
        """
        if self.managementNetwork:
            return self.managementNetwork
        if self.category and self.category.managementNetwork:
            return self.category.managementNetwork
        if self.partition:
            return self.partition.managementNetwork
        return None

    @property
    def edge_site(self) -> EdgeSite:
        """
        Return the edge site to which this node belongs
        """

        # CM-18430: load order issue
        from pythoncm.entity.edgesite import EdgeSite

        return next((it for it in self._cluster.get_by_type(EdgeSite) if self in it.nodes), None)

    @property
    def external_ip(self) -> str:
        """
        Get the most important IP on any external network
        Use the edge director role externally externally visible IP if set
        """

        # CM-18430: load order issue
        from pythoncm.entity import EdgeDirectorRole

        role = self.get_role(EdgeDirectorRole)
        if role is not None and role.externallyVisibleIp != '0.0.0.0':
            return role.externallyVisibleIp
        return super().external_ip

    @property
    def external_headnode_ip(self) -> str:
        """
        Get the most important head node IP on any external network
        Use the edge director role externally externally visible IP if set
        """

        # CM-18430: load order issue
        from pythoncm.entity import EdgeDirectorRole

        role = self.get_role(EdgeDirectorRole)
        if role is not None and role.externallyVisibleHeadNodeIp != '0.0.0.0':
            return role.externallyVisibleHeadNodeIp
        return super().external_headnode_ip
