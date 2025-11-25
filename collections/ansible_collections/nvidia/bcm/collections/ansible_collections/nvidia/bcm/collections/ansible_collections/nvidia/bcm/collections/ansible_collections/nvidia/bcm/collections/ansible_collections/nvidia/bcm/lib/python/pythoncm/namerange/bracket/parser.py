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

from ply import yacc

from pythoncm.namerange.bracket.lexer import tokens  # noqa: F401


def Parser():
    start = 'list'

    def p_list(p):
        """list : blocks"""
        p[0] = p[1]

    def p_blocks(p):
        """blocks : blocks COMMA block
        | block
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_block(p):
        """block : block groups
        | groups
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1] + p[3]

    def p_groups(p):
        """groups : groups group
        | group
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[2]]

    def p_group(p):
        """group : IDENTIFIER LBRACKET sequence RBRACKET
        | IDENTIFIER
        """
        if len(p) == 2:
            p[0] = p[1], None
        else:
            p[0] = p[1], p[3]

    def p_sequence(p):
        """sequence : sequence COMMA range
        | range
        """
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[1] + [p[3]]

    def p_range(p):
        """range : NUMBER DASH NUMBER
        | NUMBER
        """
        if len(p) == 2:
            p[0] = p[1]
        else:
            p[0] = p[1], p[3]

    def p_error(p):
        raise ValueError(f"Illegal character {p.value[0]!r} at line {p.lexpos}")

    return yacc.yacc(start=start, write_tables=False, debug=False)
