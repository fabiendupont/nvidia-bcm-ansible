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


class ReportQuery(Entity):
    def run(self, parameters: dict | None = None):
        if parameters is None:
            parameters = {}
        parameters['key'] = self.uuid
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='reportQuery',
            **parameters,
        )
        if code:
            raise OSError(out)
        return out
