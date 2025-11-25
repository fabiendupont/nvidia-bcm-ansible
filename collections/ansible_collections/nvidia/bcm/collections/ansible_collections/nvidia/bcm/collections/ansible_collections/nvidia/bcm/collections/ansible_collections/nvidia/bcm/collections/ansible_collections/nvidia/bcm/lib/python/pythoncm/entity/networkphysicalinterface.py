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
    from pythoncm.cluster import Cluster
    from pythoncm.entity_converter import EntityConverter


class NetworkPhysicalInterface(Entity):
    def __init__(
        self,
        cluster: Cluster | None = None,
        data: dict[str, typing.Any] | None = None,
        service=None,
        converter: EntityConverter | None = None,
        parent: Entity | None = None,
        add_to_cluster: bool = True,
        create_sub_entities: bool = True,
        **kwargs,
    ) -> None:
        # meta is not allowed
        if "meta" in kwargs:
            raise TypeError(f"'meta' is an invalid keyword argument for {self.__class__.__name__}")

        super().__init__(
            cluster=cluster,
            data=data,
            service=service,
            converter=converter,
            parent=parent,
            add_to_cluster=add_to_cluster,
            create_sub_entities=create_sub_entities,
            **kwargs,
        )
        if self.onNetworkPriority == 0:
            self.onNetworkPriority = 60
