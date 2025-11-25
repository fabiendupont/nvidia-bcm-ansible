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

import string


class NameNumber:
    @classmethod
    def convert(cls, text: str) -> tuple[str, str]:
        """
        Convert a text to (name, number) tuple
        """
        name = text.rstrip(string.digits)
        number = text[len(name) :]
        return name, number

    @classmethod
    def is_sequential(cls, last: str, current: str) -> bool:
        """
        Determine if two "<name><number>" texts are sequential.
        """
        last_name, last_number = cls.convert(last)
        current_name, current_number = cls.convert(current)
        return (
            (last_name == current_name)
            and (len(last_number) == len(current_number))
            and (int(last_number) + 1 == int(current_number))
        )
