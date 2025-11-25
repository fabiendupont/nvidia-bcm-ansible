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

import copy
import itertools
import json
import logging
import typing
from uuid import UUID
from uuid import uuid4

import pythoncm.entity
from pythoncm.commit_result import CommitResult
from pythoncm.entity.meta_data import MetaData
from pythoncm.entity_to_json_encoder import EntityToJSONEncoder
from pythoncm.meta_data_cache import MetaDataCache
from pythoncm.monitoring.plot.result import Result
from pythoncm.remove_result import RemoveResult
from pythoncm.util import convert_to_uuid
from pythoncm.util import lower_no_space
from pythoncm.util import name_compare
from pythoncm.util import uuid_compare
from pythoncm.util import uuid_list_compare

top_logger_name = '.'.join(__name__.split('.')[:-1])  # Use full package name
logger = logging.getLogger(top_logger_name)  # Special case: use package name

if typing.TYPE_CHECKING:
    from pythoncm.cluster import Cluster
    from pythoncm.entity.meta_data_field import MetaDataField
    from pythoncm.entity.metadata.entity import Entity as EntityMetaData
    from pythoncm.entity.validation import Validation
    from pythoncm.entity_converter import EntityConverter


class AttributeView(list):
    def __init__(self, entity, field, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._entity: Entity = entity
        self._field: MetaDataField = field

    def pop(self, *args, **kwargs):
        poped = super().pop(*args, *kwargs)
        self._entity[self._field.name].remove(poped)
        return poped

    def remove(self, value) -> None:
        self._entity[self._field.name].remove(value)
        super().remove(value)

    def append(self, value) -> None:
        if len(self) > 0 and not isinstance(value, type(self[0])):
            raise TypeError(f"passed value should be of type {type(self[0]).__name__}")

        self._entity[self._field.name].append(value)
        super().append(value)

    def clear(self):
        for value in self:
            self._entity[self._field.name].remove(value)
        super().clear()

    def extend(self, iterable):
        for value in iterable:
            if len(self) > 0 and not isinstance(value, type(self[0])):
                raise TypeError(f"passed value should be of type {type(self[0]).__name__}")

            self._entity[self._field.name].append(value)
        super().extend(iterable)

    def insert(self, index, value) -> None:
        assert index >= 0

        if len(self) == 0:
            self._entity[self._field.name].append(value)
        else:
            if index == 0:
                before_elem = self[0]
                insert_index = max(self._entity[self._field.name].index(before_elem), 0)
            else:
                before_elem = self[index - 1]
                insert_index = self._entity[self._field.name].index(before_elem) + 1
            self._entity[self._field.name].insert(insert_index, value)

        super().insert(index, value)

    def reverse(self):
        raise NotImplementedError

    def __delitem__(self, name) -> None:
        self.remove(self[name])


class Entity:
    """
    The base class for all Bright managed entities
    """

    KEY_VALUE_STORE_FORMAT = 'cmd.entity[%d].%s'

    zero_uuid = UUID(int=0)

    def __init__(
        self,
        cluster: Cluster | None = None,
        data: dict[str, typing.Any] | None = None,
        service=None,
        converter: EntityConverter | None = None,
        parent: Entity | None = None,
        add_to_cluster: bool = True,
        create_sub_entities: bool = True,
        meta: EntityMetaData = None,
        **kwargs: typing.Any,
    ) -> None:
        self._cluster = cluster
        self._logger = logger.getChild(self.__class__.__name__)  # Use class name accessible directly from package
        self._service = service
        self._parent = parent
        self._remote_clone = None
        self.meta = meta or MetaDataCache()[self.__class__]
        self.__apply_meta_data()
        self.baseType: str = self.meta.baseType
        self.childType: str = self.meta.childType
        if data is None:
            real_data = kwargs
        else:
            real_data = data
            real_data.update(kwargs)
        self._convert(real_data, converter)
        if create_sub_entities:
            self.__create_sub_entities(converter)
        if (
            self._cluster is not None
            and self.meta.top_level
            and self.uuid == self.zero_uuid
            and self.meta.add_to_cluster
            and add_to_cluster
        ):
            self._cluster.add(self)

    def __hash__(self) -> int:
        if self.uuid and self._cluster is not None:
            return hash((self.__class__, self.uuid, self._cluster))
        return super().__hash__()

    def __lt__(self, other: Entity) -> bool:
        return self.uuid < other.uuid

    @property
    def leaf_type(self) -> str:
        if len(self.childType):
            return self.childType
        return self.baseType

    def fields(self):
        """
        All data fields.
        """
        return self.meta.fields()

    def clone(
        self,
        cluster: Cluster | None = None,
        add_to_cluster: bool = True,
        clear_cloned: bool = True,
    ) -> Entity:
        """
        Clone an entity.
        """

        # Prevent cyclic import
        from pythoncm.entity_converter import EntityConverter

        if cluster is None:
            cluster = self._cluster
        self._logger.info("Clone %s %s", self.baseType, self.resolve_name)
        converter = EntityConverter(cluster, self._service)
        data = copy.deepcopy(self.to_dict())
        indexes = self._get_element_of_indexes()
        entity = converter.convert(data)
        if entity is None:
            raise ValueError(f"Unable to clone: {self.baseType} {self.resolve_name}")
        if clear_cloned:
            entity._clear_cloned()
        if self.meta.top_level and add_to_cluster:
            entity._resolve_uuids()
            cluster.add(entity, force_uuids=True)
            entity._apply_element_of_indexes(indexes)
        else:
            entity.clear_uuids()
        entity._set_is_committed(False)
        return entity

    def _clear_cloned(self) -> None:
        for field in self.fields():
            if field.clone and (field.kind == MetaData.Type.ENTITY):
                value = getattr(self, field.name)
                if field.vector:
                    [it._clear_cloned() for it in value]
                elif (value is not None) and (value != self.zero_uuid):
                    value._clear_cloned()
            elif not field.clone or (field.conditional_clone is not None and not field.conditional_clone(self)):
                setattr(self, field.name, copy.copy(field.default))

    @property
    def resolve_name(self) -> str:
        """
        Get a generic name to identify the entity.
        """
        try:
            return getattr(self, self.meta.resolve_field_name)
        except AttributeError:
            return str(self.uuid)

    def lookup(self, name, type_=None):
        """
        Check if name matches the entity.
        """
        compare = name_compare(name, self.resolve_name)
        if (compare is not None) and (type_ is not None) and not self.check_type(type_):
            compare = None
        return compare

    def check_type(self, type_) -> bool:
        if isinstance(type_, str):
            if all(name_compare(type_, it) is None for it in self.meta.allTypes):
                return False
        elif not isinstance(self, type_):
            return False
        return True

    def revert(self) -> None:
        """
        Undo all local changes.
        """
        if not self.meta.allow_commit:
            raise TypeError(f'The {self.baseType} {self.resolve_name} is read only and cannot be removed')
        if not self.meta.top_level:
            raise TypeError(f'The {self.baseType} {self.resolve_name} cannot be reverted by itself')
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service=self._service.proxy,
            call=self._service.get_one(),
            args=[*self._service.get_one_extra_args, self.uuid],
        )
        if code == 0:
            self._logger.debug('Reverted: %s', self.resolve_name)
            self._convert(out)
            self._resolve_uuids()
        else:
            raise OSError(out)

    def commit(
        self,
        wait_for_task: bool = False,
        force: typing.SupportsInt = False,
        local_validate_check: bool = True,
        wait_for_remote_update: bool = False,
    ) -> CommitResult:
        """
        Commit all local changes.
        """
        if not self.meta.allow_commit:
            raise TypeError(f'The {self.baseType} {self.resolve_name} is read only and cannot be committed')
        if not self.meta.top_level:
            raise TypeError(f'The {self.baseType} {self.resolve_name} cannot be committed by itself')
        if local_validate_check:
            check_result = self.check()
        else:
            check_result = []
        self._set_uuids()
        self._update_modified()
        if wait_for_remote_update:
            self._cluster.entity_change.reset()
        try:
            from pythoncm.entity.metadata.validation import Validation

            if not self.is_committed:
                self._logger.debug('Add: %s', self.resolve_name)
                commit_result = self._commit_add(force)
            else:
                self._logger.debug('Update: %s', self.resolve_name)
                commit_result = self._commit_update(force)
            commit_result.add(check_result, severity=Validation.Severity.WARNING)
        except Exception:
            if check_result == []:
                raise
            commit_result = CommitResult(self._cluster, success=False)
            commit_result.add(check_result)
        if commit_result.good:
            if bool(commit_result.extra_entities):
                for extra_entity in commit_result.extra_entities:
                    self._logger.debug('Add extra: %s', extra_entity.resolve_name)
                    self._cluster.add(extra_entity, replace_existing=False)
            self._set_is_committed()
            self._clear_modified()
            if commit_result.updated_entity:
                self._logger.debug('Merge updated entity: %s', self.resolve_name)
                self._merge_updated(commit_result.updated_entity)
            if wait_for_remote_update:
                self._cluster.entity_change.wait(self.uuid)
            else:
                self._cluster.register_recently_committed(self.uuid)
            if wait_for_task:
                commit_result.wait_for_task()
        return commit_result

    def _commit_add(self, force: typing.SupportsInt) -> CommitResult:
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service=self._service.proxy,
            call=self._service.add_one(),
            args=[self.to_dict(), int(force)],
        )
        if code:
            raise OSError(out)
        commit_result = CommitResult(self._cluster, **out)
        if commit_result.good:
            self._logger.debug('Added: %s', self.resolve_name)
        else:
            self._logger.info('Failed to add: %s', self.resolve_name)
        return commit_result

    def _commit_update(self, force: typing.SupportsInt) -> CommitResult:
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service=self._service.proxy,
            call=self._service.update_one(),
            args=[self.to_dict(), int(force)],
        )
        if code:
            raise OSError(out)
        if 'result' in out:
            # CommitResult expects success instead of result
            out['success'] = out['result']
            out.pop('result')
        commit_result = CommitResult(self._cluster, **out)
        if commit_result.success:
            self._logger.debug('Updated: %s', self.resolve_name)
        else:
            self._logger.info('Failed to update: %s', self.resolve_name)
        return commit_result

    def remove(
        self,
        wait_for_task: bool = False,
        force: typing.SupportsInt = False,
        *args,
    ) -> RemoveResult:
        """
        Remove the entity.
        """
        if not self.meta.allow_commit:
            raise TypeError(f'The {self.baseType} {self.resolve_name} is read only and cannot be removed')
        if not self.meta.top_level:
            self.to_be_removed = True
            remove_result = RemoveResult(self._cluster)
            remove_result.success = True
            self._logger.debug('Remove sub entity: %s', self.resolve_name)
            return remove_result
        if self.uuid not in self._cluster.entities:
            remove_result = RemoveResult(self._cluster)
            remove_result.success = False
            remove_result.add_warning('Entity was not added to the cluster')
            self._logger.warning('Remove not committed entity: %s', self.resolve_name)
            return remove_result
        if not self.is_committed:
            remove_result = RemoveResult(self._cluster)
            remove_result.success = True
            self._logger.debug('Remove local: %s', self.resolve_name)
        else:
            self._logger.debug('Remove remote: %s', self.resolve_name)
            rpc_args = []
            if self._service.owner:
                rpc_args.append(UUID(int=0))
            rpc_args.append(self.uuid)
            rpc_args += list(args)
            rpc_args.append(int(force))
            rpc = self._cluster.get_rpc()
            (code, out) = rpc.call(
                service=self._service.proxy,
                call=self._service.remove_one(),
                args=rpc_args,
            )
            if code:
                raise OSError(out)
            remove_result = RemoveResult(self._cluster, **out)
        if remove_result.success:
            self._logger.debug('Removed: %s', self.resolve_name)
            if wait_for_task:
                remove_result.wait_for_task()
            self._cluster._remove(self.uuid)
        else:
            self._logger.info('Failed to remove: %s', self.resolve_name)
        return remove_result

    def used_by(self, wait_for_task: bool = False) -> list[Entity]:
        """
        Get the list of all entities which refer to this entity.
        """
        if not self.meta.top_level:
            raise ValueError('Not a top level entity')
        if not self.is_committed:
            raise ValueError('Not committed yet')
        rpc_args = []
        if self._service.owner:
            rpc_args.append(UUID(int=0))
        rpc_args.append(self.uuid)
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service=self._service.proxy,
            call=self._service.used_by_one(),
            args=rpc_args,
        )
        if code:
            raise OSError(out)
        return out

    def validate(self, wait_for_task: bool = False) -> list[Validation]:
        """
        Validate the changes of local entity.
        """
        from pythoncm.entity.validation import Validation

        if not self.meta.allow_commit:
            raise TypeError(f'The {self.baseType} {self.resolve_name} is read only and cannot be validated')
        if not self.meta.top_level:
            raise TypeError(f'The {self.baseType} {self.resolve_name} is not a top level entity')
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service=self._service.proxy,
            call=self._service.validate_one(),
            args=[self.to_dict()],
        )
        if code:
            raise OSError(out)
        return [Validation(self._cluster, it) for it in out]

    def _set_is_committed(self, is_committed: bool = True, recursive: bool = True) -> None:
        self.is_committed = is_committed
        self._logger.debug("Set is committed %s (%s): %d", self.resolve_name, str(self.uuid), self.is_committed)
        if recursive:
            for field in self.fields():
                try:
                    value = getattr(self, field.name)
                    if field.kind == MetaData.Type.ENTITY:
                        if field.vector:
                            [it._set_is_committed(is_committed) for it in value]
                        elif (value is not None) and (value != self.zero_uuid):
                            value._set_is_committed(is_committed)
                except Exception as e:
                    self._logger.info(
                        "Set is_committed for %s %s, %s: %s", self.leaf_type, self.resolve_name, field.name, e
                    )

    def _clear_modified(self) -> None:
        self.modified = False
        for field in self.fields():
            try:
                value = getattr(self, field.name)
                if field.kind == MetaData.Type.ENTITY:
                    if field.vector:
                        [it._clear_modified() for it in value]
                    elif (value is not None) and (value != self.zero_uuid):
                        value._clear_modified()
            except Exception as e:
                self._logger.info("Clear modified for %s %s, %s: %s", self.leaf_type, self.resolve_name, field.name, e)

    @property
    def is_modified(self) -> bool:
        return self._update_modified(False, True)

    def _update_modified(self, also_removed: bool = False, check: bool = False) -> bool:
        if check and self.modified:
            return True
        modified = self.to_be_removed if also_removed else not self.is_committed
        for field in self.fields():
            if check and modified:
                return True
            if field.name in {'is_committed', 'to_be_removed'}:
                continue
            try:
                value = getattr(self, field.name)
                if field.kind == MetaData.Type.ENTITY:
                    if field.vector:
                        if self._remote_clone is not None and field.name in self._remote_clone:
                            modified |= len(value) != len(self._remote_clone[field.name])
                        modified_children = tuple(it._update_modified(True, check) for it in value)
                        modified |= any(modified_children)
                    elif (value is not None) and (value != self.zero_uuid):
                        modified |= value._update_modified(True, check)
                    else:
                        modified |= (self._remote_clone is not None) and (field.name in self._remote_clone)
                elif (self._remote_clone is None) or (field.name not in self._remote_clone):
                    modified |= value != field.default
                elif field.kind in {MetaData.Type.RESOLVE, MetaData.Type.ELEMENT_OF, MetaData.Type.UUID}:
                    resolved = convert_to_uuid(value)
                    if field.vector:
                        modified |= not uuid_list_compare(resolved, self._remote_clone[field.name])
                    else:
                        modified |= not uuid_compare(resolved, self._remote_clone[field.name])
                elif field.kind == MetaData.Type.ENUM:
                    modified |= (value != self._remote_clone[field.name]) and (
                        value.name != self._remote_clone[field.name]
                    )
                else:
                    modified |= value != self._remote_clone[field.name]
            except Exception as e:
                self._logger.info("Update modified for %s %s, %s: %s", self.leaf_type, self.resolve_name, field.name, e)
        if check:
            return modified
        self.modified |= modified
        return self.modified

    def _get_element_of_indexes(self) -> dict[str, int]:
        indexes = {}
        for field in self.fields():
            if field.kind == MetaData.Type.ELEMENT_OF:
                try:
                    value = getattr(self, field.name)
                    if isinstance(value, Entity):
                        value = value.uuid
                    elif isinstance(value, str):
                        value = UUID(value)
                    if value is not None and value != self.zero_uuid:
                        options = getattr(self, field.element_of)
                        indexes[field.name] = next((i for i, field in enumerate(options) if field.uuid == value))
                except Exception as e:
                    self._logger.info(
                        "Get element of failed for %s %s, %s: %s", self.leaf_type, self.resolve_name, field.name, str(e)
                    )
        return indexes

    def _apply_element_of_indexes(self, indexes: dict[str, int]) -> None:
        for name, index in indexes.items():
            try:
                field = self.meta.meta.get_by_name(name)
                options = getattr(self, field.element_of)
                setattr(self, name, options[index])
            except Exception as e:
                self._logger.info(
                    "Apply element of failed for %s %s, %s: %s", self.leaf_type, self.resolve_name, name, e
                )

    def __apply_meta_data(self) -> None:
        [setattr(self, field.name, copy.copy(field.default)) for field in self.fields()]

    def __create_sub_entities(self, converter: EntityConverter | None) -> None:
        # Prevent cyclic import
        from pythoncm.entity_converter import EntityConverter

        if converter is None:
            converter = EntityConverter(self._cluster, self._service)
        for field in self.fields():
            if field.create_instance and field.kind == MetaData.Type.ENTITY:
                try:
                    value = getattr(self, field.name)
                    if value is None:
                        value = converter.create(
                            field.init_instance if field.init_instance is not None else field.instance,
                            owner=self,
                            create_sub_entities=True,
                        )
                        setattr(self, field.name, value)
                except Exception as e:
                    self._logger.info(
                        "Get element of failed for %s %s, %s: %s", self.leaf_type, self.resolve_name, field.name, e
                    )

    def _convert(
        self,
        data: dict[str, typing.Any],
        converter: EntityConverter | None = None,
    ) -> None:
        # Prevent cyclic import
        from pythoncm.entity_converter import EntityConverter

        if data is None:
            return
        if not isinstance(data, dict):
            raise TypeError(f'Entity.convert called with invalid data: {type(data).__name__}')
        if converter is None:
            converter = EntityConverter(self._cluster, self._service)
        self.__dict__.update(data)
        self._remote_clone = data
        for field in self.fields():
            if field.kind == MetaData.Type.ENTITY:
                try:
                    value = getattr(self, field.name)
                    if field.vector:
                        converted = [converter.convert(it, self) for it in value]
                    elif value == 0:
                        converted = None
                    elif value is None or isinstance(value, Entity):
                        continue
                    else:
                        converted = converter.convert(value, self)
                    setattr(self, field.name, converted)
                except Exception as e:
                    self._logger.warning('Resolve error for %s: %s', field.name, e)
            elif field.kind == MetaData.Type.JSON:
                try:
                    value = getattr(self, field.name)
                    if isinstance(value, str):
                        value = json.loads(value)
                        setattr(self, field.name, value)
                except Exception as e:
                    self._logger.warning('JSON load error for %s: %s', field.name, e)
            elif field.kind == MetaData.Type.ENUM:
                try:
                    value = getattr(self, field.name)
                    if field.vector:
                        setattr(self, field.name, [field.enum_type[it] for it in value if isinstance(it, str | int)])
                    elif isinstance(value, str | int):
                        setattr(self, field.name, field.enum_type[value])
                except Exception as e:
                    self._logger.warning('JSON load error for %s: %s', field.name, e)
            elif field.kind == MetaData.Type.UUID:
                try:
                    value = getattr(self, field.name)
                    if field.vector:
                        setattr(self, field.name, [UUID(it) for it in value])
                    elif isinstance(value, str):
                        setattr(self, field.name, UUID(value))
                    elif isinstance(value, int):
                        setattr(self, field.name, UUID(int=value))
                except Exception as e:
                    self._logger.warning('UUID load error for %s: %s', field.name, e)
            elif field.vector:
                try:
                    value = getattr(self, field.name)
                    setattr(self, field.name, copy.deepcopy(value))
                except Exception as e:
                    self._logger.warning('vector field load error for %s: %s', field.name, e)

    def _resolve_uuids(self) -> None:
        for field in self.fields():
            if field.kind == MetaData.Type.RESOLVE:
                try:
                    value = getattr(self, field.name)
                    if field.vector:
                        if all(isinstance(it, str | UUID) for it in value):
                            resolved = self._cluster.get_by_uuid(value)
                            if resolved is not None and not any(it is None for it in resolved):
                                setattr(self, field.name, resolved)
                    elif isinstance(value, str | UUID):
                        if isinstance(value, str):
                            value = UUID(value)
                        if value == self.zero_uuid:
                            setattr(self, field.name, None)
                        else:
                            resolved = self._cluster.get_by_uuid(value)
                            if resolved is not None:
                                setattr(self, field.name, resolved)
                except Exception as e:
                    self._logger.warning('Resolve error for %s: %s', field.name, e)
            elif field.kind == MetaData.Type.ENTITY:
                try:
                    value = getattr(self, field.name)
                    if value is None or value == self.zero_uuid:
                        continue
                    if field.vector:
                        [it._resolve_uuids() for it in value]
                    else:
                        value._resolve_uuids()
                except Exception as e:
                    self._logger.warning('Resolve entity error for %s: %s', field.name, e)
            elif field.kind == MetaData.Type.ELEMENT_OF:
                try:
                    value = getattr(self, field.name)
                    if isinstance(value, str):
                        value = UUID(value)
                    if value is None or value == self.zero_uuid:
                        continue
                    if isinstance(value, Entity):
                        value = value.uuid
                    resolved = next(it for it in getattr(self, field.element_of) if it.uuid == value)
                    setattr(self, field.name, resolved)
                except Exception as e:
                    self._logger.warning(
                        'Resolve entity error for %s, element of: %s, value: %s, count %d: %s',
                        field.name,
                        field.element_of,
                        value,
                        len(getattr(self, field.element_of)),
                        e,
                    )

    def clear_uuids(self) -> None:
        self.uuid = self.zero_uuid
        for field in self.fields():
            if field.kind == MetaData.Type.ENTITY:
                try:
                    value = getattr(self, field.name)
                    if (value is None) or (value == 0):
                        continue
                    if field.vector:
                        [it.clear_uuids() for it in value]
                    else:
                        value.clear_uuids()
                except Exception as e:
                    self._logger.warning('Clear uuid error for %s: %s', field.name, e)

    def _set_uuids(self, cluster: Cluster | None = None, force: bool = False) -> None:
        if (cluster is not None) and (self._cluster != cluster):
            self._cluster = cluster
        if self.uuid == self.zero_uuid or force:
            self.uuid = uuid4()
        for field in self.fields():
            if field.kind == MetaData.Type.ENTITY:
                try:
                    value = getattr(self, field.name)
                    if value is None or value == self.zero_uuid:
                        continue
                    if field.vector:
                        [it._set_uuids(self._cluster, force) for it in value]
                    else:
                        value._set_uuids(self._cluster, force)
                except Exception as e:
                    self._logger.warning('Set uuid error for %s: %s', field.name, e)

    @staticmethod
    def _convert_to_uuid(data: UUID | str | Entity | None) -> UUID:
        if data is None:
            return UUID(int=0)
        if isinstance(data, str):
            return UUID(data)
        if isinstance(data, Entity):
            return data.uuid
        return data

    @staticmethod
    def _convert_to_name_type(data: Entity | None) -> str | None:
        if data is None:
            return None
        return f"{data.baseType}({data.resolve_name})"

    def to_dict(
        self, resolve_entities: bool = True, minify: bool = False, resolve_to_name_type: bool = False
    ) -> dict[str, typing.Any]:
        """
        Convert entity to python dictionary
        """
        data = {}
        for field in self.fields():
            try:
                value = getattr(self, field.name)
                if resolve_entities:
                    if field.kind == MetaData.Type.RESOLVE:
                        if field.vector:
                            if resolve_to_name_type:
                                value = [self._convert_to_name_type(it) for it in value]
                            else:
                                value = [self._convert_to_uuid(it) for it in value]
                        else:  # noqa: PLR5501
                            if resolve_to_name_type:
                                if field.clone:
                                    value = self._convert_to_name_type(value)
                                else:
                                    value = None
                            else:
                                value = self._convert_to_uuid(value)
                    elif field.kind == MetaData.Type.ENTITY:
                        if field.vector:
                            value = [it.to_dict(resolve_entities, minify, resolve_to_name_type) for it in value]
                        elif value is None:
                            value = 0  # zero_uuid ???
                        else:
                            value = value.to_dict(resolve_entities, minify, resolve_to_name_type)
                    elif field.kind == MetaData.Type.ELEMENT_OF:
                        if isinstance(value, Entity):
                            if resolve_to_name_type:
                                value = self._convert_to_name_type(value)
                            else:
                                value = value.uuid
                        elif value is None:
                            if resolve_to_name_type:
                                value = None
                            else:
                                value = self.zero_uuid
                    elif field.kind == MetaData.Type.ENUM:
                        if field.vector:
                            value = [it.name for it in value]
                        else:
                            value = value.name
                if minify:
                    if field.vector:
                        default = []
                    else:
                        default = field.default
                    if default is not None and value == default:
                        continue
            except Exception:
                if field.default is not None:
                    value = copy.copy(field.default)
                else:
                    continue
            data[field.name] = value
        return data

    def check(self) -> list[str]:
        """
        Check if local entity has valid data.
        """
        errors = []
        for field in self.fields():
            value = getattr(self, field.name)
            if not MetaData.check_kind(field, value):
                errors.append(
                    f'{field.name} of ({self.leaf_type}:{self.resolve_name}) '
                    f'does not contain the proper type: {value.__class__.__name__}'
                    f', expected: {field.kind.name}, vector: {field.vector}'
                )
            elif field.kind == MetaData.Type.ENTITY:
                if field.vector:
                    all_errors = [it.check() for it in value]
                    errors += itertools.chain.from_iterable(all_errors)
                elif value:
                    errors += value.check()
        return errors

    def __str__(self, indent: int = 4) -> str:
        return json.dumps(self.to_dict(), cls=EntityToJSONEncoder, indent=indent, ensure_ascii=True)

    def __repr__(self, indent: int = 4) -> str:
        return json.dumps(self.to_dict(), cls=EntityToJSONEncoder, indent=indent, ensure_ascii=True)

    def _filter_measurables(
        self,
        measurable_uuids: list[UUID],
        metrics: bool = True,
        healthchecks: bool = True,
        enum_metrics: bool = True,
    ) -> list[UUID]:
        if not all([metrics, healthchecks, enum_metrics]):
            measurables = self._cluster.get_by_uuid(measurable_uuids)
            measurable_uuids = []
            for measurable in measurables:
                if (
                    (measurable.is_metric() and metrics)
                    or (measurable.is_healthcheck() and healthchecks)
                    or (measurable.is_enum_metric() and enum_metrics)
                ):
                    measurable_uuids.append(measurable.uuid)
        return measurable_uuids

    def get_all_measurables(
        self,
        metrics: bool = True,
        healthchecks: bool = True,
        enum_metrics: bool = True,
        timeout: float | None = None,
    ) -> list[UUID]:
        """
        Get all measurable associated with the entity.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='getMonitoringMeasurablesForEntity',
            args=[self.uuid],
            timeout=timeout,
        )
        if code:
            raise OSError(out)
        return self._filter_measurables(out, metrics, healthchecks, enum_metrics)

    def get_all_metrics(self) -> list[UUID]:
        """
        Get all metrics associated with the entity.
        """
        return self.get_all_measurables(metrics=True, healthchecks=False, enum_metrics=False)

    def get_all_healthchecks(self) -> list[UUID]:
        """
        Get all health checks associated with the entity.
        """
        return self.get_all_measurables(metrics=False, healthchecks=True, enum_metrics=False)

    def get_all_enum_metrics(self) -> list[UUID]:
        """
        Get all enum metrics associated with the entity.
        """
        return self.get_all_measurables(metrics=False, healthchecks=False, enum_metrics=True)

    def get_latest_monitoring_data(
        self,
        measurables=None,
        include_measurable_status: bool = False,
        timeout: float | None = None,
        counter: bool = False,
    ) -> Result:
        """
        Get the latest monitoring data.
        """
        if measurables is None:
            measurables = self.get_all_measurables()
        return self._cluster.monitoring.get_latest_monitoring_data(
            [self.uuid], measurables, include_measurable_status, timeout, counter
        )

    def get_latest_health_data(
        self,
        include_measurable_status: bool = False,
        timeout: float | None = None,
    ) -> Result:
        """
        Get the latest health check data.
        """
        return self.get_latest_monitoring_data(
            measurables=self.get_all_healthchecks(),
            include_measurable_status=include_measurable_status,
            timeout=timeout,
        )

    def dump_monitoring_data(
        self,
        start_time: int,
        end_time: int,
        measurables: int | Entity | None = None,
        intervals: int = 0,
        timeout: float | None = None,
        clip: bool = False,
        uncompress: bool = False,
    ) -> Result:
        """
        Dump monitoring data

        clip: do not return data from outside the requested range
        uncompress: return samples without run-length-encoding
        """
        if measurables is None:
            measurables = self.get_all_measurables()
        else:
            measurables = [it for it in measurables if isinstance(it, int)] + [
                it.uuid for it in measurables if isinstance(it, Entity)
            ]
        request = {
            'entities': [self.uuid],
            'measurables': measurables,
            'range_start': start_time * 1000,
            'range_end': end_time * 1000,
            'clip': clip,
            'uncompress': uncompress,
            'intervals': intervals,
        }
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='plot',
            args=[request],
            timeout=timeout,
        )
        if code:
            raise OSError(out)
        return Result(self._cluster, request, out)

    def sample_now(
        self,
        measurables: UUID | Entity | None = None,
        env: dict | None = None,
        timeout: float | None = None,
    ) -> Result:
        """
        Live sample of monitoring measurables.
        """
        if measurables is None:
            measurables = self.get_all_measurables()
        else:
            measurables = [self._convert_to_uuid(it) for it in measurables]
        request = {'entities': [self.uuid], 'measurables': measurables}
        if env is not None:
            request['env'] = env
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='sample',
            args=[request],
            timeout=timeout,
        )
        if code:
            raise OSError(out)
        return Result(self._cluster, request, out, latest=True)

    def monitoring_producers(self):
        """
        Get all producers configured for the entity.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='getMonitoringDataProducerForEntity',
            args=[self.uuid],
        )
        if code:
            raise OSError(out)
        return self._cluster.get_by_uuid(out)

    def monitoring_types(self):
        """
        Get the types by which the entity is known by the monitoring system.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='getEntityTypes',
            args=[self.uuid],
        )
        if code:
            raise OSError(out)
        return out

    def monitoring_resources(self):
        """
        Get the resources associated with the entity in the monitoring system.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='getEntityResources',
            args=[self.uuid],
        )
        if code:
            raise OSError(out)
        return out

    def create_ramdisk(
        self,
        dependencies: bool = False,
        verbose: bool = False,
        wait: bool = False,
        timeout: float | None = None,
    ):
        """
        Create the ramdisk.
        """
        if not hasattr(self, 'softwareImageProxy') and self.baseType != 'SoftwareImage':
            raise ValueError('This entity does not allow ramdisk creation')
        if not self.is_committed:
            raise ValueError('This entity is not yet committed')
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmpart',
            call='createRamdisk',
            args=[[self.uuid], dependencies, self._cluster.session_uuid, verbose],
        )
        if code:
            raise OSError(out)
        if wait:
            self._cluster.background_task_manager.wait(out, timeout)
            return [self._cluster.background_task_manager.get(it) for it in out]
        return out

    def set_uuid_value(self, key: str, value: str) -> bool:
        if not self.is_committed:
            raise ValueError(f'{self.resolve_name} is not committed yet')
        return self._cluster.key_value_store.set(self.KEY_VALUE_STORE_FORMAT % (self.uuid, key), value)

    def get_uuid_value(self, key: str) -> str | None:
        _, pairs = self._cluster.key_value_store.get([self.KEY_VALUE_STORE_FORMAT % (self.uuid, key)])
        if bool(pairs):
            return pairs[0].value
        return None

    def remove_uuid_value(self, key: str) -> str | None:
        return self._cluster.key_value_store.purge([self.KEY_VALUE_STORE_FORMAT % (self.uuid, key)])

    def _merge_updated(self, updated_entity: Entity, forced: bool = False, resolve_uuids: bool = True) -> bool:
        if self.modified:
            self._logger.info('Both you and someone else changed %s', self.resolve_name)
            if not forced:
                return False
            self.modified = False
        self._set_is_committed(recursive=False)
        self._logger.info('Merge update of %s: %s', self.resolve_name, self.is_committed)
        fully_updated = True

        for field in self.fields():
            value = getattr(self, field.name)
            updated_value = getattr(updated_entity, field.name)
            if field.kind in {MetaData.Type.RESOLVE, MetaData.Type.ELEMENT_OF, MetaData.Type.UUID}:
                updated_value = convert_to_uuid(updated_value)
            if field.kind == MetaData.Type.ENTITY:
                if field.vector:
                    if (len(value) == 0) or (len(updated_value) == 0):
                        for it in updated_value:
                            it._set_is_committed()
                        setattr(self, field.name, updated_value)
                    else:
                        old_value_lookup = {it.uuid: it for it in value}
                        merged_value = []
                        for jt in updated_value:
                            old_value = old_value_lookup.get(jt.uuid, None)
                            if old_value is None:
                                jt._set_is_committed()
                                merged_value.append(jt)
                            else:
                                fully_updated &= old_value._merge_updated(jt, forced, resolve_uuids)
                                merged_value.append(old_value)
                        setattr(self, field.name, merged_value)
                elif value is None or updated_value is None:
                    setattr(self, field.name, updated_value)
                else:
                    fully_updated &= value._merge_updated(updated_value, forced, resolve_uuids)
            else:
                setattr(self, field.name, updated_value)
        self._remote_clone = updated_entity.clone(add_to_cluster=False, clear_cloned=False)._remote_clone
        if resolve_uuids:
            self._resolve_uuids()
        self._set_is_committed(recursive=False)
        return fully_updated

    def GNSS_location(self):
        """
        Get the location as reported by the GNSS script
        """
        from pythoncm.entity import GNSSLocation

        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmpart',
            call='getGNSSLocation',
            args=[self.uuid],
        )
        if code:
            raise OSError(out)
        if out is None:
            return None
        return GNSSLocation(self._cluster, out, parent=self)

    def get_extra_value(self, key: str) -> int | bool | str | list | None:
        if isinstance(self.extra_values, dict):
            return self.extra_values.get(lower_no_space(key), None)
        return None

    def set_extra_value(self, key: str, value: int | bool | str | list | None) -> None:
        if not isinstance(self.extra_values, dict):
            self.extra_values = {}
        self.extra_values[lower_no_space(key)] = value

    def clear_extra_value(self, key: str) -> bool:
        if not isinstance(self.extra_values, dict):
            return False
        key = lower_no_space(key)
        if key in self.extra_values:
            del self.extra_values[key]
            if not bool(self.extra_values):
                self.extra_values = None
            return True
        return False

    def __extra_magic_attribute_parts(self, attr: str) -> tuple[MetaDataField, type[Entity]]:
        if "_" not in attr:
            raise AttributeError(attr)

        field_name, field_type_name = attr.split("_", 1)

        field = next((field for field in self.fields() if field.name == field_name), None)

        field_type = None
        if field:
            field_type = getattr(pythoncm.entity, field_type_name, None)

        # TODO: assert field_type is subclass of field.instance

        if not field_name or not field_type:
            raise AttributeError(attr)

        return field, field_type

    def __mapping_access_check(self, name: str) -> None:
        if not isinstance(name, str):
            raise TypeError(f"{self.__class__.__name__} key should be string, not {name.__class__.__name__}")

        try:
            getattr(self, name)
        except AttributeError as exc:
            raise KeyError(name).with_traceback(exc.__traceback__) from exc

    def __getitem__(self, name: str) -> typing.Any:
        self.__mapping_access_check(name)
        return getattr(self, name)

    def __setitem__(self, name: str, value: typing.Any) -> None:
        self.__mapping_access_check(name)
        setattr(self, name, value)

    def __delitem__(self, name: str) -> None:
        self.__mapping_access_check(name)
        delattr(self, name)

    def __contains__(self, name: str) -> bool:
        try:
            getattr(self, name)
        except (TypeError, KeyError, AttributeError):
            return False
        return True

    def __getattr__(self, attr: str) -> typing.Any | list[typing.Any]:
        field, field_type = self.__extra_magic_attribute_parts(attr)

        if field.vector:
            return AttributeView(self, field, (obj for obj in self[field.name] if isinstance(obj, field_type)))

        obj = getattr(self, field.name)
        return obj if isinstance(obj, field_type) else None

    def _attr_is_set_and_committed(self, attr: str) -> bool:
        return hasattr(self, attr) and getattr(self, attr) and self.is_committed

    def __setattr__(self, attr: str, value: typing.Any) -> None:
        if hasattr(self, attr):
            try:
                self.__getattr__(attr)
                # magic used
            except AttributeError:
                # We have real attribute (property?), use normal logic
                super().__setattr__(attr, value)
                return
        try:
            field, field_type = self.__extra_magic_attribute_parts(attr)

            if field.vector:
                if not isinstance(value, list):
                    raise TypeError
                values = value

                if values and not all(isinstance(value, field_type) for value in values):
                    raise TypeError

                new_value = self[field.name]
                for candidate in values:
                    if candidate in new_value:
                        continue
                    new_value.append(candidate)
            else:
                new_value = value

            self[field.name] = new_value

        except AttributeError:
            super().__setattr__(attr, value)

    def __delattr__(self, name: str) -> None:
        if "_" in name:
            try:
                field, _field_type = self.__extra_magic_attribute_parts(name)
                if field.vector:
                    for value in getattr(self, name):
                        self.__dict__[field.name].remove(value)
                else:
                    self.__dict__[field.name] = copy.copy(field.default)
            except AttributeError:
                super().__delattr__(name)
        else:
            fields = {field.name: field for field in self.fields()}
            if name in fields:
                field = fields[name]
                self.__dict__[field.name] = copy.copy(field.default)
            else:
                super().__delattr__(name)
