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

from time import time

from pythoncm.entity.entity import Entity


class CMDaemonFailoverGroup(Entity):
    def status(self):
        """
        Get the status of all the HA group
        """
        # CM-18430: load order issue
        from pythoncm.entity import CMDaemonFailoverGroupStatus

        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmpart',
            call='getCMDaemonFailoverGroupStatus',
            args=[self.uuid],
        )
        if code:
            raise OSError(out)
        return CMDaemonFailoverGroupStatus(self, out)

    def wait(self, timeout=None):
        """
        Wait for a command to complete.
        """
        if timeout is not None:
            start_time = time()
            time_left = timeout
        else:
            time_left = None
        while (time_left is None) or (time_left > 0):
            status = self.status()
            if status is None or not status.failoverThreadRunning:
                break
            time.sleep(1)
            if time_left is not None:
                time_left = timeout + start_time - time()
        return (time_left is None) or (time_left > 0)
