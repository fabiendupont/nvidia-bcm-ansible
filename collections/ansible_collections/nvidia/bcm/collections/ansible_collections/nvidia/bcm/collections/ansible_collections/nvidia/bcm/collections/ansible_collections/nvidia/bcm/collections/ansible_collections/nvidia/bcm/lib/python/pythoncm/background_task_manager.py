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

import logging
import threading
from time import monotonic
from uuid import UUID

from pythoncm.entity import CMDaemonBackgroundTask


class BackgroundTaskManager:
    """
    Helper class that manages cmdaemon back ground tasks.
    Tasks are automatically added and procesessed.
    """

    def __init__(self, cluster):
        self.cluster = cluster
        self.logger = logging.getLogger(__name__)
        self._tasks = {}
        self._condition = threading.Condition()
        self.zero_uuid = UUID(int=0)

    def fetch(
        self, sources: list[UUID] | None = None, task_uuids: list[UUID] | None = None
    ) -> list[CMDaemonBackgroundTask]:
        if not bool(sources):
            nodes = self.cluster.get_by_type('Node')
            sources = [node.uuid for node in nodes]
        if not bool(task_uuids):
            task_uuids = []
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmain',
            call='pgetBackgroundTasks',
            args=[task_uuids, sources],
        )
        if code:
            raise OSError(out)
        return [CMDaemonBackgroundTask(self.cluster, it) for it in out if it is not None]

    def process(self, source: UUID, updated: list[UUID], removed: list[UUID]) -> None:
        """
        Process changed back ground tasks.
        """
        converted = None
        if len(updated):
            try:
                converted = self.fetch([source], updated)
            except OSError as e:
                self.logger.warning(f'Unable to update tasks: {e}')
        with self._condition:
            if len(removed):
                removed = set(removed)
                self._tasks = {uuid: task for uuid, task in self._tasks.items() if uuid not in removed}
            if converted is not None:
                self._tasks.update({it.uuid: it for it in converted})
            self.logger.debug(
                'Background tasks, updated: %d, removed: %d, total: %d',
                len(updated),
                len(removed),
                len(self._tasks),
            )
            self._condition.notify_all()

    def get(self, task_uuid: str | UUID):
        """
        Get a back ground task by ID
        """
        if isinstance(task_uuid, str):
            task_uuid = UUID(task_uuid)
        with self._condition:
            return self._tasks.get(task_uuid, None)

    def wait(self, task_uuids: str | list[str] | UUID | list[UUID], timeout=None) -> bool:
        """
        Wait for one or more tasks to be completed.
        If timeout is None, wait forever.

        Return value:
        True: all tasks have completed
        False: timeout was reached
        """
        start_time = monotonic()
        time_left = timeout
        if isinstance(task_uuids, str):
            task_uuids = [UUID(task_uuids)]
        elif isinstance(task_uuids, UUID):
            task_uuids = [task_uuids]
        elif isinstance(task_uuids, list):
            task_uuids = [UUID(it) if isinstance(it, str) else it for it in task_uuids]
        task_uuids = [it for it in task_uuids if isinstance(it, UUID) and it != self.zero_uuid]
        self.logger.debug(
            'Background tasks, wait for %d tasks: %s', len(task_uuids), ', '.join(str(it) for it in task_uuids)
        )
        if not bool(task_uuids):
            return False
        with self._condition:
            while (time_left is None) or (time_left > 0):
                if all((it in self._tasks) and (self._tasks[it].completed()) for it in task_uuids):
                    self.logger.debug('Background tasks, tasks completed')
                    break
                self._condition.wait(time_left)
                if time_left is not None:
                    time_left = timeout + start_time - monotonic()
            self.logger.debug('Background tasks, wait done')
            return (time_left is None) or (time_left > 0)
