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


class SysInfoCollector(Entity):
    @property
    def cpu_count(self) -> int:
        return len(self.cpus)

    @property
    def cpu_core_count(self) -> int:
        return sum(cpu.cores for cpu in self.cpus)

    @property
    def gpu_count(self) -> int:
        return len(self.gpus)

    @property
    def gpu_nvlink(self):
        return any(it.nvlinkUp > 0 for it in self.gpus)

    def _brand_gpu_count(self, name: str) -> int:
        return sum(name.upper() in it.brand.upper() or name.upper() in it.name.upper() for it in self.gpus)

    @property
    def nvidia_gpu_count(self) -> int:
        return self._brand_gpu_count("NVIDIA")

    @property
    def amd_gpu_count(self) -> int:
        return self._brand_gpu_count("AMD")

    @property
    def intel_gpu_count(self) -> int:
        return self._brand_gpu_count("Intel")

    @property
    def interconnect_count(self) -> int:
        count = 0
        for interconnect in self.interconnects:
            idx = interconnect.find("*")
            count += 1 if idx < 0 else int(interconnect[:idx].strip())
        return count
