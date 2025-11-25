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
module: slurm_wlm_cluster_info
description: Query cmdaemon for entity of type SlurmWlmCluster
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
slurm_wlm_cluster:
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
    placeholders:
      type: list
      description: Job queue node placeholders mode
      returned: success
    cgroups:
      type: complex
      description: Submode containing Slurm related cgroups settings
      returned: success
    powerSavingEnabled:
      type: bool
      description: Enable power saving options into slurm.conf
      returned: success
    suspendTime:
      type: int
      description: ' Nodes which remain idle for this number of seconds will be placed
        into power save mode by SuspendProgram'
      returned: success
    suspendTimeout:
      type: int
      description: Maximum time permitted (in second) between when a node suspend
        request is issued and when the node shutdown
      returned: success
    resumeTimeout:
      type: int
      description: Maximum time permitted (in second) between when a node is resume
        request is issued and when the node is actually available for use
      returned: success
    suspendProgram:
      type: str
      description: Program that will be executed when a node remains idle for an extended
        period of time
      returned: success
    resumeProgram:
      type: str
      description: Program that will be executed when a suspended node is needed by
        a submitted jobs
      returned: success
    prologSlurmctld:
      type: str
      description: Fully qualified pathname of a program for the slurmctld daemon
        to execute before granting a new job allocation
      returned: success
    epilogSlurmctld:
      type: str
      description: Fully qualified pathname of a program for the slurmctld to execute
        upon termination of a job allocation
      returned: success
    prolog:
      type: str
      description: Fully qualified pathname of a program for the slurmd to execute
        whenever it is asked to run a job step from a new job allocation
      returned: success
    epilog:
      type: str
      description: Fully qualified pathname of a script to execute as user root on
        every node when a user's job completes
      returned: success
    taskProlog:
      type: str
      description: Fully qualified pathname of a script to execute prior to launching
        job step (invoked by slurmstepd).
      returned: success
    taskEpilog:
      type: str
      description: Fully qualified pathname of a script to execute after completion
        of job step (invoked by slurmstepd).
      returned: success
    srunProlog:
      type: str
      description: Fully qualified pathname of a script to execute prior to launching
        job step (invoked by srun).
      returned: success
    srunEpilog:
      type: str
      description: Fully qualified pathname of a script to execute after completion
        of job step (invoked by srun).
      returned: success
    gresTypes:
      type: str
      description: A list of generic resources to be managed
      returned: success
    prologEpilogTimeout:
      type: int
      description: The interval in seconds Slurm waits for Prolog and Epilog before
        terminating them (value 0 removes the parameter from slurm.conf)
      returned: success
    batchStartTimeout:
      type: int
      description: The maximum time (in seconds) that a batch job is permitted for
        launching before being considered missing and releasing the allocation (value
        0 removes the parameter from slurm.conf)
      returned: success
    prefix:
      type: str
      description: Slurm root installation directory
      returned: success
    etc:
      type: str
      description: Slurm configuration files directory
      returned: success
    stateSave:
      type: str
      description: Directory into which the Slurm controller saves its state
      returned: success
    version:
      type: str
      description: Major Slurm version
      returned: success
    slurmConfFileTemplate:
      type: str
      description: Template for slurm.conf file
      returned: success
    gresConfFileTemplate:
      type: str
      description: Template for gres.conf file
      returned: success
    autoDetect:
      type: str
      description: Detect NVIDIA (nvml/nvidia) or AMD (rsmi) or Intel (oneapi) GPUs
        or AWS Trainium/Inferentia devices (nrt) automatically (per node), or use
        the cluster manager autodetection (bcm). GPU configuration is part of Slurm
        GRES.
      returned: success
    configureMigs:
      type: bool
      description: Detect and configure MIG profiles as GPU types in Slurm
      returned: success
    slurmdParameters:
      type: str
      description: Parameters specific to the Slurmd
      returned: success
    scheduler:
      type: str
      description: Scheduler to use in combination with slurm
      returned: success
    schedulerParameters:
      type: str
      description: Parameters specific to the scheduler. The interpretation of them
        varies by SchedulerType
      returned: success
    slurmctldParameters:
      type: str
      description: Parameters specific to the Slurmctld
      returned: success
    prologFlags:
      type: str
      description: Flags to control the prolog behavior
      returned: success
    selectType:
      type: str
      description: 'The type of resource selection algorithm to be used (slurm: SelectType)'
      returned: success
    selectTypeParameters:
      type: str
      description: 'Parameters specific to Select Type (slurm: SelectTypeParameters)'
      returned: success
    accountingStorageTRES:
      type: str
      description: 'List of resources you wish to track on the cluster (slurm: AccountingStorageTRES)'
      returned: success
    accountingStoreFlags:
      type: str
      description: 'List used to tell the slurmctld to store extra fields that may
        be more heavy weight than the normal job information (slurm: AccoutingStoreFlags)'
      returned: success
    ociSettings:
      type: complex
      description: OCI container settings for Slurm
      returned: success
    drainReasonPolicy:
      type: str
      description: The policy defines how a new drain reason is applied when another
        one already presents
      returned: success
    topologySettings:
      type: complex
      description: Topology settings for Slurm
      returned: success
    bcmManagedParameters:
      type: str
      description: Fields in slurm.conf that will be controlled by cmdaemon (case
        insensitive)
      returned: success
    prsSettings:
      type: complex
      description: PRS settings for Slurm
      returned: success
    licenses:
      type: list
      description: Specification of licenses (or other resources available on all
        nodes of the cluster) which can be allocated to jobs.
      returned: success
    cgroupPlugin:
      type: str
      description: Specify the plugin to be used when interacting with the cgroup
        subsystem.
      returned: success

"""
############################
# Imports
############################

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import SlurmWlmCluster
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

    results = entity_query.find(SlurmWlmCluster)

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

    module.exit_json(slurm_wlm_clusters=json_ready_result, changed=False)


if __name__ == '__main__':
    main()