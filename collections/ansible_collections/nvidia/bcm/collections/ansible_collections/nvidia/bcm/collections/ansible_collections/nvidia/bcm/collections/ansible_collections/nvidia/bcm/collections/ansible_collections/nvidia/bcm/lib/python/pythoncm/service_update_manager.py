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

import itertools
import logging
import threading
import typing
from time import monotonic

if typing.TYPE_CHECKING:
    from uuid import UUID


class ServiceUpdateManager:
    """
    Helper class to wait for cluster update service
    Note that this class only works if a single thread waits.
    """

    def __init__(self):
        self.condition = threading.Condition()
        self.changed = set()
        self.logger = logging.getLogger(__name__)

    def stop(self):
        with self.condition:
            self.condition.notify_all()

    def process(self, node: UUID, name: str):
        with self.condition:
            self.logger.info('Process update service %s, node %s', name, node)
            self.changed.add((node, name))
            self.condition.notify_all()

    def wait(
        self,
        node: UUID | list[UUID],
        name: str | list[str],
        timeout=None,
    ):
        """
        Wait for a service update on a node

        arguments:
          node: a node UUID or list of UUID
          name: a service name or list of services
          timeout: maximal time in seconds to wait

        return:
          True: services was updated
          False: timeout was reached
        """
        start_time = monotonic()
        time_left = timeout
        if not isinstance(node, list):
            node = [node]
        if not isinstance(name, list):
            name = [name]
        self.logger.info('Wait for update services %s, nodes %s', str(name), str(node))
        required = set(itertools.product(node, name))
        found = False
        with self.condition:
            self.changed = set()
            while (time_left is None) or (time_left > 0):
                if required.intersection(self.changed) == required:
                    self.logger.info('All update services found')
                    found = True
                    break
                self.condition.wait(time_left)
                if time_left is not None:
                    time_left = timeout + start_time - monotonic()
        return found
