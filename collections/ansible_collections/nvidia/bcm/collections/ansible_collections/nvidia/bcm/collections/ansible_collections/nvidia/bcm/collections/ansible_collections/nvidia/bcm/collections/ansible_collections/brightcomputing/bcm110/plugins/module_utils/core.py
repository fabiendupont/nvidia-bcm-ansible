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

import lxml.etree
import pythoncm.entity
from box import Box
from deepdiff import DeepDiff
from deepdiff.path import GET
from deepdiff.path import GETATTR
from deepdiff.path import _get_nested_obj
from deepdiff.path import _path_to_elements
from deepdiff.path import extract
from pythoncm.cluster import Cluster
from pythoncm.commit_result import CommitResult
from pythoncm.entity import Entity
from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField

from .entity_converter import EntityConverter
from .utils import load_json_parameter

if typing.TYPE_CHECKING:
    from collections.abc import Callable
    from collections.abc import Iterable
    from typing import Literal

DiffType = MetaDataField.Diff

FAKE_SUCCESS_COMMIT_RESULT = CommitResult(cluster=None, success=True)


def setpath(obj, value, path: str | tuple[str, ...] | list[str], replace: bool = False) -> None:
    elements = _path_to_elements(path, root_element=None)
    obj = _get_nested_obj(obj, elements[:-1])
    elem, action = elements[-1]
    if action == GET:
        if isinstance(obj, list):
            if replace:
                obj.pop(elem)
            obj.insert(elem, value)
        else:
            obj[elem] = value
    elif action == GETATTR:
        setattr(obj, elem, value)


def delpath(obj, path: str | tuple[str, ...] | list[str]) -> None:
    elements = _path_to_elements(path, root_element=None)
    obj = _get_nested_obj(obj, elements[:-1])
    elem, action = elements[-1]

    assert isinstance(obj, (Entity, dict, list))

    field: typing.Optional[MetaDataField] = None
    if isinstance(obj, Entity):
        field = next(f for f in obj.fields() if f.name == elem)

    if action == GET:
        if isinstance(obj, (dict, list)):
            del obj[elem]
        else:
            setattr(obj, elem, copy.copy(field.default))  # type: ignore[union-attr]
    elif action == GETATTR:
        field = next(f for f in obj.fields() if f.name == "elem")
        setattr(obj, elem, copy.copy(field.field))


# TODO: this is horrible as well
def _get_nested_field(obj, elements: Iterable[tuple[str | typing.Any, str]]):
    field = None
    for elem, action in elements:
        if action == GETATTR or (action == GET and isinstance(elem, str)):
            fields = {field.name: field for field in obj.fields()}
            if elem in fields:
                fields = {field.name: field for field in obj.fields()}
                field = fields[elem]
                instance = field.instance
                if instance:
                    obj = getattr(pythoncm.entity, instance)()
            elif "_" in elem:
                field_name, field_type = elem.split("_", 1)
                field = fields[field_name]
                obj = getattr(pythoncm.entity, field_type)()
            else:
                # not sure what to do here!
                pass

    return field


def _getfield(obj, path: str | tuple[str, ...] | list[str]):
    assert isinstance(obj, Entity)
    elements = _path_to_elements(path, root_element=None)
    return _get_nested_field(obj, elements)


def _import_entity_class(name: str) -> type[Entity]:
    return getattr(pythoncm.entity, name)


def _create_diff(t1, t2, view: str) -> DeepDiff:
    return DeepDiff(t1, t2, ignore_order=True, view=view, verbose_level=2)


