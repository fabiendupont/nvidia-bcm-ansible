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

import logging


class EnumValueCache:
    """
    Cache to translate monitoring values to enum strings.
    """

    def __init__(self, cluster):
        self.cluster = cluster
        self.logger = logging.getLogger(__name__)
        self.measurable_key_value = {}

    def update(self):
        """
        Update all enum index to value mappings
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='getEnumIndexValues',
        )
        if code:
            self.logger.warning(f'Error retrieving enum values {out}')
            return 0

        out = list(
            zip(
                out['measurables'],
                out['index'],
                out['values'],
            )
        )
        self.measurable_key_value.update({(it[0], it[1]): it[2] for it in out})
        self.logger.debug('Update enum cache: %d / %d', len(out), len(self.measurable_key_value))
        return len(out)

    def get(self, measurable, key):
        """
        Get the value for a measurable.
        """
        return self.measurable_key_value.get((measurable, key), key)
