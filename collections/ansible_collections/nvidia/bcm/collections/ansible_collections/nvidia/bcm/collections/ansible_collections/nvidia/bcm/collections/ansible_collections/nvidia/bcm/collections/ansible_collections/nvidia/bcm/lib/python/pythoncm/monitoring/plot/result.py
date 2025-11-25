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

import operator
import typing
from bisect import bisect_left
from collections import defaultdict
from time import time
from uuid import UUID

from tabulate import tabulate

from pythoncm import util
from pythoncm.entity.metadata.monitoringdataproducer import MonitoringDataProducer
from pythoncm.key_wrapper import KeyWrapper

if typing.TYPE_CHECKING:
    from pythoncm.entity import Entity
    from pythoncm.entity import MonitoringMeasurable


class Result:
    """
    Monitoring plot result
    """

    GOOD = 0
    DISABLED_MEASURABLE = 1
    DISABLED_PRODUCER = 2
    FILTERED_OUT = 4
    NON_GATHER = 8
    UNDEFINED = -1

    def __init__(self, cluster, request, raw, latest=False, job_info=None):
        self.cluster = cluster
        self.request = request
        self.job_info = job_info
        self.raw = raw
        self._latest = latest
        self._relative_time = False
        self._lookup = None

    @property
    def size(self) -> int:
        """
        Size of the monitoring data
        """
        return len(self.raw.get('items', []))

    @property
    def entities(self) -> list[UUID]:
        """
        List of the unique entities in the monitoring data
        """
        return util.unique((item.get('entity', self.cluster.zero_uuid)) for item in self.raw.get('items', []))

    @property
    def measurables(self) -> list[UUID]:
        """
        List of the unique measurables in the monitoring data
        """
        return util.unique((item.get('measurables', self.cluster.zero_uuid)) for item in self.raw.get('items', []))

    @property
    def series(self) -> dict[tuple[UUID, UUID], list[dict[str, str | float | None]]]:
        result = defaultdict(list)
        for item in self.raw.get('items', []):
            result[
                UUID(item.get('entity', self.cluster.zero_uuid_str)),
                UUID(item.get('measurable', self.cluster.zero_uuid_str)),
            ].append(item)
        return result

    def value(
        self, timestamp: int, entity: UUID | str | Entity, measurable: UUID | str | MonitoringMeasurable
    ) -> float | None:
        if 'items' not in self.raw:
            return None

        if isinstance(entity, str):
            entity = self.cluster.get_by_name(entity)
        if not isinstance(entity, UUID):
            entity = entity.uuid
        if isinstance(measurable, str):
            measurable = self.cluster.get_by_name(measurable, "MonitoringMeasurable")
        if not isinstance(measurable, UUID):
            measurable = measurable.uuid

        if self._lookup is None:
            self._lookup = defaultdict(list)
            for item in self.raw['items']:
                self._lookup[
                    item.get('entity', self.cluster.zero_uuid_str), item.get('measurable', self.cluster.zero_uuid_str)
                ].append((item.get('t1', 0), item))

        items = self._lookup.get((str(entity), str(measurable)), None)
        if items is None:
            return None

        index = bisect_left(KeyWrapper(items, key=operator.itemgetter(0)), timestamp)
        if index >= len(items):
            return None
        upper_bound = items[index][1]
        if upper_bound.get('t0', 0) <= timestamp:
            return upper_bound.get('value', 0)

        if index > 0:
            lower_bound = items[index - 1][1]
            lower_value = lower_bound.get('value', 0)
            upper_value = upper_bound.get('value', 0)
            if lower_value is not None and upper_value is not None:
                lower_t = lower_bound.get('t1', 0)
                upper_t = upper_bound.get('t0', 0)
                diff_t = upper_t - lower_t
                return ((lower_value * (upper_t - timestamp)) + (upper_value * (timestamp - lower_t))) / diff_t

        return None

    def _get_all_info_messages_uuids(self):
        # KDR: note keys are string based, because JS cannot handle 64 bit unsigned numbers
        keys = [it['info'] for it in self.raw['items'] if 'info' in it and it['info'] != '0']
        return list(set(keys))

    def relative_times(self):
        if 'items' not in self.raw:
            return False
        lowest_time = min(item['t0'] for item in self.raw['items'])
        for item in self.raw['items']:
            if 't0' in item:
                item['t0'] -= lowest_time
            if 't1' in item:
                item['t1'] -= lowest_time
        self._relative_time = True
        return True

    def uncompress(self, default_interval=None):
        if 'items' not in self.raw:
            return False
        measurable_intervals = {}
        for it in {item.get('measurable', self.cluster.zero_uuid) for item in self.raw['items']}:
            measurable = self.cluster.get_by_uuid(it)
            if measurable is not None and measurable.producer is not None:
                if measurable.producer.when == MonitoringDataProducer.When.OOB:
                    measurable_intervals[it] = measurable.producer.intervals[-1] * 1000
                else:
                    measurable_intervals[it] = measurable.producer.interval * 1000
        uncompress_items = []
        for item in self.raw['items']:
            uncompress_items.append(item)
            if 't0' in item and 't1' in item and item['t0'] != item['t1']:
                interval = measurable_intervals.get(item.get('measurable', self.cluster.zero_uuid), default_interval)
                if 0 < interval < (item['t1'] - item['t0']):
                    add = int((item['t1'] - item['t0'] - 1) / interval) + 1
                    for i in range(1, add + 1):
                        t = min(item['t0'] + i * interval, item['t1'])
                        new_item = item.copy()
                        new_item['t0'] = t
                        new_item['t1'] = t
                        uncompress_items.append(new_item)
                    item['t1'] = item['t0']
        self.raw['items'] = uncompress_items
        return True

    def table(self, time_format='%Y-%m-%d %H:%M:%S'):
        """
        Format result into a table:
        [(entity, measurable, time, value, *state*, message),
         (entity, measurable, time, value, *state*, message),
         ...
        ]
        state: only if the plot request asked for it
        """
        if 'items' not in self.raw:
            return []
        self.cluster.monitoring.info_message_cache.ensure(self._get_all_info_messages_uuids())
        data = []
        now = time()
        for item in self.raw['items']:
            entity_uuid = item.get('entity', self.cluster.zero_uuid)
            if self.job_info:
                entity_uuid = self.job_info.get_node_uuid_from_node_monitoring_uuid(entity_uuid)
            entity = self.cluster.get_by_uuid(entity_uuid)
            if entity is None:
                entity_name = entity_uuid
            elif isinstance(entity, list):
                entity_name = ', '.join(it.resolve_name for it in entity)
            else:
                entity_name = entity.resolve_name
            measurable_uuid = item.get('measurable', self.cluster.zero_uuid)
            measurable = self.cluster.get_by_uuid(measurable_uuid)
            if measurable is None:
                measurable_name = str(measurable_uuid)
            else:
                measurable_name = measurable.resolve_name
            info = None
            if item.get('now_info'):
                info = item['now_info']
            elif 'info' in item and item['info'] != '0':
                info = self.cluster.monitoring.info_message_cache.get(item['info'])
            value = item.get('value', 0)
            if measurable is not None:
                value = measurable.value_to_string(value)
            if not self._latest:
                data.append(
                    self._data_item(
                        entity_name,
                        measurable_name,
                        now,
                        item.get('t0', 0),
                        time_format,
                        value,
                        info,
                        item.get('state', 0),
                    )
                )
            if self._latest or (item.get('t0', 0) != item.get('t1', 0)):
                data.append(
                    self._data_item(
                        entity_name,
                        measurable_name,
                        now,
                        item.get('t1', 0),
                        time_format,
                        value,
                        info,
                        item.get('state', 0),
                    )
                )
        return (it[0:2] + it[3:] for it in sorted(data))

    def _data_item(self, entity_name, measurable_name, now, timestamp, time_format, value, info, state):
        formatted_timestamp = util.format_milli_seconds_time_stamp(
            value=timestamp,
            now=now,
            time_format=time_format,
            latest=self._latest,
            relative=self._relative_time,
        )
        if self.request.get('include_measurable_status', False):
            return entity_name, measurable_name, timestamp, formatted_timestamp, value, self._translate(state), info

        return entity_name, measurable_name, timestamp, formatted_timestamp, value, info

    @classmethod
    def _translate(cls, state):
        if (state & cls.DISABLED_PRODUCER) or (state & cls.DISABLED_MEASURABLE):
            return 'disabled'
        if state & cls.FILTERED_OUT:
            return 'filtered'
        return ''

    def to_string(self, time_format='%Y-%m-%d %H:%M:%S', table_format='rst', showindex='default'):
        """
        Create a nice formatted table for printing.
        """
        headers = [
            "Entity",
            "Measurable",
            "Age" if self._latest else "Time",
            "Value",
        ]
        if self.request.get('include_measurable_status', False):
            headers.append("State")
        headers.append("Info")
        return tabulate(
            self.table(time_format),
            tablefmt=table_format,
            showindex=showindex,
            headers=headers,
        )
