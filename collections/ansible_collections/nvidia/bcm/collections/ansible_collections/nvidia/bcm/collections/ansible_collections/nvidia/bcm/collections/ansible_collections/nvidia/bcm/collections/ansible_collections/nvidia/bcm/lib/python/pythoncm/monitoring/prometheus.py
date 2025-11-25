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

import json
import time


class Prometheus:
    """
    Prometheus
    """

    def __init__(self, cluster):
        self.cluster = cluster

    def time_range(self, start_time: str, end_time: str, gmt: bool = False) -> tuple[int, int]:
        """
        Execute a range PromQL
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='translateGrafanaTimeRange',
            args=[start_time, end_time, gmt],
        )
        if code:
            raise OSError(out)
        return out['start_epoch'], out['end_epoch']

    def instant_query(
        self,
        query: str,
        query_time: int | str = 0,
        exclude_bright: bool = False,
        exclude_prometheus: bool = False,
    ) -> dict | str:
        """
        Execute a instant PromQL
        """
        if not bool(query_time):
            query_time = int(1000 * time.time())
        return self.range_query(
            query=query,
            start_time=query_time,
            end_time=0,
            interval=0,
            exclude_bright=exclude_bright,
            exclude_prometheus=exclude_prometheus,
        )

    def range_query(
        self,
        query: str,
        start_time: int | str,
        end_time: int | str,
        interval: int = 120,
        exclude_bright: bool = False,
        exclude_prometheus: bool = False,
        gmt: bool = False,
    ) -> dict | str:
        """
        Execute a range PromQL
        """
        if isinstance(start_time, str):
            start_time, end_time = self.time_range(start_time, end_time, gmt)
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='executePrometheusQuery',
            args=[
                start_time,
                end_time,
                interval * 1000000,  # PromQL expects nanoseconds
                query,
                'json',
                exclude_bright,
                exclude_prometheus,
            ],
        )
        if code:
            raise OSError(out)
        try:
            return json.loads(out)
        except ValueError:
            return out

    def raw_query(self, query: str) -> str:
        """
        Execute a raw PromQL
        Example: f'api/v1/query?query=loadone&time={int(time.time())}'
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.get(path=f'prometheus/{query}')
        if code:
            raise OSError(out)
        return out
