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

from pythoncm.namerange.bracket_expand import BracketExpand
from pythoncm.namerange.dot_dot_expand import DotDotExpand


class Expand:
    @classmethod
    def expand(cls, text_range: str) -> list[str]:
        """
        Expand a text to a list of items.
        """
        if text_range.find('[') > 0:
            return BracketExpand.expand(text_range)

        return DotDotExpand.expand(text_range)