def extract_matching_keys(dict1, dict2, use_dict2_values=False):
    """
    Recursively extract elements from dict1 where the keys are present in dict2.
    Handles nested dictionaries and lists of dictionaries.

    Args:
        dict1: The source dictionary to extract from
        dict2: The dictionary containing the keys to match
        use_dict2_values: If True, use values from dict2 instead of dict1
                          If False (default), use values from dict1

    Returns:
        A new dictionary with the matching structure
    """
    result = {}

    for key, value in dict1.items():
        # Check if the key exists in dict2
        if key in dict2:
            # Handle nested dictionaries
            if isinstance(value, dict) and isinstance(dict2[key], dict):
                nested_result = extract_matching_keys(value, dict2[key], use_dict2_values)
                result[key] = nested_result

            # Handle lists that might contain dictionaries
            elif isinstance(value, list) and isinstance(dict2[key], list):
                # If we're using dict2 values and dict2's list is empty, keep it empty
                if use_dict2_values and len(dict2[key]) == 0:
                    result[key] = []
                    continue

                # If dict2's list is empty, keep the original items from dict1
                if len(dict2[key]) == 0:
                    result[key] = value
                    continue

                result_list = []

                # Process each item in the list
                for item in value:
                    if isinstance(item, dict):
                        # For lists of dictionaries, try to match with each dict in dict2's list
                        matched = False
                        for dict2_item in dict2[key]:
                            if isinstance(dict2_item, dict):
                                # Process dictionary within list
                                extracted = extract_matching_keys(item, dict2_item, use_dict2_values)
                                if extracted:
                                    result_list.append(extracted)
                                    matched = True
                                    break

                        # If dict2's list has dictionaries but no match found, use template approach
                        if not matched and any(isinstance(d, dict) for d in dict2[key]):
                            # Create a template dict with all possible keys from dict2's list items
                            template = {}
                            for d in dict2[key]:
                                if isinstance(d, dict):
                                    template.update(d)

                            # If template is empty but dict2 list accepts dictionaries, include item as is
                            if not template and any(isinstance(d, dict) for d in dict2[key]):
                                result_list.append(item)
                            else:
                                extracted = extract_matching_keys(item, template, use_dict2_values)
                                if extracted:
                                    result_list.append(extracted)
                    else:
                        # For non-dictionary items in the list, include them directly
                        result_list.append(item)

                result[key] = result_list

            else:
                # If it's not a nested dictionary or list, add the appropriate value
                result[key] = dict2[key] if use_dict2_values else value

    return result


class BaseDiffer:
    subclasses: dict[str, type] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        resolver = cls.__name__.removesuffix("_Differ")
        if resolver not in BaseDiffer.subclasses:
            BaseDiffer.subclasses[resolver] = cls

    def __init__(self, entity, param_name, param_value, diff_view) -> None:
        self.entity = entity
        self.param_name = param_name
        self.param_value = param_value
        self.diff_view = diff_view
        self.fields: dict[str, MetaDataField] = {field.name: field for field in entity.fields()}

        if "_" in param_name and param_name not in self.fields:
            self.attr_name, self.attr_type = param_name.split("_", 1)
        else:
            self.attr_name = param_name
            self.attr_type = None

    def diff(self):
        # TODO: should we complain?
        # NOTE: this can be the case for the state param.
        if self.attr_name not in self.fields:
            return None, None

        # NOTE: we don't care about transient fields in update
        # NOTE: we don't update non updatable fields
        # TODO: document those
        if self.fields[self.attr_name].diff_type in [DiffType.none, DiffType.disabled]:
            return None, self.fields[self.attr_name]

        return self._diff(), self.fields[self.attr_name]

    def _diff(self):
        field = self.fields[self.attr_name]
        differ_cls = BaseDiffer.subclasses.get(field.kind.name, _DEFAULT_Differ)
        differ = differ_cls(self.entity, self.param_name, self.param_value, self.diff_view)
        ddiff, _ = differ.diff()
        return ddiff


class ENTITY_Differ(BaseDiffer):
    def _diff_vector(self) -> DeepDiff:
        if self.attr_type:
            attr_values = self.entity[self.attr_name + "_" + self.attr_type]
        else:
            attr_values = self.entity[self.attr_name]

        attr_values_list: list[dict[str, typing.Any]] = []
        for index, attr_value in enumerate(attr_values):
            val = EntityConverter().resolve_entity(attr_value)
            try:
                val2 = extract_matching_keys(val, self.param_value[index])
                attr_values_list.append(val2)
            except IndexError:
                attr_values_list.append(val)  # type: ignore[arg-type]

        ddiff = _create_diff(attr_values_list, self.param_value, view=self.diff_view)
        return ddiff

    def _diff_one(self):
        entity_attr_value = self.entity[self.attr_name]
        if self.attr_type:
            if self.attr_type == type(entity_attr_value).__name__:
                entity_as_dict = EntityConverter().resolve_entity(entity_attr_value)
                if self.param_value is not None:
                    entity_as_dict = extract_matching_keys(entity_as_dict, self.param_value)

                ddiff = _create_diff(entity_as_dict, self.param_value, view=self.diff_view)
            else:
                ddiff = _create_diff(None, self.param_value, view=self.diff_view)
        else:
            entity_as_dict = EntityConverter().resolve_entity(entity_attr_value)

            if entity_as_dict and self.param_value is not None:
                # This needs to be done recursively.
                entity_as_dict = extract_matching_keys(entity_as_dict, self.param_value)
            ddiff = _create_diff(entity_as_dict, self.param_value, view=self.diff_view)
        return ddiff

    def _diff(self):
        if self.fields[self.attr_name].vector:
            return self._diff_vector()
        else:
            return self._diff_one()


