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
import re

from pythoncm.namerange.bracket.collapse.group import Group


class Collapse:
    @classmethod
    def collapse(cls, items):
        result = []
        for key, grouper in cls._groups(sorted(items)):
            index = [tuple(map(int, it[1::2])) for it in grouper]
            offset = int((len(key) + 1) / 2)
            prefix = key[0:offset]
            length = key[offset:]
            if len(index[0]) == 0:
                result.append(prefix[0])
            elif len(index[0]) == 1:
                result.append(
                    Group.one_dimensional(
                        prefix,
                        length[0],
                        [it[0] for it in index],
                    )
                )
            else:
                result.append(
                    Group.mutli_dimensional(
                        prefix,
                        length,
                        index,
                    )
                )
        return ','.join(result)

    @classmethod
    def __sort_function(cls, it):
        return it[0::2] + [len(jt) for jt in it[1::2]]

    @classmethod
    def _groups(cls, items):
        split = [[it for it in re.split(r'(\d+)', jt) if len(it)] for jt in items]
        split.sort(key=cls.__sort_function)
        return itertools.groupby(split, cls.__sort_function)
