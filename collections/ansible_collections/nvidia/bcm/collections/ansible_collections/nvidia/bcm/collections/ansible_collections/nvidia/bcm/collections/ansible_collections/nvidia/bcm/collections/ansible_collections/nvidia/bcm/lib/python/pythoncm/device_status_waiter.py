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

import inspect
import threading
import typing
from time import monotonic

from pythoncm.entity_converter import EntityConverter
from pythoncm.util import uuid_compare

if typing.TYPE_CHECKING:
    from uuid import UUID

    from pythoncm.device_status_waiter_manager import DeviceStatusWaiterManager


class DeviceStatusWaiterTimeoutError(Exception):
    """
    Exception raised when a device status waiter times out waiting for the device to reach its desired state.
    """


class DeviceStatusWaiter:
    """
    Manages the state of a device.
    Making it easy to wait for a device to arrive in a specific state.
    """

    def __init__(self, manager: DeviceStatusWaiterManager, device: UUID, states):
        self._manager = manager
        self._device = device
        if not isinstance(states, list) and not inspect.isfunction(states):
            self._states = [states]
        else:
            self._states = states
        self._waiting = False
        self._condition = threading.Condition()
        self._received_states = []
        self._converter = EntityConverter(self._manager.cluster, service=None)

    def process(self, status):
        """
        Process a state change of a device.
        """
        with self._condition:
            if uuid_compare(status['ref_device_uuid'], self._device) and self._waiting:
                self._received_states.append(status)
                self._condition.notify()

    def wait(self, timeout: int | None = None, raise_on_timeout: bool = False) -> bool:
        """
        Wait for the device to enter the desired state.

        :param timeout: The amount of time to wait (in seconds) before timing out on waiting to reach the desired state.
                        If None, wait indefinitely.
        :type timeout: int or None

        :param raise_on_timeout: If True, raises a DeviceStatusWaiterManagerTimeoutError when the waiter times out
                                 waiting for the desired state. If False, returns False when the waiter times out.
        :type raise_on_timeout: bool

        :return: True if the device entered the desired state before the timeout, False otherwise.
        :rtype: bool

        :raises DeviceStatusWaiterManagerTimeoutError: If the wait times out and raise_on_timeout is set to True.
        """
        if not self._states:
            return True
        start_time = monotonic()
        time_left = timeout
        rpc = self._manager.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmstatus',
            call='getStatus',
            args=[self._device],
        )
        if code:
            raise OSError(out)
        with self._condition:
            self._received_states.append(out)
            self._waiting = True
            while (time_left is None) or (time_left > 0):
                if isinstance(self._states, list):
                    while self._states and self._received_states:
                        latest = self._received_states.pop(0)
                        latest = self._converter.convert(latest)
                        if self._states[0] == latest.final_status:
                            self._states.pop(0)
                else:
                    while self._received_states:
                        latest = self._received_states.pop(0)
                        latest = self._converter.convert(latest)
                        if self._states(latest):
                            self._states = None
                            break
                if not bool(self._states):
                    break
                self._condition.wait(time_left)
                if time_left is not None:
                    time_left = timeout + start_time - monotonic()
        self._manager._completed(self)
        ok = (time_left is None) or (time_left > 0)
        if not ok and raise_on_timeout:
            raise DeviceStatusWaiterTimeoutError()

        return ok
