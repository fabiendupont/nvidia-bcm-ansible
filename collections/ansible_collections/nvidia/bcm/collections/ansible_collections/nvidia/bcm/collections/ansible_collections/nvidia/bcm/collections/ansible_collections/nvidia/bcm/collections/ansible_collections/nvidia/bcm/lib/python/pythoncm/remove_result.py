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

if typing.TYPE_CHECKING:
    from pythoncm.cluster import Cluster


class RemoveResult:
    """
    Class containing the result of removing any entity.
    """

    zero_uuid = UUID(int=0)

    def __init__(self, cluster: Cluster, **kwargs):
        from pythoncm.entity.willchange import WillChange

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
        self.will_change = [WillChange(self.cluster, it) for it in kwargs.get('changes', [])]
        if 'errormessage' in kwargs:
            self.add_warning(kwargs['errormessage'])

    @property
    def good(self) -> bool:
        """
        True if commit did not have any errors.
        """
        return self.success

    @property
    def only_warnings(self) -> bool:
        return all(it.auto_change != it.meta.AutoChange.NO for it in self.will_change)

    def add_warning(self, message, warning_level=-1):
        from pythoncm.entity.willchange import WillChange

        change = WillChange(self.cluster)
        change.ref_base_type = message
        change.auto_change = change.meta.AutoChange.NO
        self.will_change.append(change)

    def wait_for_task(self, timeout: float | None = None) -> bool | None:
        """
        Wait for back ground task, if any, to be completed.
        """
        if self.task_uuid == self.zero_uuid:
            return None
        return self.cluster.background_task_manager.wait(self.task_uuid, timeout)

    def __repr__(self):
        """
        Return all entities affected by the remove.
        """
        return '\n'.join([it.message for it in self.will_change])
