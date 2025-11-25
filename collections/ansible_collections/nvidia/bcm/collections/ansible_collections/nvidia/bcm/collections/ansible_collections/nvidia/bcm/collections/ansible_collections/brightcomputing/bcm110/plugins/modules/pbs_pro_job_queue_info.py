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
module: pbs_pro_job_queue_info
description: Query cmdaemon for entity of type PbsProJobQueue
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
pbs_pro_job_queue:
  type: list
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

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import PbsProJobQueue
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

    results = entity_query.find(PbsProJobQueue)

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

    module.exit_json(pbs_pro_job_queues=json_ready_result, changed=False)


if __name__ == '__main__':
    main()