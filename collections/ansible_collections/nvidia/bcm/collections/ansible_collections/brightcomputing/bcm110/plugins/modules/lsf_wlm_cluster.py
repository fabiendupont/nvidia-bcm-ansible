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
module: lsf_wlm_cluster
description: ['Manages lsf_wlm_clusters']
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
      - Major LSF version
      type: str
      required: false
      choices:
      - '10.1'
    prefix:
      description:
      - LSF installation directory
      type: str
      required: false
    var:
      description:
      - Var directory location
      type: str
      required: false
      default: /cm/shared/apps/lsf/var
    localVar:
      description:
      - Local var directory location
      type: str
      required: false
      default: /cm/local/apps/lsf/var
    logDir:
      description:
      - Logging directory location (LSF_LOGDIR in lsf.conf)
      type: str
      required: false
      default: /cm/local/apps/lsf/var/log
    dynamicCloudNodes:
      description:
      - Cloud nodes are added dynamically to LSF
      type: bool
      required: false
      default: false
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
      - Submode containing LSF related cgroups settings
      type: dict
      required: false
      options:
        mountPoint:
          description:
          - Where cgroups is mounted
          type: str
          required: false
          default: /sys/fs/cgroup
        resourceEnforce:
          description:
          - Controls resource enforcement through the Linux cgroup memory and cpuset subsytem
            on Linux systems with cgroup support (LSB_RESOURCE_ENFORCE)
          type: list
          required: false
          default:
          - memory
          - cpu
        processTracking:
          description:
          - Enable this parameter to track processes based on job control functions such
            as termination, suspension, resume and other signaling, on Linux systems which
            support cgroups freezer subsystem (LSF_PROCESS_TRACKING)
          type: bool
          required: false
          default: true
        linuxCgroupAccounting:
          description:
          - Enable this parameter to track processes based on CPU and memory accounting
            for Linux systems that support cgroup's memory and cpuacct subsystems (LSF_LINUX_CGROUP_ACCT)
          type: bool
          required: false
          default: true
        jobCgroupTemplate:
          description:
          - Template for job cgroup path ($CLUSTER will be replaced to LSF cluster name,
            $JOBID will be replaced to job id)
          type: str
          required: false
          default: lsf/$CLUSTER/job.$JOBID.*
    doBackups:
      description:
      - Backup configuration file before update
      type: bool
      required: false
      default: true
    gpuAutoconfig:
      description:
      - Enable GPU autodetection (LSF_GPU_AUTOCONFIG in lsf.conf)
      type: bool
      required: false
      default: false
    gpuNewSyntax:
      description:
      - Enable new GPU request syntax (LSB_GPU_NEW_SYNTAX in lsf.conf)
      type: bool
      required: false
      default: false
    dcgmPort:
      description:
      - Enable DCGM features and specifies the port number that LSF uses to communicate
        with the DCGM daemon (0 for disabled)
      type: int
      required: false
      default: 0
    unitForLimits:
      description:
      - Enables scaling of large units in the resource usage limits (LSF_UNIT_FOR_LIMITS
        in lsf.conf)
      type: str
      required: false
      default: MB
    noQueueHostsString:
      description:
      - String that is used to replace empty nodes list for a queue
      type: str
      required: false
    enableEgo:
      description:
      - Enable EGO functionality (LSF_ENABLE_EGO in lsf.conf)
      type: bool
      required: false
      default: false
    dynamicHostWaitTime:
      description:
      - Defines the length of time in seconds that a dynamic host awaits communicating
        with the master host LIM to either add the host to the cluster or to shut down
        any running daemons if the host is not added successfully. Note that the time
        will be truncated to the minute (LSF_DYNAMIC_HOST_WAIT_TIME in lsf.conf)
      type: int
      required: false
      default: 18000
    hostAddressRange:
      description:
      - Identifies the range of IP addresses that are allowed to be LSF hosts that can
        be dynamically added to or removed from the cluster (LSF_HOST_ADDR_RANGE in lsf.conf)
      type: str
      required: false
      default: '*.*'
    manageMIG:
      description:
      - enable dynamic MIG scheduling (LSF_MANAGE_MIG in lsf.conf)
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
lsf_wlm_cluster:
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

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import LSFWlmCluster
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.lsf_wlm_cluster import LSFWlmCluster_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=LSFWlmCluster_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, LSFWlmCluster)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(LSFWlmCluster, params, commit=not module.check_mode)
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