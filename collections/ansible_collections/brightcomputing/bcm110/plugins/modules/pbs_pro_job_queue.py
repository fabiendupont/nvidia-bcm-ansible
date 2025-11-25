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
module: pbs_pro_job_queue
description: ['PBSPro job queue']
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
    queueType:
      description:
      - Pbs Pro queue type
      type: str
      required: false
      default: EXECUTION
      choices:
      - EXECUTION
      - ROUTE
    fromRouteOnly:
      description:
      - Receive jobs from route queues only
      type: bool
      required: false
      default: false
    routeHeldJobs:
      description:
      - Specifies whether jobs in the held state can be routed from this queue
      type: bool
      required: false
      default: false
    routeWaitingJobs:
      description:
      - Specifies whether jobs whose execution_time attribute value is in the future can
        be routed from this queue
      type: bool
      required: false
      default: false
    routeLifetime:
      description:
      - The maximum time a job is allowed to reside in a routing queue
      type: int
      required: false
      default: 0
    routeRetryTime:
      description:
      - Route retry time in routing queue
      type: int
      required: false
      default: 0
    routes:
      description:
      - Route of queue path (route_destination parameter in qmgr)
      type: list
      required: false
      default: []
    defaultQueue:
      description:
      - Specifies the queue which is to accept jobs when no queue is requested
      type: bool
      required: false
      default: false
    minWalltime:
      description:
      - Minimum runtime of jobs running in a queue
      type: str
      required: false
      default: 00:00:00
    maxWalltime:
      description:
      - Maximum runtime of jobs running in a queue
      type: str
      required: false
      default: '240:00:00'
    defaultWalltime:
      description:
      - Default maximum runtime of jobs running in a queue
      type: str
      required: false
    maxQueued:
      description:
      - Maximum number allowed to reside in a queue at any given time (0 is the same as
        infinite)
      type: int
      required: false
      default: 0
    maxRunning:
      description:
      - Maximum number of jobs allowed to run at any given time (0 is the same as infinite)
      type: int
      required: false
      default: 0
    priority:
      description:
      - Priority of a queue against other queues of the same type [-1024; 1024]
      type: int
      required: false
      default: 0
    enabled:
      description:
      - When true, a queue will accept new jobs; when false, a queue is disabled and will
        not accept jobs
      type: bool
      required: false
      default: true
    started:
      description:
      - Jobs may be scheduled for execution from this queue; when false, a queue is considered
        stopped
      type: bool
      required: false
      default: true
    aclHostEnable:
      description:
      - When true directs the server to use the acl_hosts access list for the named queue
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
pbs_pro_job_queue:
  type: complex
  description: PBSPro job queue
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
    queueType:
      type: str
      description: Pbs Pro queue type
      returned: success
    fromRouteOnly:
      type: bool
      description: Receive jobs from route queues only
      returned: success
    routeHeldJobs:
      type: bool
      description: Specifies whether jobs in the held state can be routed from this
        queue
      returned: success
    routeWaitingJobs:
      type: bool
      description: Specifies whether jobs whose execution_time attribute value is
        in the future can be routed from this queue
      returned: success
    routeLifetime:
      type: int
      description: The maximum time a job is allowed to reside in a routing queue
      returned: success
    routeRetryTime:
      type: int
      description: Route retry time in routing queue
      returned: success
    routes:
      type: str
      description: Route of queue path (route_destination parameter in qmgr)
      returned: success
    defaultQueue:
      type: bool
      description: Specifies the queue which is to accept jobs when no queue is requested
      returned: success
    minWalltime:
      type: str
      description: Minimum runtime of jobs running in a queue
      returned: success
    maxWalltime:
      type: str
      description: Maximum runtime of jobs running in a queue
      returned: success
    defaultWalltime:
      type: str
      description: Default maximum runtime of jobs running in a queue
      returned: success
    maxQueued:
      type: int
      description: Maximum number allowed to reside in a queue at any given time (0
        is the same as infinite)
      returned: success
    maxRunning:
      type: int
      description: Maximum number of jobs allowed to run at any given time (0 is the
        same as infinite)
      returned: success
    priority:
      type: int
      description: Priority of a queue against other queues of the same type [-1024;
        1024]
      returned: success
    enabled:
      type: bool
      description: When true, a queue will accept new jobs; when false, a queue is
        disabled and will not accept jobs
      returned: success
    started:
      type: bool
      description: Jobs may be scheduled for execution from this queue; when false,
        a queue is considered stopped
      returned: success
    aclHostEnable:
      type: bool
      description: When true directs the server to use the acl_hosts access list for
        the named queue
      returned: success

"""
############################
# Imports
############################

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import PbsProJobQueue
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.pbs_pro_job_queue import PbsProJobQueue_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=PbsProJobQueue_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, PbsProJobQueue)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(PbsProJobQueue, params, commit=not module.check_mode)
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