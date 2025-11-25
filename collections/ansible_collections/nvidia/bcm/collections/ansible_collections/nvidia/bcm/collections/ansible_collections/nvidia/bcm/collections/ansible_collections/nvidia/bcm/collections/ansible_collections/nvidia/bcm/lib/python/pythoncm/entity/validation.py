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


class Validation(Entity):
    @property
    def level(self) -> str:
        if self.severity == self.meta.Severity.ERROR:
            return 'error'
        if self.severity == self.meta.Severity.FORCE:
            return 'force warning'
        return 'warning'

    @property
    def error(self) -> bool:
        return self.severity == self.meta.Severity.ERROR
