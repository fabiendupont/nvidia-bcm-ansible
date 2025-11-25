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

from ply import lex

tokens = (
    'IDENTIFIER',
    'NUMBER',
    'LBRACKET',
    'RBRACKET',
    'COMMA',
    'DASH',
)


def Lexer():
    t_IDENTIFIER = r'[a-zA-Z]+[\-0-9]*'
    t_NUMBER = r'[0-9]+'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_COMMA = r','
    t_DASH = r'\-'

    def t_error(t):
        raise ValueError(f"Illegal character {t.value[0]!r} at line {t.lineno}")

    def _regex():
        """Mostly to make pep8 happy"""
        return [
            t_IDENTIFIER,
            t_NUMBER,
            t_LBRACKET,
            t_RBRACKET,
            t_COMMA,
            t_DASH,
        ]

    return lex.lex()
