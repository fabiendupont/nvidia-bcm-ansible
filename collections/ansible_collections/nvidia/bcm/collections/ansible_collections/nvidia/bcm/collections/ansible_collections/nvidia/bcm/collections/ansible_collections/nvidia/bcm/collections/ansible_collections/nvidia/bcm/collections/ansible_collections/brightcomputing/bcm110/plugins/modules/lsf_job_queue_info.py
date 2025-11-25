#!/cm/local/apps/python3/bin/python
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


############################
# Docs
############################
DOCUMENTATION = r"""
---
module: lsf_job_queue_info
description: Query cmdaemon for entity of type LSFJobQueue
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
lsf_job_queue:
  type: list
  description: LSF job queues
  returned: success
  contains:
    uuid:
      type: str
      description: ''
      returned: success
    baseType:
      type: str
      description: ''
      returned: success
    childType:
      type: str
      description: ''
      returned: success
    revision:
      type: str
      description: ''
      returned: success
    modified:
      type: bool
      description: ''
      returned: success
    is_committed:
      type: bool
      description: ''
      returned: success
    to_be_removed:
      type: bool
      description: ''
      returned: success
    extra_values:
      type: json
      description: ''
      returned: success
    name:
      type: str
      description: Name of queue
      returned: success
    wlmCluster:
      type: complex
      description: WlmCluster to which this node belongs
      returned: success
    overlays:
      type: list
      description: Configuration overlays which nodes will be added to the queue (Slurm
        partition)
      returned: success
    categories:
      type: list
      description: List of node categories which nodes will be added to the queue
        (Slurm partition)
      returned: success
    nodegroups:
      type: list
      description: List of managed nodegroups
      returned: success
    computeNodes:
      type: list
      description: List of compute nodes that will be added to the queue
      returned: success
    options:
      type: str
      description: Additional parameters that will be passed to the WLM queue configuration
      returned: success
    administrators:
      type: str
      description: List of queue administrators.
      returned: success
    corelimit:
      type: int
      description: The per-process core file size limit (in KB) for all of the processes
        belonging to a job from this queue.
      returned: success
    cpulimit:
      type: str
      description: 'Maximum normalized CPU time and optionally, the default normalized
        CPU time allowed for all processes of a job running in this queue; value format:
        [default_limit] maximum_limit.'
      returned: success
    chkPnt:
      type: str
      description: 'Enables automatic checkpointing; value format: dir [period], where
        dir is the directory where the checkpoint files are created (do not use environment
        variables); period is the checkpoint period in minutes.'
      returned: success
    datalimit:
      type: int
      description: The per-process data segment size limit (in KB) for all of the
        processes belonging to a job from this queue.
      returned: success
    description:
      type: str
      description: Description of the queue that will be displayed by 'bqueues -l'
      returned: success
    default_host_spec:
      type: str
      description: The default CPU time normalization host for the queue.
      returned: success
    dispatch_window:
      type: str
      description: The time windows in which jobs from this queue are dispatched.
      returned: success
    exclusive:
      type: str
      description: If Y, specifies an exclusive queue. Jobs submitted to an exclusive
        queue with 'bsub -x' will only be despatched to a host that has no other LSF
        jobs running.
      returned: success
    filelimit:
      type: int
      description: The per-process file size limit (in KB) for all of the processes
        belonging to a job from this queue.
      returned: success
    hjob_limit:
      type: int
      description: Maximum number of job slots that this queue can use on any host.
      returned: success
    hosts:
      type: str
      description: A space-separated list of hosts, host groups, and host partitions
        on which jobs from this queue can be run.
      returned: success
    ignore_deadline:
      type: str
      description: If Y, disables deadline constraint scheduling (starts all jobs
        regardless of deadline constraints).
      returned: success
    interactive:
      type: str
      description: Causes the queue to reject interactive batch jobs (NO) or accept
        nothing but interactive batch jobs (ONLY). Interactive batch jobs are submitted
        via 'bsub -I'.
      returned: success
    job_accept_interval:
      type: int
      description: The number of dispatch turns to wait after dispatching a job to
        a host, before dispatching a second job to the same host.
      returned: success
    job_controls:
      type: str
      description: Changes the behaviour of the SUSPEND, RESUME, and TERMINATE actions.
      returned: success
    pre_post_exec_user:
      type: str
      description: Username for prolog and epilog execution.
      returned: success
    prolog:
      type: str
      description: Path to prolog script (pre_exec).
      returned: success
    epilog:
      type: str
      description: Path to epilog script (post_exec).
      returned: success
    hostProlog:
      type: str
      description: Path to per host prolog script (host_pre_exec).
      returned: success
    hostEpilog:
      type: str
      description: Path to per host epilog script (host_post_exec).
      returned: success
    job_starter:
      type: str
      description: Creates a specific environment for submitted jobs prior to execution.
      returned: success
    load_index:
      type: str
      description: Scheduling and suspending thresholds for the specifed dynamic load
        index.
      returned: success
    memlimit:
      type: str
      description: The per-process memory resident set size limit (in KB) for all
        of the processes belonging to a job from this queue. Format is '[default_limit]
        maximum_limit'.
      returned: success
    mig:
      type: int
      description: Enables automatic job migration and specifies the migration threshold,
        in minutes.
      returned: success
    new_job_sched_delay:
      type: int
      description: The maximum or minimum length of time that a new job waits before
        being dispatched; the behavior depends on whether the delay period specified
        is longer or shorter than a regular dispatch interval (MBD_SLEEP_TIME in lsb.params,
        60 seconds by default).
      returned: success
    nice:
      type: int
      description: Adjusts the Unix scheduling priority at which jobs from this queue
        execute.
      returned: success
    pjob_limit:
      type: int
      description: The per-processor job slot limit for the queue.
      returned: success
    processlimit:
      type: str
      description: Limits the number of concurrent processes that can be part of a
        job.
      returned: success
    proclimit:
      type: str
      description: Limits the number of processors that can be allocated to the job.
      returned: success
    priority:
      type: int
      description: Queue priority.
      returned: success
    qjob_limit:
      type: int
      description: Job slot limit for the queue. Total number of job slots this queue
        can use.
      returned: success
    rerunnable:
      type: str
      description: If yes, enables automatic job rerun (restart).
      returned: success
    require_exit_values:
      type: str
      description: The exit codes that will cause the job to be requeued.
      returned: success
    res_req:
      type: str
      description: Resource requirements used to determine eligible hosts.
      returned: success
    resume_cond:
      type: str
      description: Use the select section of the resource requirement string to specify
        load thresholds. All other sections are ignored.
      returned: success
    run_window:
      type: str
      description: Time period during which jobs in the queue are allowed to run.
      returned: success
    runlimit:
      type: str
      description: 'The maximum run limit and optionally the default run limit. Value
        format: [default_limit] maximum_limit.'
      returned: success
    slot_reserve:
      type: int
      description: Enables processor reservation and specifies the number of dispatch
        turns over which a parallel job can reserve job slots.
      returned: success
    stacklimit:
      type: int
      description: The per-process stack segment size limit (in KB) for all of the
        processes belonging to a job from this queue.
      returned: success
    stop_cond:
      type: str
      description: Use the select section of the resource requirement string to specify
        load thresholds. All other sections are ignored.
      returned: success
    swaplimit:
      type: int
      description: The amount of total virtual memory limit (in KB) for a job from
        this queue.
      returned: success
    terminate_when:
      type: str
      description: Configures the queue to invoke the TERMINATE action instead of
        the SUSPEND action in the specified circumstance.
      returned: success
    ujob_limit:
      type: int
      description: The per-user job slot limit for the queue. Maximum number of slots
        that each user can use in this queue.
      returned: success
    users:
      type: str
      description: A list of users or user groups that can submit jobs to this queue.
        Use the reserved word all to specify all users.
      returned: success
    r15s:
      type: str
      description: 'Built-in load index: run queue length (15 sec average).'
      returned: success
    r1m:
      type: str
      description: 'Built-in load index: run queue length (1 min average).'
      returned: success
    r15m:
      type: str
      description: 'Built-in load index: run queue length (15 min average).'
      returned: success
    it:
      type: str
      description: 'Built-in load index: idle time.'
      returned: success
    io:
      type: str
      description: 'Built-in load index: disk I/O.'
      returned: success
    ut:
      type: str
      description: 'Built-in load index: CPU utilization.'
      returned: success
    mem:
      type: str
      description: 'Built-in load index: available memory (in MB).'
      returned: success
    pg:
      type: str
      description: 'Built-in load index: pages in + pages out.'
      returned: success
    tmp:
      type: str
      description: 'Built-in load index: available space in temporary file system
        (MB).'
      returned: success
    swp:
      type: str
      description: 'Built-in load index: available swap space (in MB).'
      returned: success
    ls:
      type: str
      description: Built-in load index.
      returned: success
    fairshare:
      type: str
      description: Fairshare scheduling
      returned: success
    backfill:
      type: str
      description: Backfill scheduling
      returned: success
    preemption:
      type: str
      description: Preemption scheduling
      returned: success
    defaultQueue:
      type: bool
      description: Specifies the queue which is to accept jobs when no queue is requested
      returned: success

"""
############################
# Imports
############################

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import LSFJobQueue
    from pythoncm.entity_to_json_encoder import EntityToJSONEncoder
