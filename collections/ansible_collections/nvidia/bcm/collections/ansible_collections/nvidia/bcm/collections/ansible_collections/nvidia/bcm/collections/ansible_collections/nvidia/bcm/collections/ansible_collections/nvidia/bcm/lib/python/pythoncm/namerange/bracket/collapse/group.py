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

from pythoncm.namerange.bracket.collapse.matrix import Matrix
from pythoncm.namerange.bracket.collapse.selection import Selection


class Group:
    FORMAT_SINGLE = '%%0%dd'
    FORMAT_RANGE = '%%0%dd-%%0%dd'

    @classmethod
    def one_dimensional(cls, prefix, length, index):
        grouped = cls._print((prefix[0], length, cls._compress(index)))
        if len(prefix) > 1:
            grouped += prefix[1]
        return grouped

    @classmethod
    def mutli_dimensional(cls, prefix, length, index):
        if len(prefix) > len(length):
            postfix = prefix.pop()
        else:
            postfix = None
        groups = []
        while len(index):
            matrix = Matrix.build(index)
            selection, ranges = Selection.get(matrix)
            index = [it for it in index if it not in set(selection)]
            groups.append(''.join(map(cls._print, list(zip(prefix, length, ranges)))))
        if postfix is not None:
            groups = [it + postfix for it in groups]
        return ','.join(groups)

    @classmethod
    def _print(cls, xxx_todo_changeme):
        (prefix, length, ranges) = xxx_todo_changeme
        one_print_format = cls.FORMAT_SINGLE % length
        if len(ranges) == 1 and ranges[0][0] == ranges[0][1]:
            return prefix + one_print_format % ranges[0][0]
        multi_print_format = cls.FORMAT_RANGE % (length, length)
        groups = []
        for first, last in ranges:
            if first == last:
                groups.append(one_print_format % first)
            else:
                groups.append(multi_print_format % (first, last))
        return prefix + '[' + ','.join(groups) + ']'

    @classmethod
    def _compress(cls, index):
        last = index.pop(0)
        first = last
        count = 1
        compressed = []
        index.append(None)
        for it in index:
            if it is not None and it <= last + 1:
                count += it - last
            else:
                compressed.append((first, last))
                first = it
                count = 1
            last = it
        return compressed
