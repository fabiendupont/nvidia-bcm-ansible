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


class Compress:
    """
    Calculates a compression scheme for the indexes
    """

    def __init__(self, elements, dimensions=None):
        if dimensions is None:
            self.dimensions = len(elements[0])
        else:
            self.dimensions = dimensions
        self.backward = [sorted({it[self.dimension] for it in elements}) for _dimension in range(self.dimensions)]
        self.forward = [
            {it: i for i, it in enumerate(self.backward[self.dimension])} for _dimension in range(self.dimensions)
        ]

    def compress(self, data):
        pass

    def decompress(self, data):
        pass
