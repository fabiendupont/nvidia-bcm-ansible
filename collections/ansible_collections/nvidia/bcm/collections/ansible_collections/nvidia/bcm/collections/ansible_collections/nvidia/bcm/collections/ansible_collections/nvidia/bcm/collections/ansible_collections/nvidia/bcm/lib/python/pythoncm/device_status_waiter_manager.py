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
import typing

from pythoncm.device_status_waiter import DeviceStatusWaiter

if typing.TYPE_CHECKING:
    from uuid import UUID

    from pythoncm.cluster import Cluster


class DeviceStatusWaiterManager:
    """
    Manages state transitions for all interesting devices
    """

    def __init__(self, cluster: Cluster):
        self.cluster = cluster
        self.logger = logging.getLogger(__name__)
        self._waiters: list[DeviceStatusWaiter] = []
        self._condition = threading.Condition()

    def process(self, status) -> None:
        """
        Process a state change of a device.
        """
        with self._condition:
            [it.process(status) for it in self._waiters]

    def _completed(self, waiter: DeviceStatusWaiter) -> None:
        with self._condition:
            self._waiters = [it for it in self._waiters if it != waiter]

    def create(self, device: UUID, states) -> DeviceStatusWaiter:
        """
        Create and register a new waiter class.
        """
        with self._condition:
            waiter = DeviceStatusWaiter(self, device, states)
            self._waiters.append(waiter)
            return waiter
