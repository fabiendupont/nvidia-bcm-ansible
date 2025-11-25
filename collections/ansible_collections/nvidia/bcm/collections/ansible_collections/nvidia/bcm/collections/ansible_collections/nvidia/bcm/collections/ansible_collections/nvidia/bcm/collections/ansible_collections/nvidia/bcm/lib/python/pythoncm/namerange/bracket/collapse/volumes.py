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

import functools
from operator import mul


class Volumes:
    """
    Calculate the volumes in the M-dimensional matrix
    """

    @classmethod
    def largest(cls, matrix):
        """
        Yield all volumes with the maximal size
        """
        return cls._largest_groups(list(matrix.items()), key=lambda index_value: functools.reduce(mul, index_value[1]))

    @classmethod
    def to_list(cls, groups):
        return [it for group in groups for it in group]

    @classmethod
    def _largest_groups(cls, sequence, key=lambda x: x):
        largest = None
        indexes = []
        for i, elem in enumerate(sequence):
            index = key(elem)
            if largest is None or index > largest:
                largest = index
                indexes = [i]
            elif index == largest:
                indexes.append(i)
        yield (sequence[i] for i in indexes)
