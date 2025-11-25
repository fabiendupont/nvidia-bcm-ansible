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
module: lsf_job_queue
description: ['LSF job queues']
options:
    state:
      type: str
      choices:
      - present
      - absent
      default: present
      description:
      - The state the resource should have
    cloneFrom:
      type: str
      default: ''
      description:
      - The id or name of the entity that the new entity will be cloned from.
      - ' (take effect only at entity creation)'
    name:
      description:
      - Name of queue
      type: str
      required: true
    wlmCluster:
      description:
      - WlmCluster to which this node belongs
      type: str
      required: false
    overlays:
      description:
      - Configuration overlays which nodes will be added to the queue (Slurm partition)
      type: list
      required: false
      default: []
    categories:
      description:
      - List of node categories which nodes will be added to the queue (Slurm partition)
      type: list
      required: false
      default: []
    nodegroups:
      description:
      - List of managed nodegroups
      type: list
      required: false
      default: []
    computeNodes:
      description:
      - List of compute nodes that will be added to the queue
      type: list
      required: false
      default: []
    options:
      description:
      - Additional parameters that will be passed to the WLM queue configuration
      type: list
      required: false
      default: []
    administrators:
      description:
      - List of queue administrators.
      type: str
      required: false
    corelimit:
      description:
      - The per-process core file size limit (in KB) for all of the processes belonging
        to a job from this queue.
      type: int
      required: false
      default: 0
    cpulimit:
      description:
      - 'Maximum normalized CPU time and optionally, the default normalized CPU time allowed
        for all processes of a job running in this queue; value format: [default_limit]
        maximum_limit.'
      type: str
      required: false
    chkPnt:
      description:
      - 'Enables automatic checkpointing; value format: dir [period], where dir is the
        directory where the checkpoint files are created (do not use environment variables);
        period is the checkpoint period in minutes.'
      type: str
      required: false
    datalimit:
      description:
      - The per-process data segment size limit (in KB) for all of the processes belonging
        to a job from this queue.
      type: int
      required: false
      default: 0
    description:
      description:
      - Description of the queue that will be displayed by 'bqueues -l'
      type: str
      required: false
    default_host_spec:
      description:
      - The default CPU time normalization host for the queue.
      type: str
      required: false
    dispatch_window:
      description:
      - The time windows in which jobs from this queue are dispatched.
      type: str
      required: false
    exclusive:
      description:
      - If Y, specifies an exclusive queue. Jobs submitted to an exclusive queue with
        'bsub -x' will only be despatched to a host that has no other LSF jobs running.
      type: str
      required: false
    filelimit:
      description:
      - The per-process file size limit (in KB) for all of the processes belonging to
        a job from this queue.
      type: int
      required: false
      default: 0
    hjob_limit:
      description:
      - Maximum number of job slots that this queue can use on any host.
      type: int
      required: false
      default: 0
    hosts:
      description:
      - A space-separated list of hosts, host groups, and host partitions on which jobs
        from this queue can be run.
      type: str
      required: false
    ignore_deadline:
      description:
      - If Y, disables deadline constraint scheduling (starts all jobs regardless of deadline
        constraints).
      type: str
      required: false
    interactive:
      description:
      - Causes the queue to reject interactive batch jobs (NO) or accept nothing but interactive
        batch jobs (ONLY). Interactive batch jobs are submitted via 'bsub -I'.
      type: str
      required: false
    job_accept_interval:
      description:
      - The number of dispatch turns to wait after dispatching a job to a host, before
        dispatching a second job to the same host.
      type: int
      required: false
      default: 0
    job_controls:
      description:
      - Changes the behaviour of the SUSPEND, RESUME, and TERMINATE actions.
      type: str
      required: false
    pre_post_exec_user:
      description:
      - Username for prolog and epilog execution.
      type: str
      required: false
      default: root
    prolog:
      description:
      - Path to prolog script (pre_exec).
      type: str
      required: false
    epilog:
      description:
      - Path to epilog script (post_exec).
      type: str
      required: false
    hostProlog:
      description:
      - Path to per host prolog script (host_pre_exec).
      type: str
      required: false
      default: /cm/local/apps/cmd/scripts/prolog
    hostEpilog:
      description:
      - Path to per host epilog script (host_post_exec).
      type: str
      required: false
      default: /cm/local/apps/cmd/scripts/epilog
    job_starter:
      description:
      - Creates a specific environment for submitted jobs prior to execution.
      type: str
      required: false
    load_index:
      description:
      - Scheduling and suspending thresholds for the specifed dynamic load index.
      type: str
      required: false
    memlimit:
      description:
      - The per-process memory resident set size limit (in KB) for all of the processes
        belonging to a job from this queue. Format is '[default_limit] maximum_limit'.
      type: str
      required: false
    mig:
      description:
      - Enables automatic job migration and specifies the migration threshold, in minutes.
      type: int
      required: false
      default: 0
    new_job_sched_delay:
      description:
      - The maximum or minimum length of time that a new job waits before being dispatched;
        the behavior depends on whether the delay period specified is longer or shorter
        than a regular dispatch interval (MBD_SLEEP_TIME in lsb.params, 60 seconds by
        default).
      type: int
      required: false
      default: 0
    nice:
      description:
      - Adjusts the Unix scheduling priority at which jobs from this queue execute.
      type: int
      required: false
      default: 0
    pjob_limit:
      description:
      - The per-processor job slot limit for the queue.
      type: int
      required: false
      default: 0
    processlimit:
      description:
      - Limits the number of concurrent processes that can be part of a job.
      type: str
      required: false
    proclimit:
      description:
      - Limits the number of processors that can be allocated to the job.
      type: str
      required: false
    priority:
      description:
      - Queue priority.
      type: int
      required: false
      default: 0
    qjob_limit:
      description:
      - Job slot limit for the queue. Total number of job slots this queue can use.
      type: int
      required: false
      default: 0
    rerunnable:
      description:
      - If yes, enables automatic job rerun (restart).
      type: str
      required: false
    require_exit_values:
      description:
      - The exit codes that will cause the job to be requeued.
      type: str
      required: false
    res_req:
      description:
      - Resource requirements used to determine eligible hosts.
      type: str
      required: false
    resume_cond:
      description:
      - Use the select section of the resource requirement string to specify load thresholds.
        All other sections are ignored.
      type: str
      required: false
    run_window:
      description:
      - Time period during which jobs in the queue are allowed to run.
      type: str
      required: false
    runlimit:
      description:
      - 'The maximum run limit and optionally the default run limit. Value format: [default_limit]
        maximum_limit.'
      type: str
      required: false
    slot_reserve:
      description:
      - Enables processor reservation and specifies the number of dispatch turns over
        which a parallel job can reserve job slots.
      type: int
      required: false
      default: 0
    stacklimit:
      description:
      - The per-process stack segment size limit (in KB) for all of the processes belonging
        to a job from this queue.
      type: int
      required: false
      default: 0
    stop_cond:
      description:
      - Use the select section of the resource requirement string to specify load thresholds.
        All other sections are ignored.
      type: str
      required: false
    swaplimit:
      description:
      - The amount of total virtual memory limit (in KB) for a job from this queue.
      type: int
      required: false
      default: 0
    terminate_when:
      description:
      - Configures the queue to invoke the TERMINATE action instead of the SUSPEND action
        in the specified circumstance.
      type: str
      required: false
    ujob_limit:
      description:
      - The per-user job slot limit for the queue. Maximum number of slots that each user
        can use in this queue.
      type: int
      required: false
      default: 0
    users:
      description:
      - A list of users or user groups that can submit jobs to this queue. Use the reserved
        word all to specify all users.
      type: str
      required: false
    r15s:
      description:
      - 'Built-in load index: run queue length (15 sec average).'
      type: str
      required: false
    r1m:
      description:
      - 'Built-in load index: run queue length (1 min average).'
      type: str
      required: false
    r15m:
      description:
      - 'Built-in load index: run queue length (15 min average).'
      type: str
      required: false
    it:
      description:
      - 'Built-in load index: idle time.'
      type: str
      required: false
    io:
      description:
      - 'Built-in load index: disk I/O.'
      type: str
      required: false
    ut:
      description:
      - 'Built-in load index: CPU utilization.'
      type: str
      required: false
    mem:
      description:
      - 'Built-in load index: available memory (in MB).'
      type: str
      required: false
    pg:
      description:
      - 'Built-in load index: pages in + pages out.'
      type: str
      required: false
    tmp:
      description:
      - 'Built-in load index: available space in temporary file system (MB).'
      type: str
      required: false
    swp:
      description:
      - 'Built-in load index: available swap space (in MB).'
      type: str
      required: false
    ls:
      description:
      - Built-in load index.
      type: str
      required: false
    fairshare:
      description:
      - Fairshare scheduling
      type: str
      required: false
    backfill:
      description:
      - Backfill scheduling
      type: str
      required: false
    preemption:
      description:
      - Preemption scheduling
      type: str
      required: false
    defaultQueue:
      description:
      - Specifies the queue which is to accept jobs when no queue is requested
      type: bool
      required: false
      default: false

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
lsf_job_queue:
  type: complex
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

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import LSFJobQueue
except ImportError:
    HAS_PYTHONCM = False
    PYTHONCM_IMP_ERR = traceback.format_exc()
