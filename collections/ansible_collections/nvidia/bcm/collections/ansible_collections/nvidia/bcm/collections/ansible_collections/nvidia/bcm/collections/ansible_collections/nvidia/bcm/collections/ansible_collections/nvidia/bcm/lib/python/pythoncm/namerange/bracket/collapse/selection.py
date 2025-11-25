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
import itertools
from operator import add
from operator import mul
from operator import sub

from pythoncm.namerange.bracket.collapse.volumes import Volumes


class Selection:
    @classmethod
    def get(cls, matrix):
        """
        Calculate the elements of the largest selection of volumes
        """
        selection = cls._selection(matrix)
        dimensions = len(selection[0][0])
        selected = [
            itertools.product(
                *[
                    list(range(start[dimension] - size[dimension] + 1, start[dimension] + 1))
                    for dimension in range(dimensions)
                ]
            )
            for start, size in selection
        ]
        elements = [it for group in selected for it in group]
        ranges = [
            sorted({(start[dimension] - size[dimension] + 1, start[dimension]) for start, size in selection})
            for dimension in range(dimensions)
        ]
        return elements, ranges

    @classmethod
    def _selection(cls, matrix):
        """
        Find the largest volumes of compatible fringes
        """
        base_index, base_value, fringes = cls._largest(matrix)
        selection = []
        for index, value in fringes.items():
            base_dimension = cls._dimensions_changed(base_index, index)[0]
            base_diff = tuple(map(sub, index, base_index))
            allowed = True
            extra_fringes = []
            for fringe_index, fringe_value in selection:
                fringe_base_dimension = cls._dimensions_changed(base_index, fringe_index)
                if len(fringe_base_dimension) == 1 and fringe_base_dimension[0] == base_dimension:
                    continue
                desired_value = fringe_value[:]
                desired_value[base_dimension] = value[base_dimension]
                target = tuple(map(add, fringe_index, base_diff))
                target_value = matrix.get(target, None)
                if desired_value == target_value:
                    extra_fringes.append((target, target_value))
                else:
                    allowed = False
                    break
            if allowed:
                selection.append((index, value))
                selection += extra_fringes
        selection.append((base_index, base_value))
        return selection

    @classmethod
    def _largest(cls, matrix):
        candidates = []
        for group in Volumes.largest(matrix):
            for base_index, base_value in group:
                fringes = [
                    (index, value)
                    for (index, value) in matrix.items()
                    if cls._compatible(base_index, base_value, index, value)
                ]
                fringes.sort(key=lambda index_value: functools.reduce(mul, index_value[1]), reverse=True)
                fringes_dict = dict(cls._exclusive(fringes))
                fringe_volume = sum(functools.reduce(mul, value) for value in fringes_dict.values())
                candidates.append(
                    [
                        (functools.reduce(mul, base_value), fringe_volume),
                        (base_index, base_value),
                        fringes_dict,
                    ]
                )
        (_volume, _fringe_volume), (base_index, base_value), fringes = max(candidates)
        return base_index, base_value, fringes

    @classmethod
    def _dimensions_changed(cls, a, b):
        return [i for i, (it, jt) in enumerate(zip(a, b)) if it != jt]

    @classmethod
    def _compatible(cls, base_index, base_value, index, value):
        if index == base_index:
            return False
        change_value = cls._dimensions_changed(base_value, value)
        if len(change_value) > 1:
            return False
        change_index = cls._dimensions_changed(base_index, index)
        if len(change_index) != 1:
            return False
        dimension = change_index[0]
        if len(change_value) > 0 and dimension != change_value[0]:
            return False
        if base_index[dimension] >= index[dimension]:
            return (base_index[dimension] - base_value[dimension]) > index[dimension]

        return (index[dimension] - value[dimension]) > base_index[dimension]

    @classmethod
    def _overlap(cls, base_index, base_value, index, value):
        change_index = cls._dimensions_changed(base_index, index)
        if len(change_index) == 1:
            dimension = change_index[0]
            if base_index[dimension] >= index[dimension]:
                return (base_index[dimension] - base_value[dimension]) <= index[dimension]

            return (index[dimension] - value[dimension]) <= base_index[dimension]
        return False

    @classmethod
    def _exclusive(cls, fringes):
        exclusive = []
        for index, value in fringes:
            if not any(cls._overlap(base_index, base_value, index, value) for base_index, base_value in exclusive):
                exclusive.append((index, value))
        return exclusive
