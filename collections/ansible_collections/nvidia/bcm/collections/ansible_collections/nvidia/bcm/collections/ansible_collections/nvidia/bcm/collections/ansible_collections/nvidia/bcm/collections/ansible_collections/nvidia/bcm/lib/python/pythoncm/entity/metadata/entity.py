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

from uuid import UUID

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField


class Entity:
    __slots__ = (
        "meta",
        "baseType",
        "childType",
        "service_type",
        "leaf_entity",
        "top_level",
        "add_to_cluster",
        "allow_commit",
    )

    zero_uuid = UUID(int=0)

    def __init__(self):
        self.meta = MetaData()
        self.meta.add(MetaDataField('uuid',
                                    MetaData.Type.UUID,
                                    readonly=True,
                                    default=self.zero_uuid))
        self.meta.add(MetaDataField('baseType',
                                    MetaData.Type.STRING,
                                    readonly=True,
                                    default=''))
        self.meta.add(MetaDataField('childType',
                                    MetaData.Type.STRING,
                                    readonly=True,
                                    default=''))
        self.meta.add(MetaDataField('revision',
                                    MetaData.Type.STRING,
                                    default=''))
        self.meta.add(MetaDataField('modified',
                                    MetaData.Type.BOOL,
                                    diff_type=MetaDataField.Diff.none,
                                    internal=True,
                                    default=False))
        self.meta.add(MetaDataField('is_committed',
                                    MetaData.Type.BOOL,
                                    diff_type=MetaDataField.Diff.none,
                                    internal=True,
                                    default=False))
        self.meta.add(MetaDataField('to_be_removed',
                                    MetaData.Type.BOOL,
                                    diff_type=MetaDataField.Diff.none,
                                    internal=True,
                                    default=False))
        self.meta.add(MetaDataField('extra_values',
                                    MetaData.Type.JSON,
                                    default=None))
        self.baseType = ''
        self.childType = ''
        self.service_type = None
        self.leaf_entity = None
        self.top_level = None
        self.add_to_cluster = True
        self.allow_commit = True

    def fields(self):
        return self.meta.fields
