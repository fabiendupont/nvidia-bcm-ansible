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

from pythoncm.singleton import Singleton

if typing.TYPE_CHECKING:
    from pythoncm.entity.metadata.entity import Entity as EntityMetaData


class MetaDataCache(metaclass=Singleton):
    """
    Helper class to load and cache entity metadata
    """

    def __init__(self, cluster=None):
        self.cluster = cluster
        self.logger = logging.getLogger(__name__)
        self._cache: dict[str, EntityMetaData] = {}

    def _get(self, instance_name: str) -> EntityMetaData | None:
        """
        Get the meta data for the specified entity.
        """
        if instance_name not in self._cache:
            try:
                module = __import__(
                    f'pythoncm.entity.metadata.{instance_name.lower()}',
                    globals(),
                    locals(),
                    [instance_name],
                    level=0,
                )
                instance = getattr(module, instance_name)()
            except Exception as e:
                self.logger.warning('Create of meta data %s failed, error: %s', instance_name, e)
                instance = None
            self._cache[instance_name] = instance

        return self._cache[instance_name]

    def get(self, name_or_type: str | type) -> EntityMetaData | None:
        from pythoncm.entity import Entity

        key = None

        try:
            if isinstance(name_or_type, str):
                key = name_or_type
            elif issubclass(name_or_type, Entity):
                key = name_or_type.__name__
        except TypeError:
            pass

        if not key:
            raise TypeError(
                f"{self.__class__.__name__} key should be a string or a subclass of Entity, not {name_or_type!r}"
            )
        return self._get(key)

    def __getitem__(self, name_or_type: str | type) -> EntityMetaData | None:
        return self.get(name_or_type)
