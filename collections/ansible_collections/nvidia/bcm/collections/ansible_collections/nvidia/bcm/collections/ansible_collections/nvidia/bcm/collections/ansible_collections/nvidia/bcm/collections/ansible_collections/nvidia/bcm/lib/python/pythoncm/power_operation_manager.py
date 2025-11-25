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

from pythoncm.entity_converter import EntityConverter


class PowerOperationManager:
    """
    Manages back ground power operations
    """

    def __init__(self, cluster):
        self.cluster = cluster
        self.logger = logging.getLogger(__name__)
        self._states = {}
        self._condition = threading.Condition()
        self._converter = EntityConverter(self.cluster, service=None)

    def update(self, status):
        """
        Process an status update.
        """
        converted = [self._converter.convert(it) for it in status]
        converted = [it for it in converted if it is not None]
        self.logger.debug('Power operation manager, updated: %d / %d', len(converted), len(status))
        if len(converted) == 0:
            return
        with self._condition:
            # TODO: remove old
            self._states.update({(it.device, jt): it for it in converted for jt in it.indexes})
            self._condition.notify_all()

    def wait(self, devices, index, count, timeout=None):
        """
        Wait for a power operation to be completed.
        """
        with self._condition:
            start_time = monotonic()
            time_left = timeout
            states = []
            while (time_left is None) or (time_left > 0):
                states = [self._states.get((it, index), None) for it in devices]
                if states.count(None) == 0:
                    break
                self._condition.wait(time_left)
                if time_left is not None:
                    time_left = timeout + start_time - monotonic()
        return (time_left is None) or (time_left > 0), states

    def get(self, devices, index):
        """
        Get for a power operation result.

        Return one status or None per device
        """
        with self._condition:
            return [self._states.get((it, index), None) for it in devices]
