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
module: slurm_wlm_cluster
description: ['Manages slurm_wlm_clusters']
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
      - Submode containing Slurm related cgroups settings
      type: dict
      required: false
      options:
        mountPoint:
          description:
          - Where cgroups is mounted
          type: str
          required: false
          default: /sys/fs/cgroup
        constrainCores:
          description:
          - If true then constrain allowed cores to the subset of allocated resources
          type: bool
          required: false
          default: false
        constrainRAMSpace:
          description:
          - If true then constrain the job's RAM usage
          type: bool
          required: false
          default: false
        constrainSwapSpace:
          description:
          - If true then constrain the job's swap space usage
          type: bool
          required: false
          default: false
        constrainDevices:
          description:
          - If true constrain the job's allowed devices based on GRES allocated resources
          type: bool
          required: false
          default: false
        allowedRamSpace:
          description:
          - Constrain the job cgroup RAM to this percentage of the allocated memory. If
            the AllowedRAMSpace limit is exceeded, the job steps will be killed and a
            warning message will be written to standard error. Also see ConstrainRAMSpace.
          type: float
          required: false
          default: 1
        allowedSwapSpace:
          description:
          - Constrain the job cgroup swap space to this percentage of the allocated memory
          type: float
          required: false
          default: 0
        maxRAM:
          description:
          - Set an upper bound of total RAM on the RAM constraint for a job
          type: float
          required: false
          default: 1
        maxSwap:
          description:
          - Set an upper bound (of total RAM) on the amount of RAM+Swap that may be used
            for a job
          type: float
          required: false
          default: 1
        minRAMSpace:
          description:
          - Set a lower bound on the memory limits defined by AllowedRAMSpace and AllowedSwapSpace
          type: int
          required: false
          default: 31457280
        jobCgroupTemplate:
          description:
          - Template for job cgroup/v1 path ($UID will be replaced to user ID, $JOBID
            will be replaced to job id)
          type: str
          required: false
          default: slurm/uid_$UID/job_$JOBID
        jobCgroupV2Template:
          description:
          - Template for job cgroup/v2 path ($JOBID will be replaced to job id)
          type: str
          required: false
          default: system.slice/slurmstepd.scope/job_$JOBID
        memorySwappiness:
          description:
          - Configure the kernel's priority for swapping out anonymous pages (such as
            program data) verses file cache pages for the job cgroup (either ConstrainRAMSpace
            or ConstrainSwapSpace must be enabled in order for this parameter to be applied)
          type: float
          required: false
          default: 1
    powerSavingEnabled:
      description:
      - Enable power saving options into slurm.conf
      type: bool
      required: false
      default: false
    suspendTime:
      description:
      - Nodes which remain idle for this number of seconds will be placed into power save
        mode by SuspendProgram
      type: int
      required: false
      default: 300
    suspendTimeout:
      description:
      - Maximum time permitted (in second) between when a node suspend request is issued
        and when the node shutdown
      type: int
      required: false
      default: 30
    resumeTimeout:
      description:
      - Maximum time permitted (in second) between when a node is resume request is issued
        and when the node is actually available for use
      type: int
      required: false
      default: 60
    suspendProgram:
      description:
      - Program that will be executed when a node remains idle for an extended period
        of time
      type: str
      required: false
      default: /cm/local/apps/slurm/current/scripts/power/poweroff
    resumeProgram:
      description:
      - Program that will be executed when a suspended node is needed by a submitted jobs
      type: str
      required: false
      default: /cm/local/apps/slurm/current/scripts/power/poweron
    prologSlurmctld:
      description:
      - Fully qualified pathname of a program for the slurmctld daemon to execute before
        granting a new job allocation
      type: str
      required: false
    epilogSlurmctld:
      description:
      - Fully qualified pathname of a program for the slurmctld to execute upon termination
        of a job allocation
      type: str
      required: false
    prolog:
      description:
      - Fully qualified pathname of a program for the slurmd to execute whenever it is
        asked to run a job step from a new job allocation
      type: str
      required: false
      default: /cm/local/apps/cmd/scripts/prolog
    epilog:
      description:
      - Fully qualified pathname of a script to execute as user root on every node when
        a user's job completes
      type: str
      required: false
      default: /cm/local/apps/cmd/scripts/epilog
    taskProlog:
      description:
      - Fully qualified pathname of a script to execute prior to launching job step (invoked
        by slurmstepd).
      type: str
      required: false
    taskEpilog:
      description:
      - Fully qualified pathname of a script to execute after completion of job step (invoked
        by slurmstepd).
      type: str
      required: false
    srunProlog:
      description:
      - Fully qualified pathname of a script to execute prior to launching job step (invoked
        by srun).
      type: str
      required: false
    srunEpilog:
      description:
      - Fully qualified pathname of a script to execute after completion of job step (invoked
        by srun).
      type: str
      required: false
    gresTypes:
      description:
      - A list of generic resources to be managed
      type: list
      required: false
      default:
      - gpu
    prologEpilogTimeout:
      description:
      - The interval in seconds Slurm waits for Prolog and Epilog before terminating them
        (value 0 removes the parameter from slurm.conf)
      type: int
      required: false
      default: 0
    batchStartTimeout:
      description:
      - The maximum time (in seconds) that a batch job is permitted for launching before
        being considered missing and releasing the allocation (value 0 removes the parameter
        from slurm.conf)
      type: int
      required: false
      default: 0
    prefix:
      description:
      - Slurm root installation directory
      type: str
      required: false
    etc:
      description:
      - Slurm configuration files directory
      type: str
      required: false
    stateSave:
      description:
      - Directory into which the Slurm controller saves its state
      type: str
      required: false
    version:
      description:
      - Major Slurm version
      type: str
      required: false
      choices:
      - '24.05'
      - 24.05-sharp
      - '24.11'
      - 24.11-sharp
      - '25.05'
      - 25.05-sharp
    slurmConfFileTemplate:
      description:
      - Template for slurm.conf file
      type: str
      required: false
    gresConfFileTemplate:
      description:
      - Template for gres.conf file
      type: str
      required: false
    autoDetect:
      description:
      - Detect NVIDIA (nvml/nvidia) or AMD (rsmi) or Intel (oneapi) GPUs or AWS Trainium/Inferentia
        devices (nrt) automatically (per node), or use the cluster manager autodetection
        (bcm). GPU configuration is part of Slurm GRES.
      type: str
      required: false
      default: NONE
      choices:
      - NONE
      - 'OFF'
      - NVML
      - RSMI
      - ONEAPI
      - BCM
      - NRT
      - NVIDIA
    configureMigs:
      description:
      - Detect and configure MIG profiles as GPU types in Slurm
      type: bool
      required: false
      default: true
    slurmdParameters:
      description:
      - Parameters specific to the Slurmd
      type: list
      required: false
      default: []
    scheduler:
      description:
      - Scheduler to use in combination with slurm
      type: str
      required: false
      default: backfill
      choices:
      - backfill
      - builtin
    schedulerParameters:
      description:
      - Parameters specific to the scheduler. The interpretation of them varies by SchedulerType
      type: list
      required: false
      default: []
    slurmctldParameters:
      description:
      - Parameters specific to the Slurmctld
      type: list
      required: false
      default: []
    prologFlags:
      description:
      - Flags to control the prolog behavior
      type: list
      required: false
      default:
      - Alloc
    selectType:
      description:
      - 'The type of resource selection algorithm to be used (slurm: SelectType)'
      type: str
      required: false
      default: select/cons_tres
    selectTypeParameters:
      description:
      - 'Parameters specific to Select Type (slurm: SelectTypeParameters)'
      type: list
      required: false
      default:
      - CR_Core
    accountingStorageTRES:
      description:
      - 'List of resources you wish to track on the cluster (slurm: AccountingStorageTRES)'
      type: list
      required: false
      default:
      - gres/gpu
    accountingStoreFlags:
      description:
      - 'List used to tell the slurmctld to store extra fields that may be more heavy
        weight than the normal job information (slurm: AccoutingStoreFlags)'
      type: list
      required: false
      default:
      - job_comment
    ociSettings:
      description:
      - OCI container settings for Slurm
      type: dict
      required: false
      options:
        containerPath:
          description:
          - Override path pattern for placement of the generated OCI Container bundle
            directory.
          type: str
          required: false
        createEnvFile:
          description:
          - Create environment file for container.
          type: bool
          required: false
          default: false
        runTimeCreate:
          description:
          - Pattern for OCI runtime create operation.
          type: str
          required: false
        runTimeDelete:
          description:
          - Pattern for OCI runtime delete operation.
          type: str
          required: false
        runTimeKill:
          description:
          - Pattern for OCI runtime kill operation.
          type: str
          required: false
        runTimeQuery:
          description:
          - Pattern for OCI runtime query operation.
          type: str
          required: false
        runTimeRun:
          description:
          - Pattern for OCI runtime run operation.
          type: str
          required: false
        runTimeStart:
          description:
          - Pattern for OCI runtime start operation.
          type: str
          required: false
    drainReasonPolicy:
      description:
      - The policy defines how a new drain reason is applied when another one already
        presents
      type: str
      required: false
      default: REPLACE
      choices:
      - REPLACE
      - APPEND
      - SKIP
    topologySettings:
      description:
      - Topology settings for Slurm
      type: dict
      required: false
      options:
        topologyPlugin:
          description:
          - Slurm topology plugin
          type: str
          required: false
          default: NONE
          choices:
          - NONE
          - DEFAULT
          - TREE
          - BLOCK
          - TORUS
        topologySource:
          description:
          - Source of information for topology construction
          type: str
          required: false
          default: NONE
          choices:
          - NONE
          - INTERNAL
          - TOPOGRAPH
        params:
          description:
          - Topology parameters for Slurm
          type: dict
          required: false
          options:
            dragonfly:
              description:
              - Enable allocation optimization for Dragonfly network (TopologyParam=Dragonfly)
              type: bool
              required: false
              default: false
            routePart:
              description:
              - Instead  of using the plugin's default route calculation, use partition
                node lists to route communications from the controller (TopologyParam=RoutePart)
              type: bool
              required: false
              default: false
            switchAsNodeRank:
              description:
              - Assign  the  same  node  rank  to  all nodes under one leaf switch (TopologyParam=SwitchAsNodeRank)
              type: bool
              required: false
              default: false
            routeTree:
              description:
              - Use the switch hierarchy defined in a topology.conf file for routing instead
                of just scheduling (TopologyParam=RouteTree)
              type: bool
              required: false
              default: false
            topoOptional:
              description:
              - Only optimize allocation for network topology if the job includes a switch
                option (TopologyParam=TopoOptional)
              type: bool
              required: false
              default: false
        treeSettings:
          description:
          - Tree topology plugin settings
          type: dict
          required: false
          options:
            topologySwitches:
              description:
              - List of switches that should be used to write the topology file
              type: list
              required: false
              default: []
            topologyEphemeralSwitches:
              description:
              - Add ephemeral switches to topology.conf
              type: bool
              required: false
              default: true
        blockSettings:
          description:
          - Block topology plugin settings
          type: dict
          required: false
          options:
            blockSizes:
              description:
              - List of the planning base block size, alongside any higher-level block
                sizes that would be enforced by topology/block plugin
              type: list
              required: false
              default: []
            blockEntity:
              description:
              - What BCM entity represents a block
              type: str
              required: false
              default: RACK
              choices:
              - RACK
              - NODEGROUP
            allowedRacks:
              description:
              - List of racks that will be used as blocks (if empty then all racks will
                be used)
              type: list
              required: false
              default: []
            allowedNodeGroups:
              description:
              - List of nodegroups that will be used as blocks (if empty then all nodegroups
                will be used)
              type: list
              required: false
              default: []
        topographSettings:
          description:
          - Topograph service integaration settings
          type: dict
          required: false
          options:
            hostname:
              description:
              - Hostname where topograph runs
              type: str
              required: false
              default: localhost
            configPath:
              description:
              - Path to topograph configuration file
              type: str
              required: false
              default: /etc/topograph/topograph-config.yaml
            httpParameters:
              description:
              - Parameters string that is passed to the service HTTP API
              type: str
              required: false
            passCloudCredentials:
              description:
              - Specifies whether the CSP credentials will be passed to the topology generator
              type: bool
              required: false
              default: false
            fetchTimeout:
              description:
              - Topograph API timeout
              type: int
              required: false
              default: 20
            fetchAttempts:
              description:
              - Number of attempts to get topology from topograph
              type: int
              required: false
              default: 12
            fetchWaitTime:
              description:
              - Wait time in seconds between fetching attempts
              type: int
              required: false
              default: 15
    bcmManagedParameters:
      description:
      - Fields in slurm.conf that will be controlled by cmdaemon (case insensitive)
      type: list
      required: false
      default:
      - AccountingStorageBackupHost
      - AccountingStorageHost
      - AccountingStorageTRES
      - AccountingStoreFlags
      - BatchStartTimeout
      - ClusterName
      - Epilog
      - EpilogSlurmctld
      - GresTypes
      - Licenses
      - Prolog
      - PrologEpilogTimeout
      - PrologFlags
      - PrologSlurmctld
      - ResumeProgram
      - ResumeTimeout
      - SchedulerParameters
      - SchedulerType
      - SelectType
      - SelectTypeParameters
      - SlurmctldAddr
      - SlurmctldHost
      - SlurmctldParameters
      - SlurmdParameters
      - SrunEpilog
      - SrunProlog
      - StateSaveLocation
      - SuspendProgram
      - SuspendTime
      - SuspendTimeout
      - TaskEpilog
      - TaskProlog
      - TopologyParam
      - TopologyPlugin
    prsSettings:
      description:
      - PRS settings for Slurm
      type: dict
      required: false
      options:
        certificatePath:
          description:
          - Complete path where Slurm can find the certificate it needs to use to contact
            PRS
          type: str
          required: false
          default: /cm/local/apps/prs/etc/${WLM_NAME}.pem
        privateKeyPath:
          description:
          - Complete path where Slurm can find the private key it needs to use to contact
            PRS
          type: str
          required: false
          default: /cm/local/apps/prs/etc/${WLM_NAME}.key
    licenses:
      description:
      - Specification of licenses (or other resources available on all nodes of the cluster)
        which can be allocated to jobs.
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - License name
          type: str
          required: true
        count:
          description:
          - License number
          type: int
          required: false
          default: 0
    cgroupPlugin:
      description:
      - Specify the plugin to be used when interacting with the cgroup subsystem.
      type: str
      required: false
      default: AUTODETECT
      choices:
      - CGROUPV1
      - CGROUPV2
      - AUTODETECT
      - DISABLED

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
slurm_wlm_cluster:
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

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import SlurmWlmCluster
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.slurm_wlm_cluster import SlurmWlmCluster_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=SlurmWlmCluster_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, SlurmWlmCluster)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(SlurmWlmCluster, params, commit=not module.check_mode)
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