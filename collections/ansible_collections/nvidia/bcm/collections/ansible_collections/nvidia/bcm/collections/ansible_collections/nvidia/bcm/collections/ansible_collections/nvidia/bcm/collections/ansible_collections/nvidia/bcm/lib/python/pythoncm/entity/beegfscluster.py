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

import re
import typing

from pythoncm.entity.entity import Entity

if typing.TYPE_CHECKING:
    from collections.abc import Sequence

    from pythoncm.cluster import Cluster
    from pythoncm.entity.node import Node
    from pythoncm.entity_converter import EntityConverter


NAME_RE = re.compile(r"^[a-zA-Z0-9_]+")


class BeeGFSCluster(Entity):
    def __init__(
        self,
        cluster: Cluster | None = None,
        data: dict[str, typing.Any] | None = None,
        service=None,
        converter: EntityConverter | None = None,
        parent: Entity | None = None,
        add_to_cluster: bool = True,
        create_sub_entities: bool = True,
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

        if real_data.get("mountpoint") is None and cluster is not None and real_data.get("name") is not None:
            if real_data.get("multiMode", True):
                real_data["mountpoint"] = f"/mnt/beegfs-{real_data['name']}"
            else:
                real_data["mountpoint"] = "/mnt/beegfs"

        super().__init__(
            cluster=cluster,
            data=real_data,
            service=service,
            converter=converter,
            parent=parent,
            add_to_cluster=add_to_cluster,
            create_sub_entities=create_sub_entities,
        )

    def __setattr__(self, attr: str, value: typing.Any) -> None:
        if attr in {"name", "mountpoint"}:
            if self._attr_is_set_and_committed(attr):
                raise TypeError(f"Attribute {attr} is read-only.")
            if attr == "name" and value and not NAME_RE.match(value):
                raise ValueError(f"{attr} {value!r} not match {NAME_RE.pattern!r}")
        elif attr == "multiMode" and self.is_committed:
            raise TypeError(f"Attribute {self.multiMode=} is read-only.")
        super().__setattr__(attr, value)

    def __delattr__(self, name: str) -> None:
        if name in {"name", "mountpoint"} and self._attr_is_set_and_committed(name):
            raise TypeError(f"Attribute {name} is read-only.")
        if name == "multiMode" and self.is_committed:
            raise TypeError(f"Attribute {self.multiMode=} is read-only.")
        super().__delattr__(name)

    def _get_nodes_with_role_name(self, role_name: str) -> Sequence[Node]:
        if self._cluster is None:
            return ()
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='CMBeeGFS',
            call=f'getBeeGFS{role_name.rsplit(":", maxsplit=1)[-1].capitalize()}NodeUuids',
            args=[self.uuid],
        )
        if code:
            raise OSError(out)
        return tuple(self._cluster.get_by_uuid(out))

    def get_helper_nodes(self) -> Sequence[Node]:
        return self._get_nodes_with_role_name("BeeGFS::Helper")

    def get_client_nodes(self) -> Sequence[Node]:
        return self._get_nodes_with_role_name("BeeGFS::Client")

    def get_management_nodes(self) -> Sequence[Node]:
        return self._get_nodes_with_role_name("BeeGFS::Management")

    def get_metadata_nodes(self) -> Sequence[Node]:
        return self._get_nodes_with_role_name("BeeGFS::Metadata")

    def get_storage_nodes(self) -> Sequence[Node]:
        return self._get_nodes_with_role_name("BeeGFS::Storage")

    def __repr__(self):
        return f"<{self.__class__.__name__}(name={self.name}) at 0x{id(self):X}>"
