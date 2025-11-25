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
from pythoncm.entity.prototype.externaloperationresult import ExternalOperationResult

if typing.TYPE_CHECKING:
    from pythoncm.entity import DPUSettings


class DPUNode(ComputeNode):
    def final_dpu_settings(self) -> DPUSettings | None:
        if bool(self.dpuSettings):
            return self.dpuSettings
        if bool(self.category) and bool(self.category.dpuSettings):
            return self.dpuSettings
        if bool(self.partition):
            return self.partition.self.dpuSettings
        return None

    def list_bfb(self, debug: bool = False) -> list[str]:
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service="cmdevice",
            call="dpuListBfb",
            args=[debug],
        )
        if code:
            raise OSError(out)
        if not out.get("success", False):
            raise ValueError(out.get("error_message", ""))
        return out.get("names", [])

    def push_bfb(self, path: str, debug: bool = False) -> ExternalOperationResult:
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service="cmdevice",
            call="dpuPushBfb",
            args=[[self.uuid], path, debug],
        )
        if code:
            raise OSError(out)
        if len(out) != 1:
            raise ValueError(out)
        return ExternalOperationResult(self._cluster, out[0], self)

    def show(self, debug: bool = False) -> ExternalOperationResult:
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service="cmdevice",
            call="dpuShow",
            args=[[self.uuid], debug],
        )
        if code:
            raise OSError(out)
        if len(out) != 1:
            raise ValueError(out)
        return ExternalOperationResult(self._cluster, out[0], self)

    def apply(self, debug: bool = False) -> ExternalOperationResult:
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service="cmdevice",
            call="dpuApply",
            args=[[self.uuid], debug],
        )
        if code:
            raise OSError(out)
        if len(out) != 1:
            raise ValueError(out)
        return ExternalOperationResult(self._cluster, out[0], self)

    def discover(self, debug: bool = False) -> ExternalOperationResult:
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service="cmdevice",
            call="dpuDiscover",
            args=[[self.uuid], debug],
        )
        if code:
            raise OSError(out)
        if len(out) != 1:
            raise ValueError(out)
        return ExternalOperationResult(self._cluster, out[0], self)

    def boot_order(self, reboot: bool = True, debug: bool = False) -> ExternalOperationResult:
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service="cmdevice",
            call="dpuBootOrder",
            args=[[self.uuid], reboot, debug],
        )
        if code:
            raise OSError(out)
        if len(out) != 1:
            raise ValueError(out)
        return ExternalOperationResult(self._cluster, out[0], self)
