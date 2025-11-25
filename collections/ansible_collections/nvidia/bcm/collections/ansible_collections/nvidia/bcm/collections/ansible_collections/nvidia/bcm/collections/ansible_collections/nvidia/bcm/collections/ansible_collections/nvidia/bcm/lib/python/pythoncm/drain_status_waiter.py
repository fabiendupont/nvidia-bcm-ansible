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

import threading
import typing
from time import monotonic

if typing.TYPE_CHECKING:
    from uuid import UUID

    from pythoncm.cluster import Cluster
    from pythoncm.entity import Node


class DrainStatusWaiter:
    """
    Watches the drain status of nodes and waits for all to be drained
    """

    def __init__(self, cluster: Cluster, nodes: list[Node | UUID]):
        self._cluster = cluster
        self._nodes = nodes
        self._waiting = False
        self._condition = threading.Condition()

    def stop(self) -> bool:
        with self._condition:
            if self._waiting:
                self._waiting = False
                self._condition.notify_one()
                return True
        return False

    def wait(self, interval: int = 60, timeout: int | None = None) -> bool:
        with self._condition:
            self._waiting = True
            start_time = int(monotonic())
            while self._waiting:
                drain_status = self._cluster.parallel.drain_status(self._nodes)
                if all(it.all_drained for it in drain_status):
                    self._waiting = False
                    return True
                if timeout is None:
                    self._condition.wait(interval)
                elif run_time := int(monotonic()) - start_time < timeout:
                    self._condition.wait(min(interval, timeout - run_time))
                else:
                    self._waiting = False
                    break
        return False
