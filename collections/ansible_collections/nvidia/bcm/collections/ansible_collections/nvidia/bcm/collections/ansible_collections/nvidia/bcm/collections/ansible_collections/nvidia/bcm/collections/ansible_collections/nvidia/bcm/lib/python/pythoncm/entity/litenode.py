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

from pythoncm.entity import Device


class LiteNode(Device):
    def lite_daemon_package_status(self) -> list[tuple[bool, str, str]] | None:
        """
        Get the status of cm-lite-daemon packages
        """
        result = self._cluster.parallel.lite_daemon_package_status([self])
        if bool(result):
            return result[0]
        return None

    def lite_daemon_install(self, update: bool = True, force: bool = False) -> list[tuple[bool, str, str]] | None:
        """
        Install/update cm-lite-daemon packages
        """
        result = self._cluster.parallel.lite_daemon_install([self])
        if bool(result):
            return result[0]
        return None

    def lite_daemon_remove(self) -> list[tuple[bool, str, str]] | None:
        """
        Remove cm-lite-daemon packages
        """
        result = self._cluster.parallel.lite_daemon_remove([self])
        if bool(result):
            return result[0]
        return None
