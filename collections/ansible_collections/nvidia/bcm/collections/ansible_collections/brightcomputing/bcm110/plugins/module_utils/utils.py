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

import copy
import functools
import json
import typing

from pythoncm.entity.entity import Entity
from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity as EntityMetaData
from pythoncm.entity_to_json_encoder import EntityToJSONEncoder


@functools.lru_cache
def non_relevant_entity_fields():
    non_relevant = [field.name for field in EntityMetaData().fields()] + ["ref_partition_uuid"]
    try:
        non_relevant.remove("extra_values")
    except ValueError:
        pass
    return non_relevant


def is_relevant_field(field: MetaDataField | str) -> bool:
    return getattr(field, "name", field) not in non_relevant_entity_fields()


def serialize_field(field_value, field, nested_object_resolver_func) -> typing.Any:
    value: typing.Any = None

    if field.kind == MetaData.Type.RESOLVE or field.kind == MetaData.Type.ENTITY:
        if field.vector:
            value = [nested_object_resolver_func(it) for it in field_value]
        else:
            value = nested_object_resolver_func(field_value)

    elif field.kind == MetaData.Type.ELEMENT_OF:
        if isinstance(field_value, (Entity, type(None))):
            value = nested_object_resolver_func(field_value)
        else:
            raise AssertionError(f"Unexpected field definition for field {field.name!r} {field_value}")

    elif field.kind == MetaData.Type.ENUM:
        value = field_value.name
    elif field.kind == MetaData.Type.JSON:
        value = json.dumps(field_value)
    else:
        value = field_value

    return value


def nested_object_resolver(nested_entity, field, minify, depth, include_id, for_update) -> typing.Any:
    if not nested_entity:
        return nested_entity

    if depth > 0:
        if not for_update:
            return entity_to_dict(
                nested_entity, minify=minify, depth=depth - 1, include_id=include_id, for_update=for_update
            )

        if field.kind in [MetaData.Type.RESOLVE, MetaData.Type.ELEMENT_OF]:
            if isinstance(nested_entity, Entity):
                return nested_entity.resolve_name
            return nested_entity
        return entity_to_dict(
            nested_entity, minify=minify, depth=depth - 1, include_id=include_id, for_update=for_update
        )

    if field.kind == MetaData.Type.RESOLVE:
        return Entity._convert_to_uuid(nested_entity)  # FIXME: find a better way.

    if field.kind == MetaData.Type.ENTITY:
        return {k: v for k, v in nested_entity.to_dict().items() if is_relevant_field(k)}

    if field.kind == MetaData.Type.ELEMENT_OF:
        return nested_entity.uuid

    if field.kind == MetaData.Type.ENUM:
        return nested_entity.name

    return nested_entity


def _get_field_name(field, field_value) -> str:
    """Get field name, optionally suffixed with type if it doesn't match instance."""
    return field.name if type(field_value).__name__ == field.instance else f"{field.name}_{type(field_value).__name__}"


def entity_to_dict(
    entity,
    minify: bool = False,
    depth: int = 10,
    include_id: bool = False,
    for_update: bool = False,
) -> dict[str, typing.Any] | Entity:
    """
    Convert entity to python dictionary
    """
    if not isinstance(entity, Entity):
        return entity

    data: dict[str, typing.Any] = {}

    relevant_fields = [field for field in entity.fields() if is_relevant_field(field)]

    for field in relevant_fields:
        field_value: typing.Any = getattr(entity, field.name, copy.copy(field.default))

        if minify and (field.default is not None) and field_value == field.default:
            continue

        nested_object_resolver_func = functools.partial(
            nested_object_resolver,
            field=field,
            minify=minify,
            depth=depth,
            include_id=False,
            for_update=for_update,
        )

        value: typing.Any = serialize_field(
            field_value=field_value,
            field=field,
            nested_object_resolver_func=nested_object_resolver_func,
        )

        if for_update and field.kind == MetaData.Type.ENTITY:
            if field.vector:
                if not field_value:
                    data[field.name] = []
                else:
                    for index, v in enumerate(field_value):
                        name: str = _get_field_name(field, v)
                        if name not in data:
                            data[name] = []
                        data[name].append(value[index])
            else:
                if field_value is not None:
                    data[_get_field_name(field, field_value)] = value
        else:
            data[field.name] = value

        if include_id:
            data["id"] = entity.uuid

    return data


def json_encode_entity(entity: typing.Optional[Entity] = None):
    return json.loads(json.dumps(entity.to_dict() if isinstance(entity, Entity) else {}, cls=EntityToJSONEncoder))


def load_json_parameter(value: typing.Any) -> typing.Any:
    if isinstance(value, (dict, type(None))):
        return value
    if isinstance(value, str) and value.strip() in ["null", "None", ""]:
        return None
    # (med): Might be safe to assume that `value` is JSON parseable; Ansible should have signaled it by this point.
    return json.loads(value)