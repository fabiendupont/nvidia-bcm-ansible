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

import typing

from pythoncm.entity.computenode import ComputeNode

if typing.TYPE_CHECKING:
    from pythoncm.entity.computenode import CloudProvider


class CloudNode(ComputeNode):
    def terminate(self) -> str:
        """
        Terminate the node
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmcloud',
            call='terminate',
            args=[[self.uuid]],
        )
        if code:
            raise OSError(out)
        return out[0]

    @property
    def terminated(self) -> bool:
        return not self.cloudSettings.instanceId

    @property
    def provider(self) -> CloudProvider:
        return self.cloudSettings.provider
