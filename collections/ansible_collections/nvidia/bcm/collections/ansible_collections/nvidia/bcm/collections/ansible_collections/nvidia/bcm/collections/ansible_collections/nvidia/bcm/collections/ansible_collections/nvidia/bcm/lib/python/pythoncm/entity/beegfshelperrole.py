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

from pythoncm.entity import Role


class BeeGFSHelperRole(Role):
    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"configurations={[conf.resolve_name if conf else conf for conf in self.configurations]}"
            f") at 0x{id(self):X}>"
        )
