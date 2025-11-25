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

import time
import typing
from uuid import UUID

from pythoncm.entity.entity import Entity
from pythoncm.monitoring.plot.result import Result
from pythoncm.util import uuid_compare

if typing.TYPE_CHECKING:
    from pythoncm.entity.node import Node


class JobInfo(Entity):
    def get_all_measurables(
        self, metrics: bool = True, healthchecks: bool = True, enum_metrics: bool = True
    ) -> list[UUID]:
        """
        Get all measurables for the job.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='getMonitoringMeasurablesForEntity',
            args=self.ref_node_monitoring_uuids,
        )
        if code:
            raise OSError(out)
        return self._filter_measurables(out, metrics, healthchecks, enum_metrics)

    def get_node_uuid_from_node_monitoring_uuid(self, monitoring_uuid: UUID | str) -> UUID:
        if isinstance(monitoring_uuid, str):
            monitoring_uuid = UUID(monitoring_uuid)
        return next(
            (
                node
                for node, ref_node_monitoring_uuid in zip(self.nodes, self.ref_node_monitoring_uuids)
                if uuid_compare(ref_node_monitoring_uuid, monitoring_uuid)
            ),
            monitoring_uuid,
        )

    def latest_monitoring_data(self, measurables: list[UUID | Entity] | None = None) -> Result:
        """
        Latest monitoring data.
        """
        if measurables is None:
            measurables = self.get_all_measurables()
        else:
            measurables = [it for it in measurables if isinstance(it, UUID)] + [
                it.uuid for it in measurables if isinstance(it, Entity)
            ]
        request = {
            'entities': self.ref_node_monitoring_uuids,
            'measurables': measurables,
            'range_start': 0,
            'range_end': 0,
        }
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='plot',
            request=request,
        )
        if code:
            raise OSError(out)
        return Result(self._cluster, request, out, latest=True, job_info=self)

    def dump_monitoring_data(
        self,
        start_time: int | None = None,
        end_time: int | None = None,
        measurables: list[UUID | Entity] | None = None,
        intervals: int = 0,
        clip: bool = True,
    ) -> Result:
        """
        Dump monitoring data.
        """
        if start_time is None:
            start_time = self.startTime
        if end_time is None:
            if self.endTime == 0:
                end_time = int(time.time())
            else:
                end_time = self.endTime
        if measurables is None:
            measurables = self.get_all_measurables()
        else:
            measurables = [it for it in measurables if isinstance(it, UUID)] + [
                it.uuid for it in measurables if isinstance(it, Entity)
            ]
        request = {
            'entities': self.ref_node_monitoring_uuids,
            'measurables': measurables,
            'range_start': start_time * 1000,
            'range_end': end_time * 1000,
            'intervals': intervals,
            'clip': clip,
        }
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmmon',
            call='plot',
            request=request,
        )
        if code:
            raise OSError(out)
        return Result(self._cluster, request, out, job_info=self)

    def _get_data(
        self,
        call,
        start: int = 0,
        end: int = 4294967296,
    ) -> tuple[str, str]:
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(service='cmjob', call=call, args=[self.ref_wlm_cluster_uuid, self.jobId, start, end])
        if code:
            raise OSError(out)
        return out.get('path', ''), out.get('content', '')

    def stdin(
        self,
        start: int = 0,
        end: int = 4294967296,
    ) -> tuple[str, str]:
        """
        Get stdin path and content provided to job
        """
        return self._get_data('getJobStdin', start, end)

    def stdout(
        self,
        start: int = 0,
        end: int = 4294967296,
    ) -> tuple[str, str]:
        """
        Get stdout path and content of the job
        """
        return self._get_data('getJobStdout', start, end)

    def stderr(
        self,
        start: int = 0,
        end: int = 4294967296,
    ) -> tuple[str, str]:
        """
        Get stderr path and content of the job
        """
        return self._get_data('getJobStderr', start, end)

    def remove(self) -> str:
        """
        Remove/cancel the job
        """
        return self._cluster.workload.remove_job(self.ref_wlm_cluster_uuid, self.jobId)

    def requeue(self) -> str:
        """
        Requeue the job
        """
        return self._cluster.workload.requeue_job(self.ref_wlm_cluster_uuid, self.jobId)

    def hold(self) -> str:
        """
        Hold the job
        """
        return self._cluster.workload.hold_job(self.ref_wlm_cluster_uuid, self.jobId)

    def suspend(self) -> str:
        """
        Suspend the job
        """
        return self._cluster.workload.suspend_job(self.ref_wlm_cluster_uuid, self.jobId)

    def resume(self) -> str:
        """
        Resume the job
        """
        return self._cluster.workload.resume_job(self.ref_wlm_cluster_uuid, self.jobId)

    def release(self) -> str:
        """
        Release the job
        """
        return self._cluster.workload.release_job(self.ref_wlm_cluster_uuid, self.jobId)

    def pids_and_gpus(self) -> list[tuple[Node, str, list[int], list[int]]]:
        rpc = self._cluster.get_rpc()
        code, out = rpc.call(
            service="cmjob",
            call="pgetJobPidsGPUs",
            args=[self.ref_wlm_cluster_uuid, self.jobId, self._cluster._entities_to_uuids(self.nodes)],
        )
        if code:
            raise OSError(out)
        return list(zip(self.nodes, out.get("info", []), out.get("pids", []), out.get("gpus", [])))
