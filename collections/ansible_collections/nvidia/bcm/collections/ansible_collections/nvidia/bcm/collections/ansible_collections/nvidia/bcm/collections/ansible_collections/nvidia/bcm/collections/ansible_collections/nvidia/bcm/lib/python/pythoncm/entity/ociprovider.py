#
# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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

from pythoncm.entity import CloudProvider


class OCIProvider(CloudProvider):
    def get_gpu_memory_fabrics(self):
        service_name = "cmcloud"
        method_name = "getOCIGPUMemoryFabrics"
        code, out = self._cluster.get_rpc().call(service_name, method_name, provider_uuid=self.uuid)
        if code:
            raise OSError(f"{service_name}.{method_name} failed: {out}")
        return out
