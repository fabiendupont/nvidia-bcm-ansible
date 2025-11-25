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


class ChargeBackRequest(Entity):
    def report(self, timeout: int | None = None) -> dict:
        """
        Get charge back report for this request
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmjob',
            call='chargeBackByUuid',
            args=[self.uuid],
            timeout=timeout,
        )
        if code:
            raise OSError(out)
        return out
