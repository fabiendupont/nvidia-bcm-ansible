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
module: slurm_job_queue_info
description: Query cmdaemon for entity of type SlurmJobQueue
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
slurm_job_queue:
  type: list
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

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import SlurmJobQueue
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

    results = entity_query.find(SlurmJobQueue)

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

    module.exit_json(slurm_job_queues=json_ready_result, changed=False)


if __name__ == '__main__':
    main()