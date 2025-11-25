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

from pythoncm.entity.monitoringmeasurable import MonitoringMeasurable


class MonitoringMeasurableMetric(MonitoringMeasurable):
    def value_to_string(self, value: float | None, cumulative=False) -> str:
        """
        Translate a raw value to string
        """
        if value is None or math.isnan(value):
            return MonitoringMeasurable.NO_DATA
        if self.unit == '%':
            value *= 100
            value = f'{value:6.2f}%'
        else:
            try:
                import humanfriendly

                if self.unit in {'B', 'B/s'}:
                    value = humanfriendly.format_size(value, binary=True)
                elif self.unit == 's':
                    value = humanfriendly.format_timespan(value)
                else:
                    value = humanfriendly.format_number(value) + ' ' + self.unit
            except ImportError:
                if self.unit:
                    if isinstance(value, float):
                        value = f'{value:8.5f} {self.unit}'
                    else:
                        value = f'{value:d} {self.unit}'
            if not cumulative and self.cumulative and (self.unit[-2:] != '/s'):
                value += '/s'
        return value

    def is_metric(self) -> bool:
        return True
