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
module: pbs_pro_wlm_cluster
description: ['Manages pbs_pro_wlm_clusters']
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
      - Name
      type: str
      required: true
    moduleFileTemplate:
      description:
      - Template content for system module file
      type: str
      required: false
    primaryServer:
      description:
      - The WLM primary server (where the active WLM daemon will be running).
      type: str
      required: false
    network:
      description:
      - Network that will be used to form FQDN node names
      type: str
      required: false
    tracingJobs:
      description:
      - A list of job ids to trace in CMDaemon
      type: list
      required: false
      default: []
    enablePreJob:
      description:
      - Enable Cluster Manager powered pre job healthchecking in the workload manager
      type: bool
      required: false
      default: false
    enablePostJob:
      description:
      - Enable Cluster Manager powered post job healthchecking in the workload manager
      type: bool
      required: false
      default: false
    accounting:
      description:
      - Advanced accounting settings
      type: dict
      required: false
      options:
        managedHierarchy:
          description:
          - Representation of account name as a list of organizational entities
          type: list
          required: false
          default: []
        separator:
          description:
          - Separator of organizational entities in the account names
          type: str
          required: false
          default: _
        jobCommentLabels:
          description:
          - User can tag a job with a label (a key in JSON object format) that is parsed
            and monitored by BCM
          type: list
          required: false
          default: []
        extractAccountingInfo:
          description:
          - Extract accounting information, set to false to keep inside account/comments
            fields
          type: bool
          required: false
          default: true
    version:
      description:
      - Major PBS Pro version
      type: str
      required: false
      choices:
      - '20'
      - '21'
      - '22'
      - '22.05'
      - '23.06'
      - '24'
      - '25'
    placeholders:
      description:
      - Job queue node placeholders mode
      type: list
      required: false
      default: []
      elements: dict
      options:
        queue:
          description:
          - Name of queue
          type: str
          required: false
        baseNodeName:
          description:
          - Placeholder node base name
          type: str
          required: false
          default: placeholder
        maxNodes:
          description:
          - Maximum number of nodes in queue
          type: int
          required: false
          default: 0
        templateNode:
          description:
          - Node that will be used as a placeholder
          type: str
          required: false
    cgroups:
      description:
      - Submode containing PBS Pro related cgroups settings
      type: dict
      required: false
      options:
        mountPoint:
          description:
          - Where cgroups is mounted
          type: str
          required: false
          default: /sys/fs/cgroup
        jobCgroupTemplate:
          description:
          - Template for job cgroup/v1 path ($ESCAPE_JOBID will be replaced by systemd-escape
            of job id)
          type: str
          required: false
          default: pbspro.slice/pbspro-$ESCAPE_JOBID.slice
        jobCgroupV2Template:
          description:
          - Template for job cgroup/v2 path ($PBS_CGROUPV2_JOBID will be replaced by the
            proper value in cgroup fs)
          type: str
          required: false
          default: $CGROUP_PREFIX.service/jobs/$PBS_CGROUPV2_JOBID
        cgroupPrefix:
          description:
          - Cgroup prefix that used by PBS when the cgroup is created
          type: str
          required: false
          default: pbspro
        enabled:
          description:
          - 'When set the cgroups hook is enabled (in the hook config: enabled)'
          type: bool
          required: false
          default: true
        killTimeout:
          description:
          - 'Maximum number of seconds the hook spends attempting to kill job processes
            before destroying cgroups (in the hook config: kill_timeout)'
          type: int
          required: false
          default: 10
        serverTimeout:
          description:
          - 'Maximum number of seconds the hook spends attempting to fetch node info from
            the server (in the hook config: server_timeout)'
          type: int
          required: false
          default: 15
        useHyperthreads:
          description:
          - 'All CPU threads are made available to jobs (in the hook config: use_hyperthreads)'
          type: bool
          required: false
          default: false
        ncpusAreCores:
          description:
          - 'ncpus of a vnode is the number of cores, and the hook assigns all threads
            of each core to a job (in the hook config: ncpus_are_cores)'
          type: bool
          required: false
          default: false
        cpuacctEnabled:
          description:
          - Enable cpuacct cgroup controller for jobs
          type: bool
          required: false
          default: true
        cpusetEnabled:
          description:
          - Enable cpuset cgroup controller for jobs
          type: bool
          required: false
          default: true
        devicesEnabled:
          description:
          - Enable devices cgroup controller for jobs
          type: bool
          required: false
          default: true
        devicesAllow:
          description:
          - Parameter specifies how access to devices will be controlled
          type: list
          required: false
          default:
          - b *:* rwm
          - c *:* rwm
        hugetlbEnabled:
          description:
          - Enable hugetlb cgroup controller for jobs
          type: bool
          required: false
          default: false
        hugetlbDefault:
          description:
          - The amount of huge page memory assigned to the cgroup when the job does not
            request hpmem
          type: int
          required: false
          default: 0
        hugetlbReservePercent:
          description:
          - The percentage of available huge page memory (hpmem) that is not to be assigned
            to jobs
          type: int
          required: false
          default: 0
        hugetlbReserveAmount:
          description:
          - An amount of available huge page memory (hpmem) that is not to be assigned
            to jobs
          type: int
          required: false
          default: 0
        memoryEnabled:
          description:
          - Enable memory cgroup controller for jobs
          type: bool
          required: false
          default: true
        memorySoftLimit:
          description:
          - If false PBS uses hard memory limits which prevent the processes from ever
            exceeding their requested memory usage
          type: bool
          required: false
          default: true
        memoryDefault:
          description:
          - Amount of memory assigned to the job if it doesn't request any memory
          type: int
          required: false
          default: 268435456
        memoryReservePercent:
          description:
          - The percentage of available physical memory that is not to be assigned to
            jobs
          type: int
          required: false
          default: 0
        memoryReserveAmount:
          description:
          - A specific amount of available physical memory that is not to be assigned
            to jobs
          type: int
          required: false
          default: 67108864
        memswEnabled:
          description:
          - Enable memsw cgroup controller for jobs
          type: bool
          required: false
          default: false
        memswDefault:
          description:
          - Specifies the amount of memory + swap assigned to the job if it doesn't request
            any memory
          type: int
          required: false
          default: 268435456
        memswReservePercent:
          description:
          - Percentage of available swap that is not to be assigned to jobs
          type: int
          required: false
          default: 0
        memswReserveAmount:
          description:
          - An amount of available swap that is not to be assigned to jobs
          type: int
          required: false
          default: 67108864
    pelogs:
      description:
      - Submode containing a list of PBS Pro related prolog and epilog (pelog) hook settings
      type: list
      required: false
      default: []
      elements: dict
      options:
        enabled:
          description:
          - Enable hook
          type: bool
          required: false
          default: true
        name:
          description:
          - Hook name in PBS
          type: str
          required: false
        events:
          description:
          - List of hook events
          type: list
          required: false
          default: []
        path:
          description:
          - Fully qualified pathname of a hook script
          type: str
          required: false
        defaultAction:
          description:
          - PBS prolog/epilog default action
          type: str
          required: false
          default: RERUN
          choices:
          - RERUN
          - DELETE
        enableParallel:
          description:
          - Enable parallel prologues/epilogues that run on sister moms
          type: bool
          required: false
          default: true
        verboseUserOutput:
          description:
          - Provide verbose hook output to the user's .o/.e file
          type: bool
          required: false
          default: false
        torqueCompatible:
          description:
          - Make torque compatible
          type: bool
          required: false
          default: false
        order:
          description:
          - Hook order
          type: int
          required: false
          default: 0
        alarm:
          description:
          - Hook alarm time (timeout)
          type: int
          required: false
          default: 300
        debug:
          description:
          - Enable hook debug (in PBS)
          type: bool
          required: false
          default: false
    enableJobHistory:
      description:
      - Keep all job attribute information in PBS Pro
      type: bool
      required: false
      default: true
    jobHistoryDuration:
      description:
      - Specifies the length of time that PBS will keep each job's history
      type: str
      required: false
      default: 00:30:00
    prefix:
      description:
      - PBS Pro installation directory
      type: str
      required: false
    spool:
      description:
      - PBS Pro server spool directory
      type: str
      required: false
    subType:
      description:
      - PBS Pro subtype
      type: str
      required: false
      default: PBSPRO
      choices:
      - PBSPRO
      - OPENPBS
    flatUid:
      description:
      - Specifies whether a username at the submission host must be the same as the one
        at the server host
      type: bool
      required: false
      default: true
    maxRunning:
      description:
      - Maximum number of jobs allowed to run at any given time (0 is the same as infinite)
      type: int
      required: false
      default: 0

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
pbs_pro_wlm_cluster:
  type: complex
  description: ''
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
      description: Name
      returned: success
    moduleFileTemplate:
      type: str
      description: Template content for system module file
      returned: success
    primaryServer:
      type: complex
      description: The WLM primary server (where the active WLM daemon will be running).
      returned: success
    network:
      type: complex
      description: Network that will be used to form FQDN node names
      returned: success
    tracingJobs:
      type: str
      description: A list of job ids to trace in CMDaemon
      returned: success
    enablePreJob:
      type: bool
      description: Enable Cluster Manager powered pre job healthchecking in the workload
        manager
      returned: success
    enablePostJob:
      type: bool
      description: Enable Cluster Manager powered post job healthchecking in the workload
        manager
      returned: success
    accounting:
      type: complex
      description: Advanced accounting settings
      returned: success
    version:
      type: str
      description: Major PBS Pro version
      returned: success
    placeholders:
      type: list
      description: Job queue node placeholders mode
      returned: success
    cgroups:
      type: complex
      description: Submode containing PBS Pro related cgroups settings
      returned: success
    pelogs:
      type: list
      description: Submode containing a list of PBS Pro related prolog and epilog
        (pelog) hook settings
      returned: success
    enableJobHistory:
      type: bool
      description: Keep all job attribute information in PBS Pro
      returned: success
    jobHistoryDuration:
      type: str
      description: Specifies the length of time that PBS will keep each job's history
      returned: success
    prefix:
      type: str
      description: PBS Pro installation directory
      returned: success
    spool:
      type: str
      description: PBS Pro server spool directory
      returned: success
    subType:
      type: str
      description: PBS Pro subtype
      returned: success
    flatUid:
      type: bool
      description: Specifies whether a username at the submission host must be the
        same as the one at the server host
      returned: success
    maxRunning:
      type: int
      description: Maximum number of jobs allowed to run at any given time (0 is the
        same as infinite)
      returned: success

"""
############################
# Imports
############################

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import PbsProWlmCluster
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.pbs_pro_wlm_cluster import PbsProWlmCluster_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=PbsProWlmCluster_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, PbsProWlmCluster)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(PbsProWlmCluster, params, commit=not module.check_mode)
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