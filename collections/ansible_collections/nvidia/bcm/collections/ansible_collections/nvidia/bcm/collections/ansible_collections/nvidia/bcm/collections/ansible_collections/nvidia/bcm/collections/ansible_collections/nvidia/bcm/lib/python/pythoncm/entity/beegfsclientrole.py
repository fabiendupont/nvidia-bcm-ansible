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

from pythoncm.entity.role import Role

if typing.TYPE_CHECKING:
    from collections.abc import Sequence


class BeeGFSClientRole(Role):
    @property
    def mountpoints(self) -> Sequence[str]:
        return tuple(
            configuration.beegfs_cluster.mountpoint
            for configuration in self.configurations
            if configuration is not None and configuration.beegfs_cluster is not None
        )

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__}("
            f"configurations={[conf.resolve_name if conf else conf for conf in self.configurations]}"
            f") at 0x{id(self):X}>"
        )
