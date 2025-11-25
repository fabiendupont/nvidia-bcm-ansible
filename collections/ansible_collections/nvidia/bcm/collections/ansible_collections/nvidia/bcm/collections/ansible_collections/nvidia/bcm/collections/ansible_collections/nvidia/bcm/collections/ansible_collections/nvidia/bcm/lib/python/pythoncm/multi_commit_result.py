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

from pythoncm.commit_result import CommitResult

if typing.TYPE_CHECKING:
    from pythoncm.cluster import Cluster
    from pythoncm.entity.entity import Entity


class MultiCommitResult(CommitResult):
    """
    Class containing the result of committing multiple entities
    """

    def __init__(self, cluster: Cluster, **kwargs):
        from pythoncm.entity.validation import Validation
        from pythoncm.entity_converter import EntityConverter

        self.cluster = cluster
        self.success: list[bool] = kwargs.get('success', [])
        self.task_uuids: list[UUID] = [UUID(it) for it in kwargs.get('task_uuids', [])]
        self.validation = [Validation(self.cluster, it) for it in kwargs.get('validation', [])]
        if 'errormessage' in kwargs:
            self.add([kwargs['errormessage']])

        self._updated_entities = {}
        for updated_entity in kwargs.get('updated_entities', []):
            if bool(updated_entity):
                base_type = updated_entity.get('baseType', None)
                if bool(base_type):
                    service = self.cluster._find_service(base_type)
                    converter = EntityConverter(self, service)
                    updated_entity = converter.convert(updated_entity)
                    self._updated_entities[updated_entity.uuid] = updated_entity

        self._extra_entities(**kwargs)

    @property
    def good(self) -> bool:
        """
        True if commit did not have any errors.
        """
        return all(self.success)

    def updated_entity(self, uuid: UUID) -> Entity | None:
        """
        Return updated entity with the supplied UUID
        """
        return self._updated_entities.get(uuid, None)

    def wait_for_task(self, timeout: float | None = None) -> bool | None:
        """
        Wait for back ground task, if any, to be completed.
        """
        task_uuids = [it for it in self.task_uuids if it != self.zero_uuid]
        if not bool(task_uuids):
            return None
        return self.cluster.background_task_manager.wait(task_uuids, timeout)