else:
    HAS_PYTHONCM = True
    PYTHONCM_IMP_ERR = None

try:
    import deepdiff
except ImportError:
    HAS_DEEPDIFF = False
    DEEPDIFF_IMP_ERR = traceback.format_exc()
else:
    HAS_DEEPDIFF = True
    DEEPDIFF_IMP_ERR = None

try:
    from box import Box
except ImportError:
    HAS_BOX = False
    BOX_IMP_ERR = traceback.format_exc()
else:
    HAS_BOX = True
    BOX_IMP_ERR = None

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.base_module import BaseModule
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.core import EntityManager
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.utils import json_encode_entity
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.lsf_job_queue import LSFJobQueue_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=LSFJobQueue_ArgSpec.argument_spec,
        supports_check_mode=True,
    )

    if not HAS_PYTHONCM:
        module.fail_json(msg=missing_required_lib("cmdaemon-pythoncm"), exception=PYTHONCM_IMP_ERR)

    if not HAS_DEEPDIFF:
        module.fail_json(msg=missing_required_lib("deepdiff"), exception=DEEPDIFF_IMP_ERR)

    if not HAS_BOX:
        module.fail_json(msg=missing_required_lib("python-box"), exception=BOX_IMP_ERR)

    params =  module.bright_params

    cluster = Cluster()  # TODO make this configurable

    entity_manager = EntityManager(cluster, module.log)

    entity = entity_manager.lookup_entity(params, LSFJobQueue)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(LSFJobQueue, params, commit=not module.check_mode)
            changed = True
    else:

        if desired_state == "present":
            diff = entity_manager.check_diff(entity, params)
            if diff:
                entity, res = entity_manager.update_resource(entity, params, commit=not module.check_mode)
                changed = True

        if desired_state == "absent":
            entity, res = entity_manager.delete_resource(entity, params, commit=not module.check_mode)
            changed = True

    entity_as_dict = json_encode_entity(entity)

    cluster.disconnect()

    if not changed:
        module.exit_json(changed=changed, **entity_as_dict)

    if res.good:
        module.exit_json(changed=changed, diff=diff, **entity_as_dict)
    else:
        if hasattr(res, 'validation'):
            msg = "|".join(it.message for it in res.validation)
        else:
            msg = "Operation failed."
        module.fail_json(msg=msg, **entity_as_dict)


if __name__ == '__main__':
    main()