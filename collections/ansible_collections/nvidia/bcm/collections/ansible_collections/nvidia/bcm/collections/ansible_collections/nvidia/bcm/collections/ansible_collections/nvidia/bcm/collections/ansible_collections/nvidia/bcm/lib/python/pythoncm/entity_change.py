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


class EntityChange:
    """
    Helper class to wait for cluster side entity changes.
    Note that this class only works if a single thread waits.
    """

    max_age = 15

    def __init__(self):
        self.condition = threading.Condition()
        self.waiting = 0
        self.changed = {}
        self.logger = logging.getLogger(__name__)

    def stop(self):
        with self.condition:
            if self.waiting:
                self.logger.info(f"Stop event change watcher, active: {self.waiting}")
                self.waiting = 0
                self.condition.notify_all()
            else:
                self.logger.debug("Stop event change")
        return True

    def notify(self, entity_type: str, uuids: list[UUID] | None) -> bool:
        with self.condition:
            now = monotonic()
            self.changed[entity_type.lower()] = now
            self.logger.info(f"Notified about change event, type: {entity_type}")
            if uuids is not None:
                self.logger.info(f"Notified about change event, uuids: length == {len(uuids)}")
                self.logger.debug(f"Notified about change event, uuids: {uuids}")
                for uuid in uuids:
                    self.changed[uuid] = now
            old_len = self._drop_old(now)
            self.logger.info(
                f"Notified about change event, added: {len(uuids)}, cache size: {len(self.changed)}, "
                f"trimmed: {old_len - len(self.changed)}"
            )
            self.condition.notify_all()
            return True
        return False

    def reset(self):
        """
        No longer needed, keep it so not all tools need to be updated
        """
        pass

    def _drop_old(self, now: float, exclude: set[UUID] | None = None) -> int:
        old_len = len(self.changed)
        self.changed = {
            uuid: timestamp
            for uuid, timestamp in self.changed.items()
            if now - timestamp < self.max_age and (exclude is None or uuid not in exclude)
        }
        return old_len

    def wait(self, entity: str | UUID | list[str] | list[UUID], timeout: float | None = None):
        """
        Wait for a entity change to be done remotely or timeout is reached

        arguments:
          entity: base type of entity to wait for (Device, Network, ...) or
                  uuid of entity to wait for
                  list of a combination of the two cases above

          timeout: maximal time in seconds to wait

        return:
          True: entity was changed remotely.
          False: timeout was reached.
        """

        start_time = monotonic()
        time_left = timeout
        found = False
        if not isinstance(entity, list):
            entity = [entity]
        required = set()
        for it in entity:
            if isinstance(it, str):
                try:
                    required.add(UUID(it))
                except ValueError:
                    required.add(it.lower())
            else:
                required.add(it)
        self.logger.info(f"Wait for event change {required}, timeout: {timeout}")
        with self.condition:
            self.waiting += 1
            while self.waiting and ((time_left is None) or (time_left > 0)):
                now = monotonic()
                if required.intersection(self.changed.keys()) == required:
                    old_len = self._drop_old(now, required)
                    self.logger.info(
                        f"Done waiting for {len(required)}: all found, remaining {len(self.changed)}, "
                        f"trimmed: {old_len - len(self.changed)}, after {now - start_time:5.1f}"
                    )
                    found = True
                    break
                self.condition.wait(time_left)
                if time_left is not None:
                    time_left = timeout + start_time - now
            if not found:
                self.logger.info(
                    f"Done waiting for {len(required)}: not all found, cache size {len(self.changed)}, "
                    f"after {monotonic() - start_time:5.1f}"
                )
            self.waiting -= 1
        return found
