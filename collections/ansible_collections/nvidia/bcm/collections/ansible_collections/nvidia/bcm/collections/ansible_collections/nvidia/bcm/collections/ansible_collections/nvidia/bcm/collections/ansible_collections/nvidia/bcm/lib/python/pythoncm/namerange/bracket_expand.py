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

from pythoncm.namerange.bracket.lexer import Lexer
from pythoncm.namerange.bracket.parser import Parser


class BracketExpand:
    """
    Expand texts to a list of items
    """

    parser = Parser()
    lexer = Lexer()

    @classmethod
    def expand(cls, text_range: str) -> list[str]:
        """
        'node001' => ['node001']
        'node001,node003' => ['node001', 'node003']
        'node[001-003]' => ['node001', 'node002', 'node003']
        """
        if not text_range:
            return []
        parsed = cls.parser.parse(text_range, lexer=cls.lexer)
        cls.__check(parsed)
        return natsort.natsorted(set(cls.__expand(parsed)))

    @classmethod
    def __check(cls, parsed):
        [cls.__check_ranges(it[1]) for group in parsed for it in group]

    @classmethod
    def __check_ranges(cls, ranges):
        if ranges is not None:
            for number in ranges:
                if isinstance(number, tuple):
                    if len(number[0]) != len(number[1]) and number[0][0] == '0':
                        raise ValueError('Incompatible range: %s', number)

                    first = int(number[0])
                    last = int(number[1])
                    if first > last:
                        raise ValueError(f'Invalid range: {first} > {last}')

    @classmethod
    def __expand(cls, parsed):
        expanded = []
        for group in parsed:
            ranges = list(itertools.starmap(cls.__expand_ranges, group))
            expanded += list(map(''.join, itertools.product(*ranges)))
        return expanded

    @classmethod
    def __expand_ranges(cls, prefix, ranges):
        expanded = []
        if ranges is None:
            expanded.append(prefix)
        else:
            for it in ranges:
                if isinstance(it, tuple):
                    first = int(it[0])
                    last = int(it[1])
                    if len(it[0]) == len(it[1]):
                        expanded.extend(f"{prefix}{index:0{len(it[0])}d}" for index in range(first, last + 1))
                    else:
                        expanded.extend(f"{prefix}{index:d}" for index in range(first, last + 1))
                else:
                    expanded.append(prefix + it)
        return expanded
