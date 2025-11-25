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
import re
import time
import typing


class GrafanaTime:
    """
    Grafana style time format parsing

    See https://docs.grafana.org/reference/timerange/

    Example Relative Range | From:    | To:
    -----------------------+----------+---------
    Last 5 minutes         | now-5m   | now
    The day so far         | now/d    | now
    This week              | now/w    | now/w
    Week to date           | now/w    | now
    Previous Month         | now-1M/M | now-1M/M
    """

    START = 0
    END = 1

    SECOND = 1
    MINUTE = 60
    HOUR = 60 * MINUTE
    DAY = 24 * HOUR
    WEEK = 7 * DAY
    MONTH = 31 * DAY
    YEAR = 365 * DAY

    UNITS: typing.ClassVar[dict[str, int]] = {
        's': SECOND,
        'm': MINUTE,
        'h': HOUR,
        'd': DAY,
        'w': WEEK,
        'M': MONTH,
        'y': YEAR,
    }

    def __init__(self, now=None):
        if now is None:
            self.now = time.time()
        else:
            self.now = now

    def parse_range(self, start, end):
        """
        Parse a time range.
        """
        return (
            self._parse_timestamp(start, self.START),
            self._parse_timestamp(end, self.END),
        )

    def parse_timestamp(self, timestamp):
        """
        Parse one timestamp.
        """
        return self._parse_timestamp(timestamp, self.START)

    def _parse_timestamp(self, timestamp, side):
        try:
            return float(timestamp)
        except ValueError:
            pass

        match = re.match(r"^(now)(([-+][0-9]+)+([smhdwMy]))?(/([smhdwMy]))?$", timestamp)
        if match is None:
            raise ValueError(f'Invalid syntax: {timestamp}')

        result = self.now

        if match.group(3) is not None and match.group(4) is not None:
            result += self._parse_unit(int(match.group(3)), match.group(4))

        if match.group(6) is not None:
            result = self._round_to_unit(result, match.group(6), side)

        return result

    @classmethod
    def _parse_unit(cls, offset, unit):
        return offset * cls.UNITS[unit]

    @classmethod
    def _round_to_unit(cls, timestamp, unit, side):
        step = cls.UNITS[unit]
        timestamp = step * math.floor(timestamp / step)
        return timestamp + side * (step - 1)
