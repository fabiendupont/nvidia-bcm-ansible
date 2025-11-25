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

from pythoncm.remove_result import RemoveResult

if typing.TYPE_CHECKING:
    from uuid import UUID

    from pythoncm.cluster import Cluster


class MultiRemoveResult(RemoveResult):
    """
    Class containing the result of removing any entity.
    """

    def __init__(self, cluster: Cluster, **kwargs):
        from pythoncm.entity.willchange import WillChange

        self.cluster = cluster
        self.success: list[bool] = kwargs.get('success', [])
        self.task_uuid: list[UUID] = kwargs.get('task_uuid', [])
        self.will_change = [WillChange(self.cluster, it) for it in kwargs.get('changes', [])]
        if 'errormessage' in kwargs:
            self.add_warning(kwargs['errormessage'])

    @property
    def good(self) -> bool:
        """
        True if commit did not have any errors.
        """
        return all(self.success)

    def wait_for_task(self, timeout: float | None = None) -> bool | None:
        """
        Wait for back ground task, if any, to be completed.
        """
        task_uuid = [it for it in self.task_uuid if it != self.zero_uuid]
        if not bool(task_uuid):
            return None
        return self.cluster.background_task_manager.wait(task_uuid, timeout)
