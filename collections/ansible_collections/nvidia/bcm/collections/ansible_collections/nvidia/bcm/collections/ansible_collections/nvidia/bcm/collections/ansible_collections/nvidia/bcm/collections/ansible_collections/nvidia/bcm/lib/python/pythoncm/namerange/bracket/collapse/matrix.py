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


class Matrix:
    """
    Builds the largest N-dimensional boxes in an M-dimensional matrix
    """

    @classmethod
    def build(cls, elements, dimensions=None):
        """
        Build the matrix
        """
        if dimensions is None:
            dimensions = len(elements[0])
        matrix = dict(
            sorted(
                ((it, [1] * dimensions) for it in elements),
                key=lambda k_v: sum(k_v[0]),
            )
        )

        for i in range(dimensions):
            for index, value in matrix.items():
                cls._update(value, matrix.get(cls._down(index, i), [0] * dimensions), i)
        return matrix

    @classmethod
    def _down(cls, index, dimension):
        return tuple(it - (i == dimension) for i, it in enumerate(index))

    @classmethod
    def _update(cls, work, block, dimension):
        volume_work = 1
        volume_block = 1
        for i in range(dimension):
            volume_work *= work[i]
            volume_block *= block[i]
            if work[i] > block[i]:
                volume_work *= work[dimension]
                volume_block *= block[dimension] + 1
                if volume_work >= volume_block:
                    return
                work[0 : i + 1] = block[0 : i + 1]
        work[dimension] = block[dimension] + 1
