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

from enum import Enum
from enum import auto

from pythoncm.entity import Entity


class LabeledEntity(Entity):
    @property
    def labels(self) -> dict:
        class State(Enum):
            KEY = auto()
            VALUE = auto()

        state = State.KEY
        start = 0
        slash_count = 0
        quoted = False
        labels = {}
        for index, c in enumerate(self.name + ','):
            even_slash_count = slash_count % 2 == 0
            if c == '\\':
                slash_count += 1
            elif even_slash_count and not quoted and c == '=' and state == State.KEY:
                key = self.name[start:index]
                start = index + 1
                state = State.VALUE
            elif even_slash_count and not quoted and c == ',' and state == State.VALUE:
                value = self.name[start:index]
                if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
                    value = value[1:-1]
                start = index + 1
                state = State.KEY
                labels[key] = value
            elif even_slash_count and c == '"':
                quoted = not quoted
        return labels
