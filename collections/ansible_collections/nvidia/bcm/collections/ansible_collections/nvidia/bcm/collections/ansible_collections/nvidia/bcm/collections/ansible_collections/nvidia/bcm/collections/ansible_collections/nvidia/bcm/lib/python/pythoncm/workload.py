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

from pythoncm.entity import JobInfoStatistics
from pythoncm.entity import WlmFairshareOverview
from pythoncm.entity.jobinfo import JobInfo
from pythoncm.entity_converter import EntityConverter

if typing.TYPE_CHECKING:
    from uuid import UUID

    from pythoncm.entity import Job
    from pythoncm.entity.chargebackrequest import ChargeBackRequest


class Workload:
    """
    Helper class-wrapper for HPC jobs API
    """

    # Filter states
    PENDING = 1
    RUNNING = 2
    FINISHED = 4
    ERROR = 8

    def __init__(self, cluster):
        self.cluster = cluster

    def get_jobs(self, wlm_uuids: list[UUID] | None = None, local_only: bool = False):
        """
        Get all jobs for particular wlm clusters.
        If local_only=True, then the jobs are retrieved from local WLM server only.
        """
        if wlm_uuids is None:
            wlm_uuids = []
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmjob',
            call='getJobs',
            args=[wlm_uuids, local_only],
        )
        if code:
            raise OSError(out)
        converter = EntityConverter(self.cluster, service=None)
        jobs = out.get('jobs', [])
        success = out.get('success', False)
        return success, [converter.convert(it) for it in jobs]

    def get_job_by_wlm_uuid(self, wlm_uuid: UUID, job_id: str):
        """
        Get a specific job using wlm_uuid.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmjob',
            call='getJobByWlmUuid',
            args=[wlm_uuid, job_id],
        )
        if code:
            raise OSError(out)
        if not out:
            return None
        converter = EntityConverter(self.cluster, service=None)
        return converter.convert(out)

    def get_job_by_type_and_hostname(self, wlm_type, hostname, job_id):
        """
        Get a specific job using WLM type string and hostname
        where the job may run (client role is assigned).
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmjob',
            call='getJobByTypeAndHostname',
            args=[wlm_type, hostname, job_id],
        )
        if code:
            raise OSError(out)
        if not out:
            return None
        converter = EntityConverter(self.cluster, service=None)
        return converter.convert(out)

    def __job_action(self, wlm_uuid, job_id, action) -> tuple[str, bool]:
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmjob',
            call=action,
            args=[wlm_uuid, job_id],
        )
        if code:
            raise OSError(out)
        return out

    def remove_job(self, wlm_uuid: UUID, job_id: str) -> tuple[str, bool]:
        """
        Remove/cancel a specific job.
        """
        return self.__job_action(
            job_id=job_id,
            wlm_uuid=wlm_uuid,
            action='removeJob',
        )

    def requeue_job(self, wlm_uuid: UUID, job_id: str) -> tuple[str, bool]:
        """
        Requeue a specific job.
        """
        return self.__job_action(
            job_id=job_id,
            wlm_uuid=wlm_uuid,
            action='requeueJob',
        )

    def hold_job(self, wlm_uuid: UUID, job_id: str) -> tuple[str, bool]:
        """
        Hold a specific job.
        """
        return self.__job_action(
            job_id=job_id,
            wlm_uuid=wlm_uuid,
            action='holdJob',
        )

    def suspend_job(self, wlm_uuid: UUID, job_id: str) -> tuple[str, bool]:
        """
        Suspend a specific job.
        """
        return self.__job_action(
            job_id=job_id,
            wlm_uuid=wlm_uuid,
            action='suspendJob',
        )

    def resume_job(self, wlm_uuid: UUID, job_id: str) -> tuple[str, bool]:
        """
        Resume a specific job.
        """
        return self.__job_action(
            job_id=job_id,
            wlm_uuid=wlm_uuid,
            action='resumeJob',
        )

    def release_job(self, wlm_uuid: UUID, job_id: str) -> tuple[str, bool]:
        """
        Release a specific job.
        """
        return self.__job_action(
            job_id=job_id,
            wlm_uuid=wlm_uuid,
            action='releaseJob',
        )

    def update_job(self, wlm_uuid: UUID, job: Job) -> tuple[str, bool]:
        """
        Update job.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmjob',
            call='updateJob',
            args=[wlm_uuid, job],
        )
        if code:
            raise OSError(out)
        return out

    def constrain_jobs(self, wlm_uuid: UUID, job_ids: list[str], location: str) -> tuple[str, bool]:
        """
        Constrain job.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmjob',
            call='constrainJobs',
            args=[wlm_uuid, job_ids, location],
        )
        if code:
            raise OSError(out)
        return out

    def get_job_info(self, wlm_uuid: UUID, job_id: str):
        """
        Get information about specific job.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmjob',
            call='getJobInfo',
            args=[wlm_uuid, job_id],
        )
        if code:
            raise OSError(out)
        return JobInfo(self.cluster, out)

    def remove_job_info(self, wlm_uuid: UUID, job_ids: list[str]):
        """
        Remove information about specific jobs
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmjob',
            call='removeJobInfo',
            args=[wlm_uuid, job_ids],
        )
        if code:
            raise OSError(out)
        return out

    def filter_job_info(
        self,
        wlm_uuids: list[UUID] | None = None,
        queue_uuids: list[UUID] | None = None,
        job_id: str = '',
        job_name: str = '',
        array_id: str = '',
        user: str = '',
        group: str = '',
        account: str = '',
        accounting_info: dict[str, str] | None = None,
        start_time: int = 0,
        end_time: int = 0xFFFFFFFF,
        states: int = 0xFFFFFFFFFFFFFFFF,
        start: int = 0,
        limit: int = 0xFFFFFFFFFFFFFFFF,
    ):
        """
        Return information on all jobs matching the criteria.
        """
        if wlm_uuids is None:
            wlm_uuids = []
        if queue_uuids is None:
            queue_uuids = []
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmjob',
            call='filterJobInfo',
            args=[
                wlm_uuids,
                queue_uuids,
                job_id,
                job_name,
                array_id,
                user,
                group,
                account,
                accounting_info,
                start_time,
                end_time,
                states,
                start,
                limit,
            ],
        )
        if code:
            raise OSError(out)
        return [JobInfo(self.cluster, it) for it in out]

    def filter_job_statistics(
        self,
        wlm_uuids: list[UUID] | None = None,
        queue_uuids: list[UUID] | None = None,
        job_id: str = '',
        job_name: str = '',
        array_id: str = '',
        user: str = '',
        group: str = '',
        account: str = '',
        accounting_info=None,
        start_time: int = 0,
        end_time: int = 0xFFFFFFFF,
        states: int = 0xFFFFFFFFFFFFFFFF,
        start: int = 0,
        limit: int = 0xFFFFFFFFFFFFFFFF,
        filters: list | None = None,
        interval: int = 0,
        offset: int = 0,
    ):
        """
        Get job statistic on all jobs matching the criteria.
        Grouped by user, group, interval
        """
        if wlm_uuids is None:
            wlm_uuids = []
        if queue_uuids is None:
            queue_uuids = []
        if filters is None:
            filters = []
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmjob',
            call='getJobInfoStatistics',
            args=[
                wlm_uuids,
                queue_uuids,
                job_id,
                job_name,
                array_id,
                user,
                group,
                account,
                accounting_info,
                start_time,
                end_time,
                states,
                start,
                limit,
                filters,
                interval,
                offset,
            ],
        )
        if code:
            raise OSError(out)
        return [JobInfoStatistics(self.cluster, it) for it in out]

    def charge_back(self, request: ChargeBackRequest, timeout: int | None = None) -> dict:
        """
        Get charge back report for this request
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmjob',
            call='chargeBackByEntity',
            args=[request],
            timeout=timeout,
        )
        if code:
            raise OSError(out)
        return out

    def fairshare_overview(self, wlm_uuids: list[UUID] | None = None) -> list[WlmFairshareOverview]:
        """Get WLM accounting fairshare overview."""
        if wlm_uuids is None:
            wlm_uuids = []
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmjob',
            call='getFairshareOverview',
            args=[wlm_uuids],
        )
        if code:
            raise OSError(out)
        return [WlmFairshareOverview(self.cluster, it) for it in out]

    def flush_job_info_to_db(self) -> int:
        """Flush cached job information to database"""
        rpc = self.cluster.get_rpc()
        code, out = rpc.call(
            service='cmjob',
            call='flushJobInfoToDatabase',
        )
        if code:
            raise OSError(out)
        return out
