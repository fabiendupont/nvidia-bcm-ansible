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
from uuid import UUID

from pythoncm.entity.metadata.validation import Validation as ValidationMeta

if typing.TYPE_CHECKING:
    from pythoncm.cluster import Cluster


class CommitResult:
    """
    Class containing the result of committing any entity.
    """

    zero_uuid = UUID(int=0)

    def __init__(self, cluster: Cluster, **kwargs):
        from pythoncm.entity.validation import Validation
        from pythoncm.entity_converter import EntityConverter

        self.cluster = cluster
        self.success: bool = kwargs.get('success', False)

        uuid = kwargs.get('task_uuid', None)
        if bool(uuid):
            if isinstance(uuid, UUID):
                self.task_uuid = uuid
            else:
                self.task_uuid = UUID(uuid)
        else:
            self.task_uuid = self.zero_uuid

        self.validation = [Validation(self.cluster, it) for it in kwargs.get('validation', [])]
        if 'errormessage' in kwargs:
            self.add([kwargs['errormessage']])

        updated_entity = kwargs.get('updated_entity', None)
        if bool(updated_entity):
            base_type = updated_entity.get('baseType', None)
            if bool(base_type):
                service = self.cluster._find_service(base_type)
                converter = EntityConverter(self, service)
                self.updated_entity = converter.convert(updated_entity)
            else:
                self.cluster.logger.info("No base type for updated entity")
                self.updated_entity = None
        else:
            self.updated_entity = None

        self._extra_entities(**kwargs)

    def _extra_entities(self, **kwargs) -> None:
        from pythoncm.entity_converter import EntityConverter

        extra_entities = kwargs.get('extra_entities', None)
        if bool(extra_entities):
            self.extra_entities = []
            for extra_entity in extra_entities:
                base_type = extra_entity.get('baseType', None)
                if bool(base_type):
                    service = self.cluster._find_service(base_type)
                    converter = EntityConverter(self, service)
                    self.extra_entities.append(converter.convert(extra_entity))
                else:
                    self.extra_entities = None
                    break
        else:
            self.extra_entities = None

    def add(self, errors, severity=ValidationMeta.Severity.ERROR):
        from pythoncm.entity.validation import Validation

        for error in errors:
            validation = Validation(self.cluster)
            validation.message = error
            validation.severity = severity
            self.validation.append(validation)

    @property
    def good(self) -> bool:
        """
        True if commit did not have any errors.
        """
        return self.success

    @property
    def not_active(self) -> bool:
        """
        True if head node was not active yet.
        """
        return any(it.error == ValidationMeta.Error.NOT_ACTIVE for it in self.validation)

    def wait_for_task(self, timeout: float | None = None) -> bool | None:
        """
        Wait for back ground task, if any, to be completed.
        """
        if self.task_uuid == self.zero_uuid:
            return None
        return self.cluster.background_task_manager.wait(self.task_uuid, timeout)

    def __repr__(self):
        """
        Return all validation warnings and errors.
        """
        return '\n'.join([it.message for it in self.validation])
