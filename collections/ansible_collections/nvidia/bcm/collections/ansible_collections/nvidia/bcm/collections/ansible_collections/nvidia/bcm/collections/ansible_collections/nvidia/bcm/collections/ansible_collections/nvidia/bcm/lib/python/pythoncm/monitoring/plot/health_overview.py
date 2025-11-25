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
from time import time
from uuid import UUID

from tabulate import tabulate

from pythoncm import util


class HealthOverview:
    """
    Helper class to display health overview
    """

    zero_uuid = UUID(int=0)

    def __init__(self, cluster):
        self.cluster = cluster
        self.logger = logging.getLogger(__name__)
        self.health_overview = None

    @property
    def alter_level_types(self):
        return ["sum", "count", "maximum"]

    def get_measurables(self):
        alert_level = [
            self.cluster.get_by_name(f"AlertLevel:{it}", "MonitoringMeasurableMetric") for it in self.alter_level_types
        ]
        return [it for it in alert_level if it is not None]

    def update(self, data):
        measurables = {str(it.uuid): it for it in self.get_measurables()}
        info_message_keys = list({it["info"] for it in data.get("items", []) if bool(it.get("info", None))})
        self.cluster.monitoring.info_message_cache.ensure(info_message_keys)
        health_overview = {}
        now = time()
        types = self.alter_level_types
        for item in data.get("items", []):
            entity_uuid = item.get("entity", self.zero_uuid)
            measurable_uuid = item.get("measurable", self.zero_uuid)
            entity = self.cluster.get_by_uuid(entity_uuid)
            if entity is None:
                entity_name = entity_uuid
            else:
                entity_name = entity.resolve_name
            measurable = measurables.get(measurable_uuid, None)
            if measurable is None:
                self.logger.info(f"Measurable not found: {measurable_uuid}")
                continue
            if entity_name not in health_overview:
                timestamp = util.format_milli_seconds_time_stamp(
                    value=item.get("t1", 0),
                    now=now,
                    latest=True,
                )
                info = self.cluster.monitoring.info_message_cache.get(item.get("info", None))
                if info is not None and len(info) > 2 and info[0] == "[" and info[-1] == "]":
                    info = ", ".join([self.cluster.resolve_name_by_uuid(it) for it in info[1:-1].split(",")])
                health_overview[entity_name] = [0, 0, 0, timestamp, info]
            try:
                index = types.index(measurable.parameter)
                health_overview[entity_name][index] = item.get("value", 0)
            except Exception as e:
                self.logger.info(f"Unknown alert level parameter: {measurable.parameter}, error: {e}")
        self.health_overview = [[key, *values] for (key, values) in health_overview.items()]
        self.health_overview.sort()

    def to_string(self, table_format="rst", showindex="default"):
        """
        Create a nice formatted table for printing.
        """
        return tabulate(
            self.health_overview,
            tablefmt=table_format,
            showindex=showindex,
            headers=[
                "Entity",
                "Sum",
                "Count",
                "Maximum",
                "Time",
                "Info",
            ],
        )
