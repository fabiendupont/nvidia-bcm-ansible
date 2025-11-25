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

from pythoncm.entity.entity import Entity


class FSPart(Entity):
    def trigger(self):
        """
        Trigger an update of a non image based file system part.
        """
        if self.type == self.meta.Type.IMAGE:
            raise ValueError('This FSPart belongs to an image')
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='triggerFspartUpdate',
            args=[[self.uuid]],
        )
        if code:
            raise OSError(out)
        return out

    def info(self, calculate_size=False):
        """
        Get information about the file system part.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='getFSPartInfo',
            args=[[self.uuid], calculate_size],
        )
        if code:
            raise OSError(out)
        return out

    def lock(self):
        """
        Lock the file system part, so it cannot be used anymore
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='lockFSParts',
            args=[[self.uuid]],
        )
        if code:
            raise OSError(out)
        return out[0]

    def unlock(self):
        """
        Lock the file system part, so it cannot be used anymore
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='unlockFSParts',
            args=[[self.uuid]],
        )
        if code:
            raise OSError(out)
        return out[0]

    def is_locked(self):
        """
        Determine of if the file system part is locked
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmprov',
            call='islockedFSParts',
            args=[self.uuid],
        )
        if code:
            raise OSError(out)
        return out