class RESOLVE_Differ(BaseDiffer):
    def _diff(self):
        attr_name = self.attr_name
        if self.fields[attr_name].vector:
            attr_values = [resolve_attr.resolve_name for resolve_attr in self.entity[self.param_name]]
            ddiff = _create_diff(attr_values, self.param_value, view=self.diff_view)

        else:
            resolve_attr = self.entity[self.param_name]
            if resolve_attr:
                attr_value = resolve_attr.resolve_name
            else:
                attr_value = self.fields[attr_name].default or ""  # FIXME: not sure about this.
            ddiff = _create_diff(attr_value, self.param_value, view=self.diff_view)
        return ddiff


class ELEMENT_OF_Differ(BaseDiffer):
    def _diff(self):
        attr_name = self.attr_name
        resolve_attr = self.entity[self.param_name]
        if resolve_attr:
            attr_value = resolve_attr.resolve_name
        else:
            attr_value = self.fields[attr_name].default or ""  # FIXME: not sure about this.
        ddiff = _create_diff(attr_value, self.param_value, view=self.diff_view)
        return ddiff


class ENUM_Differ(BaseDiffer):
    def _diff(self):
        ddiff = _create_diff(self.entity[self.param_name].name, self.param_value, view=self.diff_view)
        return ddiff


class UUID_Differ(BaseDiffer):
    def _diff(self):
        ddiff = None
        if self.param_value != str(self.entity[self.param_name]):
            ddiff = _create_diff(str(self.entity[self.param_name]), self.param_value, view=self.diff_view)
        return ddiff


class JSON_Differ(BaseDiffer):
    def _diff(self):
        ddiff = None
        entity_as_dict = self.entity.to_dict()
        p_value_in_python = load_json_parameter(self.param_value)
        if entity_as_dict[self.param_name] != p_value_in_python:
            ddiff = _create_diff(entity_as_dict[self.param_name], p_value_in_python, view=self.diff_view)

        return ddiff


class _DEFAULT_Differ(BaseDiffer):
    def _diff(self):
        attr_name = self.attr_name
        entity_attr_value = self.entity[attr_name]
        ddiff = None
        try:
            # (med): We try to be smart here by checking if we are actually changing the value
            # of the field, not just adding or removing whitespace. This is possible for fields
            # where the value has a specific format like yaml and xml.
            if self.fields[attr_name].diff_type.value(entity_attr_value, self.param_value):
                ddiff = _create_diff(entity_attr_value, self.param_value, view=self.diff_view)
        except (TypeError, lxml.etree.XMLSyntaxError):
            ddiff = _create_diff(entity_attr_value, self.param_value, view=self.diff_view)
        return ddiff


