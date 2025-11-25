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
    from pythoncm.entity.beegfscluster import BeeGFSCluster
    from pythoncm.entity_converter import EntityConverter


class BeeGFSMetadataConfig(Entity):
    def __init__(
        self,
        cluster: Cluster | None = None,
        data: dict[str, typing.Any] | None = None,
        service=None,
        converter: EntityConverter | None = None,
        parent: Entity | None = None,
        add_to_cluster: bool = True,
        create_sub_entities: bool = True,
        *,
        beegfs_cluster: BeeGFSCluster | str | None = None,
        **kwargs: typing.Any,
    ) -> None:
        # meta is not allowed
        if "meta" in kwargs:
            raise TypeError(f"'meta' is an invalid keyword argument for {self.__class__.__name__}")

        # We need to resolve real data to process it correctly
        if data is None:
            real_data: dict[str, typing.Any] = kwargs
        else:
            real_data = data
            real_data.update(kwargs)

        super().__init__(
            cluster=cluster,
            data=real_data,
            service=service,
            converter=converter,
            parent=parent,
            add_to_cluster=add_to_cluster,
            create_sub_entities=create_sub_entities,
        )
        if beegfs_cluster is not None:
            if isinstance(beegfs_cluster, str) and cluster is None:
                raise ValueError('BeeGFSCluster lookup is impossible without PythonCM cluster connection')
            self.beegfs_cluster = beegfs_cluster

            if (
                not self.is_committed
                and real_data.get("dataDir") is None
                and self.beegfs_cluster is not None
                and self.beegfs_cluster.name
                and not self.beegfs_cluster.multiMode
            ):
                self.dataDir = f"/var/lib/beegfs/{self.beegfs_cluster.name}/metadata"

    @property
    def resolve_name(self) -> str:
        """
        Special case
        """
        if self._cluster is None:
            return f"{self.ref_beegfs_cluster_uuid} (PythonCM Cluster is not bound)"
        if (beegfs := self.beegfs_cluster) is not None:
            return beegfs.name
        return str(self.ref_beegfs_cluster_uuid)

    @property
    def beegfs_cluster(self) -> BeeGFSCluster | None:
        return self._cluster.get_by_uuid(self.ref_beegfs_cluster_uuid)

    @beegfs_cluster.setter
    def beegfs_cluster(self, new_cluster: BeeGFSCluster | str) -> None:
        from pythoncm.entity import BeeGFSCluster

        if isinstance(new_cluster, BeeGFSCluster):
            self.ref_beegfs_cluster_uuid = new_cluster.uuid
        elif (beegfs_cluster := self._cluster.get_by_name(new_cluster, 'BeeGFSCluster')) is not None:
            self.ref_beegfs_cluster_uuid = beegfs_cluster.uuid

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(beegfs_cluster={self.resolve_name}) at 0x{id(self):X}>"
