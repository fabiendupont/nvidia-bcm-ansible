# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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

import json
import typing

from .inspect import entity_internal_fields
from .inspect import entity_meta_instance
from .inspect import expand_field_to_leaf_entites
from .inspect import get_meta_data_class
from .inspect import import_entity_meta
from .inspect import is_extra_value_enabled


def scaler_fn(entity, field):
    return getattr(entity, field.name)


def resolve_fn(entity, field):
    if field.vector:
        return [x.resolve_name for x in getattr(entity, field.name)]
    else:
        val = getattr(entity, field.name)
        if isinstance(val, str):
            return val
        return getattr(val, "resolve_name", None)


def entity_fn(entity, field):
    if field.vector:
        if hasattr(entity, field.name):
            return [EntityConverter().resolve_entity(x) for x in getattr(entity, field.name)]

        field_name_and_type = field.name.rsplit("_", 1)

        if len(field_name_and_type) == 2:
            field_name, field_type = field_name_and_type
        else:
            field_name, field_type = field_name_and_type[0], None

        return [
            EntityConverter().resolve_entity(x)
            for x in getattr(entity, field_name)
            if (x.__class__.__name__ == field_type)  # (med) Not sure about this at the moment.
        ]
    else:
        return EntityConverter().resolve_entity(getattr(entity, field.name))


def enum_fn(entity, field):
    return getattr(entity, field.name).name


def json_fn(entity, field):
    val = getattr(entity, field.name)
    return json.dumps(val)


def element_of_fn(entity, field):
    val = getattr(entity, field.name)
    return getattr(val, "resolve_name", None)


class EntityConverter:
    def _resolve_kind(self, field):
        meta_data = get_meta_data_class()

        types = {
            meta_data.Type.BOOL: "bool",
            meta_data.Type.INT: "int",
            meta_data.Type.UINT: "int",
            meta_data.Type.FLOAT: "float",
            meta_data.Type.STRING: "str",
            meta_data.Type.RESOLVE: "resolve",
            meta_data.Type.ENTITY: "entity",
            meta_data.Type.TIMESTAMP: "int",
            meta_data.Type.ENUM: "enum",
            meta_data.Type.ELEMENT_OF: "element_of",
            meta_data.Type.JSON: "json",
            meta_data.Type.UUID: "str",
        }

        kind = types[field.kind]
        return kind

    def _resolve_value(self, field):
        element_kind = self._resolve_kind(field)

        if element_kind in ["element_of"]:
            return element_of_fn

        if element_kind in ["enum"]:
            return enum_fn

        if element_kind in ["bool", "int", "float", "str"]:
            return scaler_fn

        if element_kind in ["json"]:
            return json_fn

        if element_kind in ["resolve"]:
            return resolve_fn

        if element_kind in ["entity"]:
            return entity_fn

        raise AssertionError(f"{element_kind} SHOULD BE GET TO HERE!!!")

    def _resolve_field(self, entity, field):
        resolver = self._resolve_value(field)
        value = resolver(entity, field)
        return (field.name, value)

    def resolve_entity(self, entity) -> typing.Optional[dict]:
        if entity is None:
            return None
        entity_meta = entity.meta
        internal_fields = entity_internal_fields()
        relevent_fields = [
            field
            for field in entity_meta.fields()
            if field.name not in internal_fields and not field.readonly and not field.internal
        ]

        non_leaf_entity_fields = [
            field
            for field in relevent_fields
            if field.kind == entity_meta.meta.Type.ENTITY and not entity_meta_instance(field.instance).leaf_entity
        ]

        expanded_entity_fields = []

        for non_leaf_entity_field in non_leaf_entity_fields:
            expanded_entity_fields.extend(expand_field_to_leaf_entites(non_leaf_entity_field))

        remaining_fields = [field for field in relevent_fields if field not in non_leaf_entity_fields]

        all_fields = remaining_fields + expanded_entity_fields
        entity_name = entity_meta.__class__.__name__
        if is_extra_value_enabled(entity_name):
            # TODO: must validate that extra_values is a valid entity attribute
            entity_meta = import_entity_meta("Entity")
            if extra_values_field := next(
                (
                    f
                    for f in entity_meta().fields()
                    if f.name
                    in [
                        "extra_values",
                    ]
                ),
                None,
            ):
                all_fields += [extra_values_field]
        d = dict()
        for field in all_fields:
            k, v = self._resolve_field(entity, field)
            d[k] = v
        return d