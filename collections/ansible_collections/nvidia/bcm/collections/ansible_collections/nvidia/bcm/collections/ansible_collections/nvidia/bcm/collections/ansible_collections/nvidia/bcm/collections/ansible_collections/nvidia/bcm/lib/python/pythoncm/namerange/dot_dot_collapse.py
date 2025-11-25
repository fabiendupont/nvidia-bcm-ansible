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

import typing

import natsort

from pythoncm.namerange.name_number import NameNumber

if typing.TYPE_CHECKING:
    from collections.abc import Sequence


class DotDotCollapse:
    @classmethod
    def collapse(cls, items: Sequence[str]) -> str:
        """
        ['node001'] => 'node001'
        ['node001', 'node003'] => 'node001,node003'
        ['node001', 'node002', 'node003'] => 'node001..node003'
        """
        if len(items) == 0:
            return ''
        groups = []
        work_items: list[str | None] = natsort.natsorted(set(items))
        work_items.append(None)
        first = work_items.pop(0)
        last = first
        count = 1
        for current in work_items:
            if current is not None and NameNumber.is_sequential(last, current):
                count += 1
            else:
                if count == 1:
                    groups.append(last)
                elif count == 2:
                    groups.append(f"{first},{last}")
                else:
                    groups.append(f"{first}..{last}")
                count = 1
                first = current
            last = current
        return ','.join(groups)