except ImportError:
    HAS_PYTHONCM = False
    PYTHONCM_IMP_ERR = traceback.format_exc()
else:
    HAS_PYTHONCM = True
    PYTHONCM_IMP_ERR = None


from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.core import EntityQuery
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.utils import entity_to_dict

############################
# main
############################


def main():

    module = AnsibleModule(
        argument_spec={'format': {'choices': ['list', 'dict'], 'default': 'list', 'type': 'str'}, 'depth': {'default': 3, 'type': 'int'}, 'include_id': {'default': False, 'type': 'bool'}, 'for_update': {'default': False, 'type': 'bool'}},
        supports_check_mode=True,
    )

    if not HAS_PYTHONCM:
        module.fail_json(msg=missing_required_lib("cmdaemon-pythoncm"), exception=PYTHONCM_IMP_ERR)

    cluster = Cluster()  # TODO make this configurable

    entity_query = EntityQuery(cluster)

    results = entity_query.find(LSFJobQueue)

    format = module.params["format"]

    depth = module.params["depth"]

    include_id = module.params["include_id"]

    for_update = module.params["for_update"]

    if format == "list":
        json_ready_result = [
            entity_to_dict(
                entity,
                depth=depth,
                for_update=for_update,
                include_id=include_id,
            )
            for entity in results
        ] if results else []

    if format == "dict":
        json_ready_result = {
            entity.resolve_name: entity_to_dict(
                entity,
                depth=depth,
                for_update=for_update,
                include_id=include_id,
            )
            for entity in results
        } if results else {}

    cluster.disconnect()

    json_ready_result = json.loads(json.dumps(json_ready_result, cls=EntityToJSONEncoder))

    module.exit_json(lsf_job_queues=json_ready_result, changed=False)


if __name__ == '__main__':
    main()