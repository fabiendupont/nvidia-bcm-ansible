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

import importlib
import logging

from pythoncm.entity.entity import Entity


class EntityConverter:
    """
    Helper class to convert raw dictionaries to pythoncm objects.
    """

    def __init__(self, cluster, service):
        self.cluster = cluster
        self.logger = logging.getLogger(__name__)
        self.service = service
        self.entity_module = importlib.import_module('pythoncm.entity')

    def create(self, instance_type, owner=None, create_sub_entities=False):
        data = {'childType': instance_type}
        return self.convert(data, owner, create_sub_entities)

    def convert(self, data, owner=None, create_sub_entities=False):
        """
        Convert a single dictionaries to a pythoncm entity.
        """
        if isinstance(data, Entity):
            return data
        if not isinstance(data, dict):
            return None
        instance_type = data.get('childType', None)
        if not instance_type:
            instance_type = data.get('baseType', None)
        if instance_type is None:
            return None
        try:
            return getattr(self.entity_module, instance_type)(
                data=data,
                cluster=self.cluster,
                service=self.service,
                parent=owner,
                converter=self,
                create_sub_entities=create_sub_entities,
            )
        except Exception as e:
            self.logger.warning('Create %s failed, error: %s', instance_type, e)
        return None

    def get_type_by_name(self, name, try_append_role=True):
        """
        Convert a case invariant name into a pythoncm class definition

        try_append_role: automatically append "Role" to name and try again
        """
        name = name.lower()
        try:
            return next(
                self.entity_module.__dict__[key]
                for key in self.entity_module.__dict__
                if str.isupper(key[0]) and key.lower() == name
            )
        except StopIteration:
            if try_append_role:
                return self.get_type_by_name(name + "role", False)
        return None
