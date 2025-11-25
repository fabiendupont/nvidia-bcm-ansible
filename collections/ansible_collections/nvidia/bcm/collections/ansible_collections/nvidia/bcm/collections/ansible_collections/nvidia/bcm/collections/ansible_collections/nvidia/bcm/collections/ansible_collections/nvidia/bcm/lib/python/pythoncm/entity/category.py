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
    from uuid import UUID

    from pythoncm.entity.computenode import ComputeNode
    from pythoncm.entity.configurationoverlay import ConfigurationOverlay
    from pythoncm.entity.role import Role
    from pythoncm.entity.softwareimage import SoftwareImage
    from pythoncm.entity.switch import Switch


class Category(Entity):
    def get_configuration_overlays(
        self,
        also_disabled: bool = False,
        also_to_be_removed: bool = False,
    ) -> list[ConfigurationOverlay]:
        """
        Get all configuration overlays the category is a part of
        """

        # CM-18430: load order issue
        from pythoncm.entity.configurationoverlay import ConfigurationOverlay

        return [
            it
            for it in self._cluster.get_by_type(ConfigurationOverlay, also_to_be_removed)
            if (also_disabled or (not it.disabled and self in it.categories))
        ]

    @property
    def software_image(self) -> SoftwareImage | None:
        """
        Get the software image associated to this category
        """
        if self.softwareImageProxy is None:
            return None
        return self.softwareImageProxy.software_image

    @software_image.setter
    def software_image(self, image: SoftwareImage):
        """
        Set the software image associated to this category
        """

        # CM-18430: load order issue
        from pythoncm.entity.softwareimageproxy import SoftwareImageProxy

        if self.softwareImageProxy is None:
            self.softwareImageProxy = SoftwareImageProxy(cluster=self._cluster)
        self.softwareImageProxy.software_image = image

    @property
    def nodes(self) -> list[ComputeNode]:
        """
        Get all nodes using this category
        """

        # CM-18430: load order issue
        from pythoncm.entity.computenode import ComputeNode

        return [node for node in self._cluster.get_by_type(ComputeNode) if node.category == self]

    @property
    def switches(self) -> list[Switch]:
        """
        Get all switches using this category
        """

        # CM-18430: load order issue
        from pythoncm.entity.switch import Switch

        return [it for it in self._cluster.get_by_type(Switch) if it.category == self]

    @property
    def devices(self) -> list[ComputeNode | Switch]:
        """
        Get all switches using this category
        """
        return self.nodes + self.switches

    @typing.overload
    def get_all_roles(
        self,
        roles_only: bool = True,
        also_to_be_removed: bool = False,
    ) -> list[Role]:
        """Get all roles."""

    @typing.overload
    def get_all_roles(
        self,
        roles_only: bool = False,
        also_to_be_removed: bool = False,
    ) -> dict[int, tuple[int, Category | ConfigurationOverlay, Role]]:
        """Get all roles."""

    def get_all_roles(
        self,
        roles_only: bool = True,
        also_to_be_removed: bool = False,
    ) -> list[Role] | dict[int, tuple[UUID, Category | ConfigurationOverlay, Role]]:
        """Get all roles."""

        # CM-18430: load order issue
        from pythoncm.entity.role import Role

        role_priority = {
            it.unique_identifier(): (Role.CATEGORY_PRIORITY, self, it)
            for it in self.roles
            if also_to_be_removed or not it.to_be_removed
        }

        for overlay in self.get_configuration_overlays(also_to_be_removed=also_to_be_removed):
            for role in overlay.roles:
                if not also_to_be_removed and role.to_be_removed:
                    continue
                if (role.unique_identifier() in role_priority) and (
                    role_priority[role.unique_identifier()][0] > overlay.priority
                ):
                    continue
                role_priority[role.unique_identifier()] = (overlay.priority, overlay, role)

        if roles_only:
            return [role for (priority, source, role) in role_priority.values()]
        return role_priority

    def get_role(
        self,
        instance_type: type[Role],
        also_to_be_removed: bool = False,
    ) -> Role | None:
        return next(
            (role for role in self.get_all_roles(True, also_to_be_removed) if isinstance(role, instance_type)), None
        )

    def get_role_by_name(
        self,
        role_name: str,
        also_to_be_removed=False,
    ) -> Role | None:
        return next(
            (role for role in self.get_all_roles(True, also_to_be_removed) if role.name.lower() == role_name.lower()),
            None,
        )
