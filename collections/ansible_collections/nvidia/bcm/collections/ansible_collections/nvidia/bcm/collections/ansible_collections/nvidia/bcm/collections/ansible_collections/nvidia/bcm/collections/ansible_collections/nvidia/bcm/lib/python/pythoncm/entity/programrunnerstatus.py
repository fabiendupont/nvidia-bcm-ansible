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
from time import time

from pythoncm.entity.entity import Entity

if typing.TYPE_CHECKING:
    from pythoncm.cluster import Cluster
    from pythoncm.entity_converter import EntityConverter


class ProgramRunnerStatus(Entity):
    PRE_RUNNING = 0
    PRE_QUEUED = 1
    PRE_WAIT_FOR_SEND = 2
    PRE_SOAP_ERROR = 3
    PRE_NODE_DOWN = 4
    PRE_NO_RCM = 5
    PRE_NO_SUCH_DEVICE = 6
    PRE_NO_SUCH_NODE = 7
    PRE_UNKNOWN = 8
    PRE_KILLED = 9
    PRE_STOPPED = 10
    PRE_FINISHED = 11
    PRE_FAILED_TO_STOP = 12
    PRE_STILL_RUNNING = 13
    PRE_BAD_USER = 14
    PRE_FAILED_TO_START = 15
    PRE_NOT_STARTED_YET = 16
    PRE_STATE_MAPPING: typing.ClassVar[dict[int, str]] = {
        PRE_RUNNING: 'Running',
        PRE_QUEUED: 'Queued',
        PRE_WAIT_FOR_SEND: 'Sending',
        PRE_SOAP_ERROR: 'RPC error',
        PRE_NODE_DOWN: 'Node down',
        PRE_NO_RCM: 'No communication layer',
        PRE_NO_SUCH_DEVICE: 'No such device',
        PRE_NO_SUCH_NODE: 'No such node',
        PRE_UNKNOWN: 'Unknown error',
        PRE_KILLED: 'Command killed',
        PRE_STOPPED: 'Node going down',
        PRE_FINISHED: 'Finished',
        PRE_FAILED_TO_STOP: 'Failed to stop',
        PRE_STILL_RUNNING: 'Still running',
        PRE_BAD_USER: 'Bad user name',
        PRE_FAILED_TO_START: 'Failed to start',
        PRE_NOT_STARTED_YET: 'Not started yet',
    }

    def __init__(
        self,
        cluster: Cluster | None = None,
        data: dict[str, typing.Any] | None = None,
        service=None,
        converter: EntityConverter | None = None,
        parent: Entity | None = None,
        add_to_cluster: bool = True,
        create_sub_entities: bool = True,
        **kwargs,
    ) -> None:
        # meta is not allowed
        if "meta" in kwargs:
            raise TypeError(f"'meta' is an invalid keyword argument for {self.__class__.__name__}")

        super().__init__(
            cluster=cluster,
            data=data,
            service=service,
            converter=converter,
            parent=parent,
            add_to_cluster=add_to_cluster,
            create_sub_entities=create_sub_entities,
            **kwargs,
        )
        self._condition = threading.Condition()
        self._node_state: dict[typing.Any, int] = dict(zip(self.nodes, self.state))
        self._node_output: dict[typing.Any, str] = {}
        self._node_error: dict[typing.Any, str] = {}
        self.completed = False

    def _nodes_busy(self) -> int:
        return sum(
            state
            in {
                self.PRE_RUNNING,
                self.PRE_QUEUED,
                self.PRE_STILL_RUNNING,
                self.PRE_NOT_STARTED_YET,
                self.PRE_WAIT_FOR_SEND,
            }
            for state in self._node_state.values()
        )

    def wait(self, timeout: float | None = None) -> bool:
        """
        Wait for a command to complete.
        """
        if timeout is not None:
            start_time = time()
            time_left = timeout
        else:
            time_left = None
        with self._condition:
            while (time_left is None) or (time_left > 0):
                if self.completed or (self._nodes_busy() == 0):
                    break
                self._condition.wait(time_left)
                if time_left is not None:
                    time_left = timeout + start_time - time()
            return (time_left is None) or (time_left > 0)

    def process(self, pid: int, node, output: str = '', error: str = '') -> None:
        """
        Process new data from a node.
        """
        with self._condition:
            if len(output) > 0:
                if node in self._node_output:
                    self._node_output[node] += output
                else:
                    self._node_output[node] = output
            if len(error) > 0:
                if node in self._node_error:
                    self._node_error[node] += error
                else:
                    self._node_error[node] = error
            if pid <= 0:
                self.completed |= pid < 0
                self._node_state[node] = self.PRE_FINISHED
                self._condition.notify()

    def get_output(self, node) -> str | None:
        """
        Get the command output for a specific node.
        """
        with self._condition:
            return self._node_output.get(str(node), None)

    def get_error(self, node) -> str | None:
        """
        Get the command error for a specific node.
        """
        with self._condition:
            return self._node_error.get(str(node), None)

    def get_state(self, node) -> tuple[int | None, str]:
        """
        Get the execution state for a specific node.
        """
        with self._condition:
            state = self._node_state.get(str(node), None)
            if state is not None:
                return state, self.PRE_STATE_MAPPING[state]
            return state, 'Node not part of the execution'

    def kill(self):
        """
        Kill the command on all nodes.
        """

        # CM-18430: load order issue
        from pythoncm.entity.metadata.programrunnerkill import ProgramRunnerKill

        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmproc',
            call='killCommand',
            args=[self.nodes, [self.input.tracker]],
        )
        if code:
            raise OSError(out)
        with self._condition:
            for it in (ProgramRunnerKill(self._cluster, jt) for jt in out):
                try:
                    index = it.trackers.index(self.input.tracker)
                    self._node_state[it.node] = it.results[index]
                except ValueError:
                    self._logger.info('Execute kill, tracker not found')