class EntityManager:
    def __init__(
        self,
        cluster: Cluster,
        log_func: Callable | None = None,
    ) -> None:
        self.cluster = cluster
        self.log_func = log_func

    def lookup_entity(self, params, entity_class):
        entity_name = params[entity_class().meta.resolve_field_name]
        return self._lookup_entity_by_name(entity_name, entity_class)

    def _lookup_entity_by_name(
        self,
        entity_name: str,
        entity_class: type[Entity] | str,
    ) -> Entity | None:
        return self.cluster.get_by_name(entity_name, entity_class)

    def _diff_one_field(
        self,
        entity,
        params,
        param_name,
        param_value,
        diff_view="text",
    ) -> tuple[DeepDiff | None, MetaDataField]:
        differ = BaseDiffer(entity, param_name, param_value, diff_view)
        ddiff, field = differ.diff()
        return ddiff, field

    @typing.overload
    def check_diff(
        self,
        entity,
        params: dict[str, typing.Any],
        ignore_dictionary_item_removed: bool,
        diff_view: Literal["text"],
    ) -> dict[str, list[str]]:
        """Check diff."""

    @typing.overload
    def check_diff(
        self,
        entity,
        params: dict[str, typing.Any],
        ignore_dictionary_item_removed: bool,
        diff_view: Literal["tree"] | Literal["_delta"],
    ) -> dict[str, DeepDiff]:
        """Check diff."""

    def check_diff(
        self,
        entity,
        params: dict[str, typing.Any],
        ignore_dictionary_item_removed: bool = True,
        diff_view: Literal["text"] | Literal["tree"] | Literal["_delta"] = "text",
    ) -> dict[str, DeepDiff | list[str]]:
        """Check diff."""
        diffs = {}

        for param_name, param_value in params.items():
            diff, field = self._diff_one_field(entity, params, param_name, param_value, diff_view=diff_view)
            if not diff:
                continue

            if field.kind != MetaData.Type.JSON and ignore_dictionary_item_removed:
                diff.pop("dictionary_item_removed", None)  # TODO: figure out a way to not end up with such a diff.
            if not diff:
                continue

            diffs[param_name] = diff

        if diff_view == "text":
            # return {k: v.to_dict() for k, v in diffs.items()}
            # NEED to find a way to deal with type_changes changes
            # ansible choke on those because Type object are part of the dict
            return {k: v.pretty().splitlines() for k, v in diffs.items()}
        else:
            return diffs

    def _sort_fields(self, all_fields) -> dict[str, MetaDataField]:
        tail = [field for field in all_fields if field.kind == MetaData.Type.ELEMENT_OF]
        head = [field for field in all_fields if field not in tail]
        sorted_list = head + tail
        return {field.name: field for field in sorted_list}

    def create_resource(
        self,
        entity_class: type[Entity],
        params: dict[str, typing.Any],
        commit: bool = True,
    ) -> tuple[Entity, CommitResult]:
        fields = self._sort_fields(entity_class().fields())

        data: dict[str, Entity | list[Entity]] = {}

        def sort_func(param):
            param_name, param_value = param

            if "_" in param_name and param_name not in fields:
                bare_param_name, _ = param_name.split("_", 1)
            else:
                bare_param_name = param_name

            if bare_param_name not in fields:  # perhaps an alias
                return -1

            field = fields[bare_param_name]

            return field.kind

        clone_from = params.pop("cloneFrom", None)

        sorted_params = {k: v for k, v in sorted(params.items(), key=sort_func)}

        for param_name in sorted_params.keys():
            if "_" in param_name and param_name not in fields:
                bare_param_name, _ = param_name.split("_", 1)
            else:
                bare_param_name = param_name

            if bare_param_name not in fields:  # perhaps an alias
                continue

            field = fields[bare_param_name]

            if field.kind == MetaData.Type.ENTITY:
                if "_" in param_name and param_name not in fields:
                    _, instance_type = param_name.split("_", 1)
                else:
                    instance_type = field.instance

                sub_entity_class = _import_entity_class(instance_type)
                if field.vector:
                    entities = [
                        self.create_resource(sub_entity_class, one_param, commit=False)[0]
                        for one_param in sorted_params[param_name]
                    ]
                    data.setdefault(bare_param_name, [])
                    data[bare_param_name].extend(entities)
                else:
                    entity, _ = self.create_resource(sub_entity_class, sorted_params[param_name], commit=False)
                    data[bare_param_name] = entity

            elif field.kind == MetaData.Type.RESOLVE:
                sub_entity_class = _import_entity_class(field.instance)
                if field.vector:
                    entities = [
                        self._lookup_entity_by_name(one_param, sub_entity_class)
                        for one_param in sorted_params[param_name]
                    ]
                    data.setdefault(bare_param_name, [])
                    data[bare_param_name].extend(entities)
                else:
                    entity = self._lookup_entity_by_name(sorted_params[param_name], sub_entity_class)
                    if not entity:
                        err_msg = (
                            f"Error looking up {sorted_params[param_name]!r} object "
                            f"for type {sub_entity_class.__name__}"
                        )
                        raise Exception(err_msg)
                    data[bare_param_name] = entity

            elif field.kind == MetaData.Type.ELEMENT_OF:
                data[bare_param_name] = next(
                    obj for obj in data[field.element_of] if sorted_params[param_name] == obj.resolve_name
                )
            elif field.kind == MetaData.Type.JSON:
                data[bare_param_name] = json.loads(sorted_params[bare_param_name])
            else:
                if field.enum_type:
                    data[bare_param_name] = getattr(field.enum_type, sorted_params[bare_param_name])
                else:
                    data[bare_param_name] = sorted_params[bare_param_name]

        if clone_from:
            clone_from_obj = self.cluster.get_by_name(clone_from, entity_class)
            # TODO: improve error handling here.
            new_entity = clone_from_obj.clone()
            new_entity._convert(data)
        else:
            new_entity = entity_class(cluster=self.cluster, data=data)
        return new_entity, (new_entity.commit(wait_for_task=True) if commit else FAKE_SUCCESS_COMMIT_RESULT)

    def delete_resource(
        self,
        entity: Entity,
        params,
        commit: bool = True,
    ) -> tuple[Entity, CommitResult]:
        return entity, (entity.remove() if commit else FAKE_SUCCESS_COMMIT_RESULT)

    def _update_resource_values_changed(
        self,
        entity,
        attr_name: str,
        attr_instance: str,
        changes,
        field,
        params,
        param_name,
    ):
        for change in changes:
            if attr_instance:
                path = change.path().replace("root", f"root.{attr_name}_{attr_instance}")
            else:
                path = change.path().replace("root", f"root.{attr_name}")

            target_field = _getfield(entity, path)

            if not target_field.instance:
                if target_field.enum_type:
                    new_value = getattr(target_field.enum_type, change.t2)
                elif target_field.kind == MetaData.Type.JSON:
                    new_value = load_json_parameter(change.t2)
                else:
                    new_value = change.t2
                setpath(entity, new_value, path, replace=True)
            else:
                if target_field.kind == MetaData.Type.RESOLVE:
                    if change.t2 is None:
                        new_value = None
                    else:
                        new_value = self.cluster.get_by_name(change.t2, target_field.instance)
                    setpath(entity, new_value, path)

                elif target_field.kind == MetaData.Type.ENTITY:
                    assert isinstance(change.t2, dict)

                    self.update_resource(extract(entity, path), change.t2, commit=False)

                elif target_field.kind == MetaData.Type.ELEMENT_OF:
                    new_value = next((x for x in entity[target_field.element_of] if x.resolve_name == change.t2), None)
                    setpath(entity, new_value, path)

                else:
                    raise NotImplementedError

    def _update_resource_iterable_item_added(
        self,
        entity,
        attr_name: str,
        attr_instance: str,
        changes,
        field,
        params,
        param_name,
    ):
        for change in changes:
            if attr_instance:
                path = change.path().replace("root", f"root.{attr_name}_{attr_instance}")
            else:
                path = change.path().replace("root", f"root.{attr_name}")

            target_field = _getfield(entity, path)

            if not target_field.instance:
                if target_field.enum_type:
                    new_value = getattr(target_field.enum_type, change.t2)
                else:
                    new_value = change.t2
            else:
                if target_field.kind == MetaData.Type.RESOLVE:
                    new_value_type = getattr(pythoncm.entity, target_field.instance)

                    new_value = self.cluster.get_by_name(change.t2, new_value_type)

                elif target_field.kind == MetaData.Type.ENTITY:
                    element = _path_to_elements(path)[-2][0]

                    if "_" in element:
                        elem_field_name, elem_field_value_type = element.split("_", 1)
                        assert elem_field_name == target_field.name and hasattr(pythoncm.entity, elem_field_value_type)
                        target_param_name = elem_field_value_type
                    else:
                        target_param_name = target_field.instance

                    new_value_type = getattr(pythoncm.entity, target_param_name)

                    new_value, _ = self.create_resource(new_value_type, change.t2, commit=False)
                else:
                    raise NotImplementedError

            setpath(entity, new_value, path)

    def _update_resource_iterable_item_removed(
        self,
        entity,
        attr_name: str,
        attr_instance: str,
        changes,
        field,
        params,
        param_name,
    ):
        def sort_changes(change):
            path_elements = _path_to_elements(change.path())
            last_element = path_elements[-1]  # eg (0, 'GET')
            return int(last_element[0])

        sorted_changes = sorted(changes, key=sort_changes, reverse=True)
        for change in sorted_changes:
            if attr_instance:
                path = change.path().replace("root", f"root.{attr_name}_{attr_instance}")
            else:
                path = change.path().replace("root", f"root.{attr_name}")

            delpath(entity, path)

    def _update_resource_type_changes(
        self,
        entity,
        attr_name: str,
        attr_instance: str,
        changes,
        field,
        params,
        param_name,
    ):
        for change in changes:
            if attr_instance:
                path = change.path().replace("root", f"root.{attr_name}_{attr_instance}")
            else:
                path = change.path().replace("root", f"root.{attr_name}")

            target_field = _getfield(entity, path)

            if not target_field.instance:
                if target_field.enum_type:
                    new_value = getattr(target_field.enum_type, change.t2)
                elif target_field.kind == MetaData.Type.JSON:
                    new_value = load_json_parameter(change.t2)
                else:
                    new_value = change.t2
            else:
                if change.t1 is None:
                    new_value_type = getattr(pythoncm.entity, target_field.instance)

                    if target_field.kind == MetaData.Type.ENTITY:
                        element = _path_to_elements(path)[-1][0]

                        if "_" in element:
                            elem_field_name, elem_field_value_type = element.split("_", 1)
                            assert elem_field_name == target_field.name and hasattr(
                                pythoncm.entity, elem_field_value_type
                            )
                            target_param_name = elem_field_value_type
                        else:
                            target_param_name = target_field.instance

                        new_value_type = getattr(pythoncm.entity, target_param_name)

                        new_params = extract(params[param_name], change.path())
                        new_value, _ = self.create_resource(new_value_type, new_params, commit=False)

                    elif target_field.kind == MetaData.Type.RESOLVE:
                        new_value = self.cluster.get_by_name(change.t2, new_value_type)

                elif change.t2 is None:
                    if target_field.vector:
                        new_value = copy.copy(target_field.default)
                    else:
                        new_value = None
                else:
                    raise NotImplementedError

            setpath(entity, new_value, path)

    def _update_resource_dictionary_item_removed(
        self,
        entity,
        attr_name: str,
        attr_instance: str,
        changes,
        field,
        params,
        param_name,
    ):
        for change in changes:
            if attr_instance:
                path = change.path().replace("root", f"root.{attr_name}_{attr_instance}")
            else:
                path = change.path().replace("root", f"root.{attr_name}")

            delpath(entity, path)

    def _update_resource_dictionary_item_added(
        self, entity, attr_name, attr_instance, changes, field, params, param_name
    ):
        # FIXME: ideally we should not have those.
        self._update_resource_values_changed(entity, attr_name, attr_instance, changes, field, params, param_name)

    def update_resource(
        self,
        entity: Entity,
        params: dict[str, typing.Any],
        commit: bool = True,
    ) -> tuple[Entity, CommitResult]:
        params.pop("cloneFrom", None)  # NOTE: cloneFrom takes effect only at object creation.
        tree_diffs = self.check_diff(
            entity,
            params,
            diff_view="tree",
            ignore_dictionary_item_removed=False,
        )

        fields = {field.name: field for field in entity.fields()}

        ops: dict[str, list[Callable[[], typing.Any]]] = {}

        for param_name, tree_diff in tree_diffs.items():
            for change_type, changes in tree_diff.items():
                if "_" in param_name and param_name not in fields:
                    attr_name, attr_instance = param_name.split("_", 1)
                else:
                    attr_name = param_name
                    attr_instance = None  # noqa

                boxed_params = Box(params)

                updater = getattr(self, f"_update_resource_{change_type}")

                ops.setdefault(change_type, [])
                ops[change_type].append(
                    functools.partial(
                        updater,
                        entity,
                        attr_name,
                        attr_instance,
                        changes,
                        fields[attr_name],
                        boxed_params,
                        param_name,
                    )
                )

        resource_dictionary_item_removed_ops = ops.pop("dictionary_item_removed", [])

        for remove_op in resource_dictionary_item_removed_ops:
            remove_op()

        for _ops_name, ops_func_list in ops.items():
            for ops_func in ops_func_list:
                ops_func()

        return entity, entity.commit(wait_for_task=True) if commit else FAKE_SUCCESS_COMMIT_RESULT


class EntityQuery:
    def __init__(self, cluster: Cluster) -> None:
        self.cluster = cluster

    def find(self, entity_class: type[Entity]) -> list[Entity]:
        return self.cluster.get_by_type(entity_class)