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


class RemoteNodeInstallerInteraction(Entity):
    def confirm(
        self,
        passphrase: str | None = None,
    ) -> bool:
        """
        Confirm an interaction
        """
        if self.wasDenied:
            raise ValueError('Already denied')
        if passphrase is not None:
            if self.type != self.meta.Type.DISK_ENCRYPTION_PASSPHRASE:
                raise TypeError('Passphrase can only be set for a disk encryption interaction')
            self.payload = passphrase
        self.wasConfirmed = True
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='updateRemoteNodeInstallerInteractions',
            args=[self.to_dict()],
        )
        if code:
            raise OSError(out)
        if isinstance(out, list) and bool(out):
            return self._merge_updated(RemoteNodeInstallerInteraction(self._cluster, out[0]))
        return False

    def deny(self) -> bool:
        """
        Deny an interaction
        """
        if self.wasConfirmed:
            raise ValueError('Already confirmed')
        self.wasDenied = True
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='updateRemoteNodeInstallerInteractions',
            args=[self.to_dict()],
        )
        if code:
            raise OSError(out)
        if isinstance(out, list) and bool(out):
            return self._merge_updated(RemoteNodeInstallerInteraction(self._cluster, out[0]))
        return False
