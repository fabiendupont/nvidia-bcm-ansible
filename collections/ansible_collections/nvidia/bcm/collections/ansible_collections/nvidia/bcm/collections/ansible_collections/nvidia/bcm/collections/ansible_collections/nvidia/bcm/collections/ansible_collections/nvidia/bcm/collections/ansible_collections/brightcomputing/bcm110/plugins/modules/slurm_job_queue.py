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
module: slurm_job_queue
description: ['Slurm job queues']
options:
    state:
      description:
      - State of partition or availability for use.
      type: str
      required: false
      default: NONE
      choices:
      - NONE
      - UP
      - DOWN
      - DRAIN
      - INACTIVE
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
    defaultQueue:
      description:
      - Set this as the default queue
      type: bool
      required: false
      default: false
    minNodes:
      description:
      - Minimal nodes one job has to use
      type: str
      required: false
      default: '1'
    maxNodes:
      description:
      - Maximal nodes one job can use
      type: str
      required: false
      default: UNLIMITED
    defaultTime:
      description:
      - Default job runtime
      type: str
      required: false
      default: UNLIMITED
    maxTime:
      description:
      - Maximal job runtime
      type: str
      required: false
      default: UNLIMITED
    priorityJobFactor:
      description:
      - Partition factor used by priority/multifactor plugin in calculating job priority
      type: int
      required: false
      default: 1
    priorityTier:
      description:
      - Jobs submitted to a partition with a higher priority tier value will be dispatched
        before pending jobs in partition with lower priority tier value
      type: int
      required: false
      default: 1
    hidden:
      description:
      - Hide from all
      type: bool
      required: false
      default: false
    disableRoot:
      description:
      - Do not allow root to run jobs
      type: bool
      required: false
      default: false
    rootOnly:
      description:
      - Only allow root to run jobs
      type: bool
      required: false
      default: false
    allowGroups:
      description:
      - Specify user groups which are allowed to run jobs
      type: str
      required: false
      default: ALL
    overSubscribe:
      description:
      - Controls the ability of the partition to execute more than one job at a time on
        each resource
      type: str
      required: false
      default: 'NO'
    alternate:
      description:
      - Partition name of alternate partition to be used if the state of this partition
        is DRAIN or INACTIVE
      type: str
      required: false
    graceTime:
      description:
      - Specifies, in units of seconds, the preemption grace time to be extended to a
        job which has been selected for preemption
      type: int
      required: false
      default: 0
    defMemPerCPU:
      description:
      - Default real memory size available per allocated CPU in MegaBytes
      type: str
      required: false
      default: UNLIMITED
    maxMemPerCPU:
      description:
      - Maximum real memory size available per allocated CPU in MegaBytes
      type: str
      required: false
      default: UNLIMITED
    defMemPerNode:
      description:
      - Default real memory size available per allocated node in MegaBytes
      type: str
      required: false
      default: UNLIMITED
    maxMemPerNode:
      description:
      - Maximum real memory size available per allocated node in MegaBytes
      type: str
      required: false
      default: UNLIMITED
    preemptMode:
      description:
      - Mechanism used to preempt jobs from this partition
      type: str
      required: false
      default: 'OFF'
    reqResv:
      description:
      - Specifies users of this partition are required to designate a reservation when
        submitting a job
      type: str
      required: false
      default: 'NO'
    SelectTypeParameters:
      description:
      - Partition-specific resource allocation type
      type: str
      required: false
    allowAccounts:
      description:
      - Specify accounts which are allowed to run jobs
      type: str
      required: false
      default: ALL
    allowQos:
      description:
      - Specify qos which are allowed to run jobs
      type: str
      required: false
      default: ALL
    denyAccounts:
      description:
      - Specify accounts which are denied to run jobs
      type: str
      required: false
    denyQos:
      description:
      - Specify qos which are denied to run jobs
      type: str
      required: false
    lln:
      description:
      - Schedule resources to jobs on the least loaded nodes
      type: bool
      required: false
      default: false
    maxCPUsPerNode:
      description:
      - Maximum number of CPUs on any node available to all jobs from this partition
      type: str
      required: false
      default: UNLIMITED
    tresBillingWeights:
      description:
      - Billing weights of each TRES type that will be used in calculating the usage of
        a job
      type: list
      required: false
      default: []
    defMemPerGPU:
      description:
      - Default  real  memory  size  available  per  allocated GPU in megabytes
      type: str
      required: false
      default: UNLIMITED
    defCpuPerGPU:
      description:
      - Default count of CPUs allocated per allocated GPU
      type: str
      required: false
      default: UNLIMITED
    cpuBind:
      description:
      - How tasks are bound to allocated CPUs
      type: str
      required: false
      default: NONE
      choices:
      - NONE
      - BOARD
      - SOCKET
      - LDOM
      - CORE
      - THREAD
    qos:
      description:
      - Used to extend the limits available to a QOS on a partition
      type: str
      required: false
    exclusiveUser:
      description:
      - If set to YES then nodes will be exclusively allocated to users
      type: bool
      required: false
      default: false
    ordering:
      description:
      - Positioning of the jobqueue. Smaller values go first in the configuration file.
      type: int
      required: false
      default: 0
    allocNodes:
      description:
      - Nodes from which users can submit jobs in the partition of managed nodes
      type: list
      required: false
      default: []
    nodesets:
      description:
      - List of nodesets that will be added to Slurm partition
      type: list
      required: false
      default: []

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
slurm_job_queue:
  type: complex
  description: Slurm job queues
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
    defaultQueue:
      type: bool
      description: Set this as the default queue
      returned: success
    minNodes:
      type: str
      description: Minimal nodes one job has to use
      returned: success
    maxNodes:
      type: str
      description: Maximal nodes one job can use
      returned: success
    defaultTime:
      type: str
      description: Default job runtime
      returned: success
    maxTime:
      type: str
      description: Maximal job runtime
      returned: success
    priorityJobFactor:
      type: int
      description: Partition factor used by priority/multifactor plugin in calculating
        job priority
      returned: success
    priorityTier:
      type: int
      description: Jobs submitted to a partition with a higher priority tier value
        will be dispatched before pending jobs in partition with lower priority tier
        value
      returned: success
    hidden:
      type: bool
      description: Hide from all
      returned: success
    disableRoot:
      type: bool
      description: Do not allow root to run jobs
      returned: success
    rootOnly:
      type: bool
      description: Only allow root to run jobs
      returned: success
    allowGroups:
      type: str
      description: Specify user groups which are allowed to run jobs
      returned: success
    overSubscribe:
      type: str
      description: Controls the ability of the partition to execute more than one
        job at a time on each resource
      returned: success
    alternate:
      type: str
      description: Partition name of alternate partition to be used if the state of
        this partition is DRAIN or INACTIVE
      returned: success
    graceTime:
      type: int
      description: Specifies, in units of seconds, the preemption grace time to be
        extended to a job which has been selected for preemption
      returned: success
    defMemPerCPU:
      type: str
      description: Default real memory size available per allocated CPU in MegaBytes
      returned: success
    maxMemPerCPU:
      type: str
      description: Maximum real memory size available per allocated CPU in MegaBytes
      returned: success
    defMemPerNode:
      type: str
      description: Default real memory size available per allocated node in MegaBytes
      returned: success
    maxMemPerNode:
      type: str
      description: Maximum real memory size available per allocated node in MegaBytes
      returned: success
    preemptMode:
      type: str
      description: Mechanism used to preempt jobs from this partition
      returned: success
    reqResv:
      type: str
      description: Specifies users of this partition are required to designate a reservation
        when submitting a job
      returned: success
    SelectTypeParameters:
      type: str
      description: Partition-specific resource allocation type
      returned: success
    allowAccounts:
      type: str
      description: Specify accounts which are allowed to run jobs
      returned: success
    allowQos:
      type: str
      description: Specify qos which are allowed to run jobs
      returned: success
    denyAccounts:
      type: str
      description: Specify accounts which are denied to run jobs
      returned: success
    denyQos:
      type: str
      description: Specify qos which are denied to run jobs
      returned: success
    lln:
      type: bool
      description: Schedule resources to jobs on the least loaded nodes
      returned: success
    maxCPUsPerNode:
      type: str
      description: Maximum number of CPUs on any node available to all jobs from this
        partition
      returned: success
    tresBillingWeights:
      type: str
      description: Billing weights of each TRES type that will be used in calculating
        the usage of a job
      returned: success
    defMemPerGPU:
      type: str
      description: Default  real  memory  size  available  per  allocated GPU in megabytes
      returned: success
    defCpuPerGPU:
      type: str
      description: Default count of CPUs allocated per allocated GPU
      returned: success
    cpuBind:
      type: str
      description: How tasks are bound to allocated CPUs
      returned: success
    qos:
      type: str
      description: Used to extend the limits available to a QOS on a partition
      returned: success
    exclusiveUser:
      type: bool
      description: If set to YES then nodes will be exclusively allocated to users
      returned: success
    ordering:
      type: int
      description: Positioning of the jobqueue. Smaller values go first in the configuration
        file.
      returned: success
    allocNodes:
      type: list
      description: Nodes from which users can submit jobs in the partition of managed
        nodes
      returned: success
    state:
      type: str
      description: State of partition or availability for use.
      returned: success
    nodesets:
      type: str
      description: List of nodesets that will be added to Slurm partition
      returned: success

"""
############################
# Imports
############################

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import SlurmJobQueue
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.slurm_job_queue import SlurmJobQueue_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=SlurmJobQueue_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, SlurmJobQueue)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(SlurmJobQueue, params, commit=not module.check_mode)
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