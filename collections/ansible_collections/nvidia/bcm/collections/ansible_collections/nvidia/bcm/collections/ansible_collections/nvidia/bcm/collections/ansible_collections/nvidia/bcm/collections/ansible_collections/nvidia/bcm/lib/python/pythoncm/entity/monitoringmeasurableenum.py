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

import math
import typing

from pythoncm.entity.monitoringmeasurable import MonitoringMeasurable


class MonitoringMeasurableEnum(MonitoringMeasurable):
    def value_to_string(self, value: str | typing.SupportsFloat | None) -> str:
        """
        Translate a raw value to string
        """
        if value is None or math.isnan(value):
            return MonitoringMeasurable.NO_DATA
        return self._cluster.monitoring.enum_value_cache.get(self.uuid, value)

    def is_enum_metric(self) -> bool:
        return True
