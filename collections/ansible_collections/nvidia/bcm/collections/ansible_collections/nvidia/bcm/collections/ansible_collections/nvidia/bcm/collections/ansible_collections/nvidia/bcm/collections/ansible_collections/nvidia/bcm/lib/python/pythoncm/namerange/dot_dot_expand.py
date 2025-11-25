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

import itertools

import natsort

from pythoncm.namerange.name_number import NameNumber


class DotDotExpand:
    """
    Expand texts to a list of items
    """

    @classmethod
    def expand(cls, text_range: str) -> list[str]:
        """
        'node001' => ['node001']
        'node001,node003' => ['node001', 'node003']
        'node001..node003' => ['node001', 'node002', 'node003']
        """
        groups = [it.strip() for it in text_range.split(',')]
        expanded = itertools.chain.from_iterable(cls.__expand_dot_dot_group(it) for it in groups)
        return natsort.natsorted(set(expanded))

    @classmethod
    def __expand_dot_dot_group(cls, group):
        index = group.find('..')
        if index >= 0:
            start = group[0:index]
            end = group[index + 2 :]
            start_name, start_str_index = NameNumber.convert(start)
            end_name, end_str_index = NameNumber.convert(end)
            if start_name != end_name:
                raise ValueError(f'Names in .. format not equal: {start_name}, {end_name}')
            start_index, end_index = int(start_str_index), int(end_str_index)
            if start_index > end_index:
                raise ValueError(f'Negative range in .. format not equal: {start_index}, {end_index}')
            if len(start_str_index) == len(end_str_index):
                digits = len(start_str_index)
                return [f"{start_name}{it:0{digits}d}" for it in range(start_index, end_index + 1)]
            return [f"{start_name}{it}" for it in range(start_index, end_index + 1)]
        if len(group):
            return [group]
        return []
