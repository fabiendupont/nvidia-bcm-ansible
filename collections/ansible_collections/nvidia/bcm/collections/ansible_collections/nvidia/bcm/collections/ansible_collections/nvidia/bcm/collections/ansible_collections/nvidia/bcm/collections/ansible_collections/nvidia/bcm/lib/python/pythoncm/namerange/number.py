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


class Number:
    @classmethod
    def collapse(cls, numbers: list[int]) -> str:
        parts: list[str] = []
        if bool(numbers):
            numbers.sort()
            first = numbers[0]
            last = first
            for index in [*numbers, None]:
                if index is None or index - last > 1:
                    if first == last:
                        parts.append(str(first))
                    elif first + 1 == last:
                        parts.extend((str(first), str(last)))
                    else:
                        parts.append(f'{first}-{last}')
                    first = index
                    last = index
                else:
                    last = index
        return ','.join(parts)

    @classmethod
    def expand(cls, collapsed: str) -> list[int]:
        result: list[int] = []
        if bool(collapsed):
            for part in collapsed.split(','):
                if '-' in part:
                    first, last = part.split('-', 1)
                    result += range(int(first), int(last) + 1)
                else:
                    result.append(int(part))
        return result
