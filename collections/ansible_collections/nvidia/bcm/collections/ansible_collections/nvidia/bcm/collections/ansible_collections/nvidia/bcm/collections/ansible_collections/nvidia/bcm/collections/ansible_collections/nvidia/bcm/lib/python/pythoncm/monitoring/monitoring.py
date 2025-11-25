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

import typing
from enum import Enum
from enum import auto
from uuid import UUID

from pythoncm.entity import MonitoringDataProducer
from pythoncm.entity import MonitoringPickupInterval
from pythoncm.entity import MonitoringSubSystemInfo
from pythoncm.monitoring.enum_value_cache import EnumValueCache
from pythoncm.monitoring.info_message_cache import InfoMessageCache
from pythoncm.monitoring.plot.health_overview import HealthOverview
from pythoncm.monitoring.plot.result import Result
from pythoncm.monitoring.prometheus import Prometheus

if typing.TYPE_CHECKING:
    from pythoncm.entity import Entity
    from pythoncm.entity import MonitoringMeasurable
    from pythoncm.entity import Node


class Monitoring:
    class Operation(Enum):
        NONE = auto()
        SUM = auto()
        AVG = auto()
        MAX = auto()
        MIN = auto()
        COUNT = auto()

    class OperationGroup(Enum):
        NONE = auto()
        BOTH = auto()
        ENTITY = auto()
        MEASURABLE = auto()

    class Algorithm(Enum):
        LAST = auto()
        LINEAR = auto()
        SUM = auto()
        AVG = auto()
        MAX = auto()
        MIN = auto()
        OUTLIER = auto()

    def __init__(self, cluster):
        self.cluster = cluster
        self.prometheus = Prometheus(self.cluster)
        self.info_message_cache = InfoMessageCache(self.cluster)
        self.enum_value_cache = EnumValueCache(self.cluster)

    def connect(self):
        self.enum_value_cache.update()

    def _get_all_entities(self, timeout=None):
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='getMonitoredEntities',
            timeout=timeout,
        )
        if code:
            raise OSError(out)
        return out

    def _get_all_measurables(self, entities, timeout=None):
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='getMonitoringMeasurablesForEntities',
            args=[entities],
            timeout=timeout,
        )
        if code:
            raise OSError(out)
        measurables = out.get('measurables', [])
        return list(set(measurables))

    def _get_entities_measurables(self, entities, measurables, timeout=None):
        if entities is None:
            entities = self._get_all_entities(timeout)
        else:
            entities = self.cluster._entities_to_uuids(entities)
        if measurables is None:
            measurables = self._get_all_measurables(entities, timeout)
        else:
            measurables = self.cluster._entities_to_uuids(measurables)
        return entities, measurables

    def get_all_entity_measurables(
        self, include_labeled_entities: bool = True, include_jobs: bool = True, timeout: int | None = None
    ) -> tuple[list[UUID], list[UUID]]:
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='getAllEntityMeasurables',
            args=[include_labeled_entities, include_jobs],
            timeout=timeout,
        )
        if code:
            raise OSError(out)
        return ([UUID(it) for it in out.get('entities', [])], [UUID(it) for it in out.get('measurables', [])])

    def dump_monitoring_data(
        self,
        entities: list[UUID | Entity],
        start_time: int,
        end_time: int,
        measurables: list[UUID | Entity] | None = None,
        intervals: int = 0,
        timeout: int | None = None,
        clip: bool = False,
        uncompress: bool = False,
        pair_wise: bool = False,
        algorithm: Algorithm | None = None,
        operation: Operation | None = None,
        operation_group: OperationGroup | None = None,
        time_operation: Operation | None = None,
    ):
        """
        Dump monitoring data

        entities:      list of entities/keys to dump data for
        measurables:   list of measurables/keys to dump data for
        range_start:   dump range start in epoch
        range_end:     dump end start in epoch
        intervals:     number of interpolation intervals (0 for raw data)
        clip:          clip the first and last data point to exactly the supplied range
        uncompress:    uncompress run lenght compressed data
        pair_wise:     treat the entities and measurables as pairs not combinations
        """
        entities, measurables = self._get_entities_measurables(entities, measurables)
        request = {
            'entities': entities,
            'measurables': measurables,
            'range_start': start_time * 1000,
            'range_end': end_time * 1000,
            'intervals': intervals,
            'clip': clip,
            'uncompress': uncompress,
            'pair_wise': pair_wise,
        }
        if algorithm is not None:
            request['algorithm'] = algorithm.name
        if operation is not None:
            request['operation'] = operation.name
        if operation_group is not None:
            request['operation_group'] = operation_group.name
        if time_operation is not None:
            request['time_operation'] = time_operation.name
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='plot',
            args=[request],
            timeout=timeout,
        )
        if code:
            raise OSError(out)
        return Result(self.cluster, request, out)

    def get_latest_monitoring_data(
        self,
        entities,
        measurables=None,
        include_measurable_status=False,
        timeout=None,
        counter=False,
    ):
        """
        Get the latest monitoring data.
        """
        entities, measurables = self._get_entities_measurables(entities, measurables)
        request = {
            'entities': entities,
            'measurables': measurables,
            'include_measurable_status': include_measurable_status,
            'data_type': 'COUNTER' if counter else 'CUMULATIVE',
        }
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='plot',
            args=[request],
            timeout=timeout,
        )
        if code:
            raise OSError(out)
        return Result(self.cluster, request, out, latest=True)

    def sample_now(self, entities, measurables=None, env=None, timeout=None):
        """
        Live sample measurables.
        """
        entities, measurables = self._get_entities_measurables(entities, measurables)
        request = {
            'entities': entities,
            'measurables': measurables,
        }
        if env is not None:
            request['env'] = env
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='sample',
            args=[request],
            timeout=timeout,
        )
        if code:
            raise OSError(out)
        return Result(self.cluster, request, out, latest=True)

    def health_overview(self, entities=None, timeout=None):
        """
        Get a overview of all failing or unknown health checks.
        """
        health_overview = HealthOverview(self.cluster)
        measurables = health_overview.get_measurables()
        if len(measurables) == 0:
            raise ValueError('Unable to find any AlertLevel measurable')
        measurables = [it.uuid for it in measurables]
        if entities is None:
            entities = self._get_all_entities()
        else:
            entities = self.cluster._entities_to_uuids(entities)
        request = {
            'entities': entities,
            'measurables': measurables,
        }
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='plot',
            args=[request],
            timeout=timeout,
        )
        if code:
            raise OSError(out)
        health_overview.update(out)
        return health_overview

    def system_information(self, nodes, timeout=None):
        """
        Get detailed information on the monitoring system.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmdevice',
            call='psubSystemInfo',
            args=[self._entities_to_uuids(nodes)],
            timeout=timeout,
        )
        if code:
            raise OSError(out)
        return [
            MonitoringSubSystemInfo(self.cluster, it, parent=self.cluster.get_by_uuid(it['ref_node_uuid']))
            for it in out
        ]

    def reinitialize(self, producers=None, entities=None, timeout=None):
        """
        For reinitialize of monitoring data producers.
        """
        if entities is None:
            entities = []
        if producers is None:
            producers = self.cluster.get_by_type(MonitoringDataProducer)
        producer_uuids = self.cluster._entities_to_uuids(producers)
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='getEntitiesForMonitoringDataProducers',
            args=[producer_uuids],
            timeout=timeout,
        )
        if code:
            raise OSError(out)
        node_uuids = out
        (code, out) = rpc.call(
            service='cmmon',
            call='preinitializeDataProducers',
            args=[
                producer_uuids,
                self.cluster._entities_to_uuids(entities),
                node_uuids,
            ],
            timeout=timeout,
        )
        if code:
            raise OSError(out)
        return list(zip(node_uuids, out))

    def trigger_information(self, timeout=None):
        """
        Get low level information on monitoring triggers.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='getTriggerEvaluationData',
            timeout=timeout,
        )
        if code:
            raise OSError(out)
        return out

    def request_pickup(self, nodes: list[UUID | Node], interval: int = 1, times: int = 1, priority: int = 100) -> int:
        """
        Request monitoring data to picked up on an alternative schedule
        """
        intervals = []
        for node in nodes:
            item = MonitoringPickupInterval()
            if isinstance(node, UUID):
                item.ref_node_uuid = node
            else:
                item.ref_node_uuid = node.uuid
            item.interval = interval
            item.times = times
            item.priority = priority
            intervals.append(item)
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(service='cmmon', call='requestPickupIntervals', args=[intervals])
        if code:
            raise OSError(out)
        return out

    def drop(self, nodes: list[UUID | Node], measurables: list[UUID | MonitoringMeasurable], trim: bool = True) -> int:
        """
        Drop monitoring data, return number of data pages dropped
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='removeEntityMeasurable',
            args=[self.cluster._entities_to_uuids(nodes), self.cluster._entities_to_uuids(measurables), trim],
        )
        if code:
            raise OSError(out)
        return out

    def push(self, data: list[dict], asynchronous: bool = False, time_series: bool = False) -> int:
        """
        Push monitoring data in the JSON data producer format
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(service='cmmon', call='pushMonitoringData', args=[data, asynchronous, time_series])
        if code:
            raise OSError(out)
        return out

    def push_prometheus(self, data: str) -> int:
        """
        Push prometheus data
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(service='cmmon', call='pushPrometheusData', args=[data])
        if code:
            raise OSError(out)
        return out

    def suspend(self, nodes: list[UUID | Node], services: list[str] | None) -> int:
        """
        Suspend one or more monitoring service
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service='cmmon',
            call='pmonitoringSuspend',
            args=[self.cluster._entities_to_uuids(nodes), services if bool(services) else []],
        )
        if code:
            raise OSError(out)
        return out

    def resume(self, nodes: list[UUID | Node], services: list[str] | None) -> int:
        """
        Resume one or more monitoring service
        """
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service='cmmon',
            call='pmonitoringResume',
            args=[self.cluster._entities_to_uuids(nodes), services if bool(services) else []],
        )
        if code:
            raise OSError(out)
        return out
