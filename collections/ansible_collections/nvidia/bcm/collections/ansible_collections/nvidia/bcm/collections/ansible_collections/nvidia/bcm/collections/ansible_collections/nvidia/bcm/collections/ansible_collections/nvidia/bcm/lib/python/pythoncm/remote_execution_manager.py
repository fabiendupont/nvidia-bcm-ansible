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
from uuid import UUID


class RemoteExecutionManager:
    """
    Manages all commands executed on the cluster.
    """

    def __init__(self, cluster):
        self.cluster = cluster
        self.logger = logging.getLogger(__name__)
        self._executors = {}
        self._missed_output = []
        self._condition = threading.Condition()

    def update(self, pid, tracker, node, output, error):
        with self._condition:
            if isinstance(tracker, str):
                tracker = UUID(tracker)
            if tracker in self._executors:
                self.logger.debug(f"Process execution data for, tracker {tracker}, pid {pid}, node {node}")
                self._executors[tracker].process(
                    pid=pid,
                    node=node,
                    output=output,
                    error=error,
                )
            else:
                self.logger.debug("Process execution missed data for, tracker {tracker}, pid {pid}, node {node}")
                self._missed_output.append(
                    {
                        "pid": pid,
                        "tracker": tracker,
                        "node": node,
                        "output": output,
                        "error": error,
                    }
                )

    def register(self, program_runner_status):
        with self._condition:
            tracker = program_runner_status.input.tracker
            self.logger.debug(f"Process execution add tracker {tracker}")
            [
                program_runner_status.process(
                    pid=it.get("pid", 0),
                    node=it.get("node", 0),
                    output=it.get("output", ""),
                    error=it.get("error", ""),
                )
                for it in self._missed_output
                if it["tracker"] == tracker
            ]
            self._missed_output = [it for it in self._missed_output if it["tracker"] != tracker]
            self._executors[tracker] = program_runner_status

    def unregister(self, program_runner_status):
        with self._condition:
            tracker = program_runner_status.input.tracker
            try:
                del self._executors[tracker]
                return True
            except KeyError:
                return False
