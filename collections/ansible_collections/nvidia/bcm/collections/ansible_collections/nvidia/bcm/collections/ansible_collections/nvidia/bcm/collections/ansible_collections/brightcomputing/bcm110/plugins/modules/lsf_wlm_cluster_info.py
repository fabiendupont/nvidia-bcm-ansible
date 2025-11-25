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
module: lsf_wlm_cluster_info
description: Query cmdaemon for entity of type LSFWlmCluster
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
lsf_wlm_cluster:
  type: list
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
      description: Major LSF version
      returned: success
    prefix:
      type: str
      description: LSF installation directory
      returned: success
    var:
      type: str
      description: Var directory location
      returned: success
    localVar:
      type: str
      description: Local var directory location
      returned: success
    logDir:
      type: str
      description: Logging directory location (LSF_LOGDIR in lsf.conf)
      returned: success
    dynamicCloudNodes:
      type: bool
      description: Cloud nodes are added dynamically to LSF
      returned: success
    placeholders:
      type: list
      description: Job queue node placeholders mode
      returned: success
    cgroups:
      type: complex
      description: Submode containing LSF related cgroups settings
      returned: success
    doBackups:
      type: bool
      description: Backup configuration file before update
      returned: success
    gpuAutoconfig:
      type: bool
      description: Enable GPU autodetection (LSF_GPU_AUTOCONFIG in lsf.conf)
      returned: success
    gpuNewSyntax:
      type: bool
      description: Enable new GPU request syntax (LSB_GPU_NEW_SYNTAX in lsf.conf)
      returned: success
    dcgmPort:
      type: int
      description: Enable DCGM features and specifies the port number that LSF uses
        to communicate with the DCGM daemon (0 for disabled)
      returned: success
    unitForLimits:
      type: str
      description: Enables scaling of large units in the resource usage limits (LSF_UNIT_FOR_LIMITS
        in lsf.conf)
      returned: success
    noQueueHostsString:
      type: str
      description: String that is used to replace empty nodes list for a queue
      returned: success
    enableEgo:
      type: bool
      description: Enable EGO functionality (LSF_ENABLE_EGO in lsf.conf)
      returned: success
    dynamicHostWaitTime:
      type: int
      description: Defines the length of time in seconds that a dynamic host awaits
        communicating with the master host LIM to either add the host to the cluster
        or to shut down any running daemons if the host is not added successfully.
        Note that the time will be truncated to the minute (LSF_DYNAMIC_HOST_WAIT_TIME
        in lsf.conf)
      returned: success
    hostAddressRange:
      type: str
      description: Identifies the range of IP addresses that are allowed to be LSF
        hosts that can be dynamically added to or removed from the cluster (LSF_HOST_ADDR_RANGE
        in lsf.conf)
      returned: success
    manageMIG:
      type: bool
      description: enable dynamic MIG scheduling (LSF_MANAGE_MIG in lsf.conf)
      returned: success

"""
############################
# Imports
############################

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import LSFWlmCluster
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

    results = entity_query.find(LSFWlmCluster)

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

    module.exit_json(lsf_wlm_clusters=json_ready_result, changed=False)


if __name__ == '__main__':
    main()