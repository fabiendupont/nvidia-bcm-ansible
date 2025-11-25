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

from pythoncm.namerange.bracket_collapse import BracketCollapse
from pythoncm.namerange.dot_dot_collapse import DotDotCollapse


class Collapse:
    DOT_DOT = 0
    BRACKET = 1

    @classmethod
    def collapse(cls, items: list[str], method=DOT_DOT) -> str:
        """
        Collapse a list of items to text.
        """
        if method == cls.DOT_DOT:
            return DotDotCollapse.collapse(items)

        return BracketCollapse.collapse(items)
