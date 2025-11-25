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
    from pythoncm.entity_converter import EntityConverter


class Role(Entity):
    NODE_PRIORITY: int = 750
    CATEGORY_PRIORITY: int = 250

    def unique_identifier(self) -> str:
        """
        Most roles can only be assigned once. Because
        there are exceptions, the childType of a role
        can not always be used as a unique identifier
        """
        return self.childType

    def __get_name(self) -> str | None:
        for prefix in ("Kubernetes", "Docker", "Etcd", "BeeGFS", "PRS"):
            if self.childType.startswith(prefix):
                return f"{prefix}::{self.childType[len(prefix) : -4]}"
        if self.childType != "GenericRole":
            return self.childType[:-4]
        return None

    def _convert(
        self,
        data: dict[str, typing.Any],
        converter: EntityConverter | None = None,
    ) -> None:
        if isinstance(data, dict):
            if "name" not in data:
                name = self.__get_name()
                if name is not None:
                    data["name"] = name
        else:
            name = self.__get_name()
            if name is not None:
                data = {"name": name}
        super()._convert(data, converter)
