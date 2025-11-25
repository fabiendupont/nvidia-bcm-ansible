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
module: configuration_overlay
description: ['Configuration overlay']
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
    allHeadNodes:
      description:
      - All head nodes
      type: bool
      required: false
      default: false
    nodes:
      description:
      - List of nodes belonging to this group
      type: list
      required: false
      default: []
    categories:
      description:
      - List of categories belonging to this group
      type: list
      required: false
      default: []
    customizationFiles:
      description:
      - Config file customizations
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description: []
          type: str
          required: true
        entries:
          description:
          - Config file customization entries
          type: list
          required: false
          default: []
          elements: dict
          options:
            key:
              description:
              - Name of the key
              type: str
              required: true
            value:
              description:
              - Value for the key
              type: str
              required: false
            enabled:
              description: []
              type: bool
              required: false
              default: true
            action:
              description:
              - Determines how entres are added
              type: str
              required: false
              default: SMART_ADD
              choices:
              - SMART_ADD
              - APPEND
              - PREPEND
              - REMOVE
              - PRESERVE
              - DEFAULT
            formatting:
              description: []
              type: str
              required: false
            separator:
              description: []
              type: str
              required: false
        label:
          description: []
          type: str
          required: false
        type:
          description:
          - Determines file type
          type: str
          required: false
          default: Generic
          choices:
          - ENV
          - INI
          - Generic
        managedsection:
          description:
          - Determines how cmdaemon should customize the file
          type: str
          required: false
          default: ENTIRE_FILE
          choices:
          - BEGIN_OF_FILE
          - END_OF_FILE
          - FORCE_BEGIN_OF_FILE
          - FORCE_END_OF_FILE
          - ENTIRE_FILE
          - NONE
        formatting:
          description: []
          type: str
          required: false
        enabled:
          description: []
          type: bool
          required: false
          default: true
    priority:
      description:
      - Priority of the roles, node roles have a 750 priority, and category roles 250,
        set to -1 disable the overlay
      type: int
      required: false
      default: 500
    roles_PbsProSubmitRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        pbsProWlmClusters:
          description:
          - List of PbsPro clusters which the role belongs to
          type: list
          required: false
          default: []
    roles_BeeGFSManagementRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        configurations:
          description:
          - List of BeeGFS management configurations
          type: list
          required: false
          default: []
          elements: dict
          options:
            ref_beegfs_cluster_uuid:
              description:
              - BeeGFS cluster
              - (Field should be formatted as a UUID)
              type: str
              required: true
              default: None
            dataDir:
              description:
              - Path to the data directory
              type: str
              required: false
              default: /var/lib/beegfs/management
            allowNewServers:
              description:
              - Allow new servers registration
              type: bool
              required: false
              default: true
            allowNewTargets:
              description:
              - Allow new storage targets registration
              type: bool
              required: false
              default: true
            targetOfflineTimeout:
              description:
              - Timeout until targets on a storage server are considered offline when
                no target status is received
              type: int
              required: false
              default: 180
            clientAutoRemove:
              description:
              - Time after which an unreachable node is considered dead
              type: int
              required: false
              default: 1800
            numberOfWorkers:
              description:
              - Number of worker threads
              type: int
              required: false
              default: 4
            metaDynamicPools:
              description:
              - Raise lower limits if difference in capacity becomes too large between
                targets
              type: bool
              required: false
              default: true
            metaInodesLowLimit:
              description:
              - Metadata inode free space pool threshold
              type: str
              required: false
              default: 10M
            metaInodesEmergencyLimit:
              description:
              - Metadata inode free space pool threshold
              type: str
              required: false
              default: 1M
            metaSpaceLowLimit:
              description:
              - Meta space low limit
              type: int
              required: false
              default: 10000000000
            metaSpaceEmergencyLimit:
              description:
              - Meta space emergency limit
              type: int
              required: false
              default: 3000000000
            storageDynamicPools:
              description:
              - Raise lower limits if difference in capacity becomes too large between
                targets
              type: bool
              required: false
              default: true
            storageInodesLowLimit:
              description:
              - Storage inode free space pool threshold
              type: int
              required: false
              default: 10000000
            storageInodesEmergencyLimit:
              description:
              - Storage inode free space pool threshold
              type: int
              required: false
              default: 1000000
            storageSpaceLowLimit:
              description:
              - Storage space free space pool threshold
              type: int
              required: false
              default: 1000000000000
            storageSpaceEmergencyLimit:
              description:
              - Storage space free space pool threshold
              type: int
              required: false
              default: 20000000000
            enableQuota:
              description:
              - Enable quota
              type: bool
              required: false
              default: false
            quotaQueryGIDFile:
              description:
              - Path to a file with GIDs to be checked by quota
              type: str
              required: false
            quotaGIDs:
              description:
              - GIDs to be checked by quota
              type: list
              required: false
              default: []
            quotaQueryGIDRange:
              description:
              - GID range to be checked by quota
              type: str
              required: false
            quotaQueryUIDFile:
              description:
              - Path to a file with UIDs to be checked by quota
              type: str
              required: false
            quotaUIDs:
              description:
              - UIDs to be checked by quota
              type: list
              required: false
              default: []
            quotaQueryUIDRange:
              description:
              - UID range to be checked by quota
              type: str
              required: false
            quotaQueryType:
              description:
              - Query type for quota
              type: str
              required: false
              default: system
            quotaQueryWithSystemUsersGroups:
              description:
              - Allow also system users/groups to be checked by quota
              type: bool
              required: false
              default: false
            quotaUpdateInterval:
              description:
              - Quota update interval
              type: int
              required: false
              default: 600
            connectionSettings:
              description:
              - Submode containing BeeGFS management connection settings
              type: dict
              required: false
              options:
                portTCP:
                  description:
                  - TCP port for the service
                  type: int
                  required: false
                  default: 8008
                portUDP:
                  description:
                  - UDP port for the service
                  type: int
                  required: false
                  default: 8008
                backlogTCP:
                  description:
                  - TCP listen backlog
                  type: int
                  required: false
                  default: 128
                interfacesFile:
                  description:
                  - Path to the file with a list of interfaces for communication
                  type: str
                  required: false
                interfacesList:
                  description:
                  - List of interfaces for communication
                  type: list
                  required: false
                  default: []
                netFilterFile:
                  description:
                  - Path to a file with a list of allowed IP subnets
                  type: str
                  required: false
                useRDMA:
                  description:
                  - Use RDMA
                  type: bool
                  required: false
                  default: true
            logSettings:
              description:
              - Submode containing BeeGFS logging settings
              type: dict
              required: false
              options:
                logType:
                  description:
                  - Defines the logger type. This can either be 'syslog' to send log messages
                    to the general system logger or 'logfile'
                  type: str
                  required: false
                  default: SYSLOG
                  choices:
                  - SYSLOG
                  - LOGFILE
                level:
                  description:
                  - Log level
                  type: int
                  required: false
                  default: 2
                noDate:
                  description:
                  - Do not show date along with time in log
                  type: bool
                  required: false
                  default: false
                numberOfLines:
                  description:
                  - Number of lines in log file, after which it will be rotated
                  type: int
                  required: false
                  default: 50000
                numberOfRotatedFiles:
                  description:
                  - Number of old log files to keep
                  type: int
                  required: false
                  default: 5
                file:
                  description:
                  - Path to the log file, empty means logs go to the journal
                  type: str
                  required: false
    roles_ScaleServerRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        dryRun:
          description:
          - Run in dry run mode
          type: bool
          required: false
          default: false
        debug:
          description:
          - Print debug messages to the log
          type: bool
          required: false
          default: false
        runInterval:
          description:
          - Frequency of cm-scale decision making (in seconds)
          type: int
          required: false
          default: 120
        advancedSettings:
          description:
          - Submode containing advanced settings
          type: dict
          required: false
          options:
            debug2:
              description:
              - Print very low level debug messages to the log
              type: bool
              required: false
              default: false
            maxThreads:
              description:
              - Maximum number of threads for sequential operations
              type: int
              required: false
              default: 16
            powerOperationTimeout:
              description:
              - Power Operation Timeout (in seconds)
              type: int
              required: false
              default: 30
            connectionRetryInterval:
              description:
              - Connection to CMDaemon retry interval (in seconds)
              type: int
              required: false
              default: 5
            logFile:
              description:
              - Path to cm-scale logs file
              type: str
              required: false
              default: /var/log/cm-scale.log
            pinQueues:
              description:
              - Pin workload to its queue nodes
              type: bool
              required: false
              default: false
            mixLocations:
              description:
              - Allow to map workload to different locations (for example, cloud and local)
              type: bool
              required: false
              default: true
            failedNodeIsHealthy:
              description:
              - Do not start a new node instead of a failed one
              type: bool
              required: false
              default: false
            collectStatistics:
              description:
              - Collect internal Auto Scaler statistics and push to the monitoring
              type: bool
              required: false
              default: false
            azureDiskAccountNodes:
              description:
              - Number of nodes that can share the same Azure disk account
              type: int
              required: false
              default: 20
            azureDiskImageName:
              description:
              - Image name for Azure disks
              type: str
              required: false
              default: images
            azureDiskContainerName:
              description:
              - Container name for Azure disks
              type: str
              required: false
              default: vhds
            azureDiskAccountPrefix:
              description:
              - Prefix for randomly generated Azure disk account names
              type: str
              required: false
            nodeSelection:
              description:
              - Type of node selection used by Auto Scaler
              type: str
              required: false
              default: ABS
              choices:
              - ABS
              - UPTIME
              - RANDOM
            nodeSelectionUptimePeriod:
              description:
              - Period of time in which Auto Scaler calculates total uptime for the nodes
                during selection
              type: int
              required: false
              default: 1209600
            options:
              description:
              - Additional parameters that will be passed to cm-scale daemon
              type: list
              required: false
              default: []
        engines_ScaleKubeEngine:
          description:
          - Submode containing workload engines settings
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - HPC workload engine name
              type: str
              required: true
            workloadsPerNode:
              description:
              - Number of workloads that can be scheduled to the same node at the same
                time
              type: int
              required: false
              default: 1
            priority:
              description:
              - Workload engine priority
              type: int
              required: false
              default: 0
            ageFactor:
              description:
              - Fairsharing coefficient for workload age significance
              type: float
              required: false
              default: 1.0
            engineFactor:
              description:
              - Fairsharing coefficient for engine priority significance
              type: float
              required: false
              default: 1.0
            externalPriorityFactor:
              description:
              - Fairsharing coefficient for external priority significance
              type: float
              required: false
              default: 0.0
            maxNodes:
              description:
              - Allowed running nodes limit
              type: int
              required: false
              default: 32
            notes:
              description:
              - Engine related notes
              type: str
              required: false
            options:
              description:
              - Additional engine related parameters that will be passed to cm-scale daemon
              type: list
              required: false
              default: []
            cluster:
              description:
              - Kubernetes cluster which pods will be tracked
              type: str
              required: false
            cpuBusyThreshold:
              description:
              - CPU load % that defines if node is too busy for new pods
              type: float
              required: false
              default: 0.9
            memoryBusyThreshold:
              description:
              - Memory load % that defines if node is too busy for new pods
              type: float
              required: false
              default: 0.9
            trackers_ScaleHpcQueueTracker:
              description:
              - Workload trackers
              type: list
              required: false
              default: []
              elements: dict
              options:
                name:
                  description:
                  - Tracker name
                  type: str
                  required: true
                enabled:
                  description:
                  - Tracker is currently enabled or disabled
                  type: bool
                  required: false
                  default: true
                assignCategory:
                  description:
                  - Category that should be assigned to managed nodes
                  type: str
                  required: false
                primaryOverlays:
                  description:
                  - Configuration overlays that managed nodes are added to when they are
                    required by workload
                  type: list
                  required: false
                  default: []
                allowedResourceProviders:
                  description:
                  - Only the specified resource providers will be used for a workload
                    of this tracker (if empty than all allowed)
                  type: list
                  required: false
                  default: []
                queueLengthThreshold:
                  description:
                  - Number of pending workloads/jobs that triggers the nodes bursting
                  type: int
                  required: false
                  default: 0
                ageThreshold:
                  description:
                  - Workload/job pending time threshold that triggers the nodes bursting
                    for this workload (in seconds)
                  type: int
                  required: false
                  default: 0
                workloadsPerNode:
                  description:
                  - Number of workloads that can be scheduled to the same node at the
                    same time (0 means no limit)
                  type: int
                  required: false
                  default: 0
                options:
                  description:
                  - Additional tracker related parameters
                  type: list
                  required: false
                  default: []
                queue:
                  description:
                  - Tracking job queue
                  type: str
                  required: false
            trackers_ScaleGenericTracker:
              description:
              - Workload trackers
              type: list
              required: false
              default: []
              elements: dict
              options:
                name:
                  description:
                  - Tracker name
                  type: str
                  required: true
                enabled:
                  description:
                  - Tracker is currently enabled or disabled
                  type: bool
                  required: false
                  default: true
                assignCategory:
                  description:
                  - Category that should be assigned to managed nodes
                  type: str
                  required: false
                primaryOverlays:
                  description:
                  - Configuration overlays that managed nodes are added to when they are
                    required by workload
                  type: list
                  required: false
                  default: []
                allowedResourceProviders:
                  description:
                  - Only the specified resource providers will be used for a workload
                    of this tracker (if empty than all allowed)
                  type: list
                  required: false
                  default: []
                queueLengthThreshold:
                  description:
                  - Number of pending workloads/jobs that triggers the nodes bursting
                  type: int
                  required: false
                  default: 0
                ageThreshold:
                  description:
                  - Workload/job pending time threshold that triggers the nodes bursting
                    for this workload (in seconds)
                  type: int
                  required: false
                  default: 0
                workloadsPerNode:
                  description:
                  - Number of workloads that can be scheduled to the same node at the
                    same time (0 means no limit)
                  type: int
                  required: false
                  default: 0
                options:
                  description:
                  - Additional tracker related parameters
                  type: list
                  required: false
                  default: []
                handler:
                  description:
                  - Full path to python module that produces workload entities for cm-scale
                  type: str
                  required: false
            trackers_ScaleKubeNamespaceTracker:
              description:
              - Workload trackers
              type: list
              required: false
              default: []
              elements: dict
              options:
                name:
                  description:
                  - Tracker name
                  type: str
                  required: true
                enabled:
                  description:
                  - Tracker is currently enabled or disabled
                  type: bool
                  required: false
                  default: true
                assignCategory:
                  description:
                  - Category that should be assigned to managed nodes
                  type: str
                  required: false
                primaryOverlays:
                  description:
                  - Configuration overlays that managed nodes are added to when they are
                    required by workload
                  type: list
                  required: false
                  default: []
                allowedResourceProviders:
                  description:
                  - Only the specified resource providers will be used for a workload
                    of this tracker (if empty than all allowed)
                  type: list
                  required: false
                  default: []
                queueLengthThreshold:
                  description:
                  - Number of pending workloads/jobs that triggers the nodes bursting
                  type: int
                  required: false
                  default: 0
                ageThreshold:
                  description:
                  - Workload/job pending time threshold that triggers the nodes bursting
                    for this workload (in seconds)
                  type: int
                  required: false
                  default: 0
                workloadsPerNode:
                  description:
                  - Number of workloads that can be scheduled to the same node at the
                    same time (0 means no limit)
                  type: int
                  required: false
                  default: 0
                options:
                  description:
                  - Additional tracker related parameters
                  type: list
                  required: false
                  default: []
                controllerNamespace:
                  description:
                  - Tracking Kubernetes namespace name
                  type: str
                  required: false
                object:
                  description:
                  - Type of Kubernetes objects to track
                  type: str
                  required: false
                  default: job
                  choices:
                  - job
                  - pod
        engines_ScaleHpcEngine:
          description:
          - Submode containing workload engines settings
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - HPC workload engine name
              type: str
              required: true
            workloadsPerNode:
              description:
              - Number of workloads that can be scheduled to the same node at the same
                time
              type: int
              required: false
              default: 1
            priority:
              description:
              - Workload engine priority
              type: int
              required: false
              default: 0
            ageFactor:
              description:
              - Fairsharing coefficient for workload age significance
              type: float
              required: false
              default: 1.0
            engineFactor:
              description:
              - Fairsharing coefficient for engine priority significance
              type: float
              required: false
              default: 1.0
            externalPriorityFactor:
              description:
              - Fairsharing coefficient for external priority significance
              type: float
              required: false
              default: 0.0
            maxNodes:
              description:
              - Allowed running nodes limit
              type: int
              required: false
              default: 32
            notes:
              description:
              - Engine related notes
              type: str
              required: false
            options:
              description:
              - Additional engine related parameters that will be passed to cm-scale daemon
              type: list
              required: false
              default: []
            wlmCluster:
              description:
              - WLM cluster that will be used by cm-scale
              type: str
              required: false
            trackers_ScaleHpcQueueTracker:
              description:
              - Workload trackers
              type: list
              required: false
              default: []
              elements: dict
              options:
                name:
                  description:
                  - Tracker name
                  type: str
                  required: true
                enabled:
                  description:
                  - Tracker is currently enabled or disabled
                  type: bool
                  required: false
                  default: true
                assignCategory:
                  description:
                  - Category that should be assigned to managed nodes
                  type: str
                  required: false
                primaryOverlays:
                  description:
                  - Configuration overlays that managed nodes are added to when they are
                    required by workload
                  type: list
                  required: false
                  default: []
                allowedResourceProviders:
                  description:
                  - Only the specified resource providers will be used for a workload
                    of this tracker (if empty than all allowed)
                  type: list
                  required: false
                  default: []
                queueLengthThreshold:
                  description:
                  - Number of pending workloads/jobs that triggers the nodes bursting
                  type: int
                  required: false
                  default: 0
                ageThreshold:
                  description:
                  - Workload/job pending time threshold that triggers the nodes bursting
                    for this workload (in seconds)
                  type: int
                  required: false
                  default: 0
                workloadsPerNode:
                  description:
                  - Number of workloads that can be scheduled to the same node at the
                    same time (0 means no limit)
                  type: int
                  required: false
                  default: 0
                options:
                  description:
                  - Additional tracker related parameters
                  type: list
                  required: false
                  default: []
                queue:
                  description:
                  - Tracking job queue
                  type: str
                  required: false
            trackers_ScaleGenericTracker:
              description:
              - Workload trackers
              type: list
              required: false
              default: []
              elements: dict
              options:
                name:
                  description:
                  - Tracker name
                  type: str
                  required: true
                enabled:
                  description:
                  - Tracker is currently enabled or disabled
                  type: bool
                  required: false
                  default: true
                assignCategory:
                  description:
                  - Category that should be assigned to managed nodes
                  type: str
                  required: false
                primaryOverlays:
                  description:
                  - Configuration overlays that managed nodes are added to when they are
                    required by workload
                  type: list
                  required: false
                  default: []
                allowedResourceProviders:
                  description:
                  - Only the specified resource providers will be used for a workload
                    of this tracker (if empty than all allowed)
                  type: list
                  required: false
                  default: []
                queueLengthThreshold:
                  description:
                  - Number of pending workloads/jobs that triggers the nodes bursting
                  type: int
                  required: false
                  default: 0
                ageThreshold:
                  description:
                  - Workload/job pending time threshold that triggers the nodes bursting
                    for this workload (in seconds)
                  type: int
                  required: false
                  default: 0
                workloadsPerNode:
                  description:
                  - Number of workloads that can be scheduled to the same node at the
                    same time (0 means no limit)
                  type: int
                  required: false
                  default: 0
                options:
                  description:
                  - Additional tracker related parameters
                  type: list
                  required: false
                  default: []
                handler:
                  description:
                  - Full path to python module that produces workload entities for cm-scale
                  type: str
                  required: false
            trackers_ScaleKubeNamespaceTracker:
              description:
              - Workload trackers
              type: list
              required: false
              default: []
              elements: dict
              options:
                name:
                  description:
                  - Tracker name
                  type: str
                  required: true
                enabled:
                  description:
                  - Tracker is currently enabled or disabled
                  type: bool
                  required: false
                  default: true
                assignCategory:
                  description:
                  - Category that should be assigned to managed nodes
                  type: str
                  required: false
                primaryOverlays:
                  description:
                  - Configuration overlays that managed nodes are added to when they are
                    required by workload
                  type: list
                  required: false
                  default: []
                allowedResourceProviders:
                  description:
                  - Only the specified resource providers will be used for a workload
                    of this tracker (if empty than all allowed)
                  type: list
                  required: false
                  default: []
                queueLengthThreshold:
                  description:
                  - Number of pending workloads/jobs that triggers the nodes bursting
                  type: int
                  required: false
                  default: 0
                ageThreshold:
                  description:
                  - Workload/job pending time threshold that triggers the nodes bursting
                    for this workload (in seconds)
                  type: int
                  required: false
                  default: 0
                workloadsPerNode:
                  description:
                  - Number of workloads that can be scheduled to the same node at the
                    same time (0 means no limit)
                  type: int
                  required: false
                  default: 0
                options:
                  description:
                  - Additional tracker related parameters
                  type: list
                  required: false
                  default: []
                controllerNamespace:
                  description:
                  - Tracking Kubernetes namespace name
                  type: str
                  required: false
                object:
                  description:
                  - Type of Kubernetes objects to track
                  type: str
                  required: false
                  default: job
                  choices:
                  - job
                  - pod
        engines_ScaleGenericEngine:
          description:
          - Submode containing workload engines settings
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - HPC workload engine name
              type: str
              required: true
            workloadsPerNode:
              description:
              - Number of workloads that can be scheduled to the same node at the same
                time
              type: int
              required: false
              default: 1
            priority:
              description:
              - Workload engine priority
              type: int
              required: false
              default: 0
            ageFactor:
              description:
              - Fairsharing coefficient for workload age significance
              type: float
              required: false
              default: 1.0
            engineFactor:
              description:
              - Fairsharing coefficient for engine priority significance
              type: float
              required: false
              default: 1.0
            externalPriorityFactor:
              description:
              - Fairsharing coefficient for external priority significance
              type: float
              required: false
              default: 0.0
            maxNodes:
              description:
              - Allowed running nodes limit
              type: int
              required: false
              default: 32
            notes:
              description:
              - Engine related notes
              type: str
              required: false
            options:
              description:
              - Additional engine related parameters that will be passed to cm-scale daemon
              type: list
              required: false
              default: []
            trackers_ScaleHpcQueueTracker:
              description:
              - Workload trackers
              type: list
              required: false
              default: []
              elements: dict
              options:
                name:
                  description:
                  - Tracker name
                  type: str
                  required: true
                enabled:
                  description:
                  - Tracker is currently enabled or disabled
                  type: bool
                  required: false
                  default: true
                assignCategory:
                  description:
                  - Category that should be assigned to managed nodes
                  type: str
                  required: false
                primaryOverlays:
                  description:
                  - Configuration overlays that managed nodes are added to when they are
                    required by workload
                  type: list
                  required: false
                  default: []
                allowedResourceProviders:
                  description:
                  - Only the specified resource providers will be used for a workload
                    of this tracker (if empty than all allowed)
                  type: list
                  required: false
                  default: []
                queueLengthThreshold:
                  description:
                  - Number of pending workloads/jobs that triggers the nodes bursting
                  type: int
                  required: false
                  default: 0
                ageThreshold:
                  description:
                  - Workload/job pending time threshold that triggers the nodes bursting
                    for this workload (in seconds)
                  type: int
                  required: false
                  default: 0
                workloadsPerNode:
                  description:
                  - Number of workloads that can be scheduled to the same node at the
                    same time (0 means no limit)
                  type: int
                  required: false
                  default: 0
                options:
                  description:
                  - Additional tracker related parameters
                  type: list
                  required: false
                  default: []
                queue:
                  description:
                  - Tracking job queue
                  type: str
                  required: false
            trackers_ScaleGenericTracker:
              description:
              - Workload trackers
              type: list
              required: false
              default: []
              elements: dict
              options:
                name:
                  description:
                  - Tracker name
                  type: str
                  required: true
                enabled:
                  description:
                  - Tracker is currently enabled or disabled
                  type: bool
                  required: false
                  default: true
                assignCategory:
                  description:
                  - Category that should be assigned to managed nodes
                  type: str
                  required: false
                primaryOverlays:
                  description:
                  - Configuration overlays that managed nodes are added to when they are
                    required by workload
                  type: list
                  required: false
                  default: []
                allowedResourceProviders:
                  description:
                  - Only the specified resource providers will be used for a workload
                    of this tracker (if empty than all allowed)
                  type: list
                  required: false
                  default: []
                queueLengthThreshold:
                  description:
                  - Number of pending workloads/jobs that triggers the nodes bursting
                  type: int
                  required: false
                  default: 0
                ageThreshold:
                  description:
                  - Workload/job pending time threshold that triggers the nodes bursting
                    for this workload (in seconds)
                  type: int
                  required: false
                  default: 0
                workloadsPerNode:
                  description:
                  - Number of workloads that can be scheduled to the same node at the
                    same time (0 means no limit)
                  type: int
                  required: false
                  default: 0
                options:
                  description:
                  - Additional tracker related parameters
                  type: list
                  required: false
                  default: []
                handler:
                  description:
                  - Full path to python module that produces workload entities for cm-scale
                  type: str
                  required: false
            trackers_ScaleKubeNamespaceTracker:
              description:
              - Workload trackers
              type: list
              required: false
              default: []
              elements: dict
              options:
                name:
                  description:
                  - Tracker name
                  type: str
                  required: true
                enabled:
                  description:
                  - Tracker is currently enabled or disabled
                  type: bool
                  required: false
                  default: true
                assignCategory:
                  description:
                  - Category that should be assigned to managed nodes
                  type: str
                  required: false
                primaryOverlays:
                  description:
                  - Configuration overlays that managed nodes are added to when they are
                    required by workload
                  type: list
                  required: false
                  default: []
                allowedResourceProviders:
                  description:
                  - Only the specified resource providers will be used for a workload
                    of this tracker (if empty than all allowed)
                  type: list
                  required: false
                  default: []
                queueLengthThreshold:
                  description:
                  - Number of pending workloads/jobs that triggers the nodes bursting
                  type: int
                  required: false
                  default: 0
                ageThreshold:
                  description:
                  - Workload/job pending time threshold that triggers the nodes bursting
                    for this workload (in seconds)
                  type: int
                  required: false
                  default: 0
                workloadsPerNode:
                  description:
                  - Number of workloads that can be scheduled to the same node at the
                    same time (0 means no limit)
                  type: int
                  required: false
                  default: 0
                options:
                  description:
                  - Additional tracker related parameters
                  type: list
                  required: false
                  default: []
                controllerNamespace:
                  description:
                  - Tracking Kubernetes namespace name
                  type: str
                  required: false
                object:
                  description:
                  - Type of Kubernetes objects to track
                  type: str
                  required: false
                  default: job
                  choices:
                  - job
                  - pod
        resourceProviders_ScaleDynamicNodesProvider:
          description:
          - List of resource providers
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Resource provider name
              type: str
              required: true
            enabled:
              description:
              - Resource provider is currently enabled
              type: bool
              required: false
              default: true
            priority:
              description:
              - Node provider priority
              type: int
              required: false
              default: 0
            wholeTime:
              description:
              - A compute node running time (in minutes) before it is stopped if no workload
                requires it
              type: int
              required: false
              default: 0
            stoppingAllowancePeriod:
              description:
              - A time (in minutes) just before the end of the wholeTime period prior
                to which all power off (or terminate) operations must be started
              type: int
              required: false
              default: 0
            keepRunning:
              description:
              - Nodes that should not be stopped or terminated even if they are unused
                (range format)
              type: str
              required: false
            extraNodes:
              description:
              - Nodes that should be started before regular nodes
              type: list
              required: false
              default: []
            extraNodeIdleTime:
              description:
              - Time that extra nodes can remain unused (after this time they are stopped)
              type: int
              required: false
              default: 3600
            extraNodeStart:
              description:
              - Automatically start extra node before the first compute node is started
              type: bool
              required: false
              default: true
            extraNodeStop:
              description:
              - Automatically stop extra node after the last compute node stops
              type: bool
              required: false
              default: true
            allocationProlog:
              description:
              - Script that is executed when a node is allocated to a workload
              type: str
              required: false
            allocationEpilog:
              description:
              - Script that is executed when a node is deallocated
              type: str
              required: false
            allocationScriptsTimeout:
              description:
              - Allocation scripts timeout
              type: int
              required: false
              default: 10
            defaultResources:
              description:
              - List of default resources in format [name=value]
              type: list
              required: false
              default: []
            shutdownEnabled:
              description:
              - Shutdown nodes instead of just power off, and wait until a set timeout
                before doing a hard power off
              type: bool
              required: false
              default: true
            shutdownTimeout:
              description:
              - Shutdown timeout before powering off
              type: int
              required: false
              default: 180
            longStartingNodeAction:
              description:
              - Action applied to nodes that start for too long
              type: str
              required: false
              default: NONE
              choices:
              - NONE
              - POWEROFF
              - TERMINATE
            longStartingNodeTimeout:
              description:
              - How long Auto Scaler should wait before the action is applied for long
                starting nodes
              type: int
              required: false
              default: 600
            options:
              description:
              - Additional resource provider related parameters that will be passed to
                cm-scale daemon
              type: list
              required: false
              default: []
            templateNode:
              description:
              - Template node
              type: str
              required: false
            nodeRange:
              description:
              - Node range
              type: str
              required: false
            networkInterface:
              description:
              - Which node network interface will be changed on cloning (incremented)
              type: str
              required: false
            startTemplateNode:
              description:
              - Should template node be started automatically
              type: bool
              required: false
              default: false
            stopTemplateNode:
              description:
              - Should template node be stopped automatically
              type: bool
              required: false
              default: false
            removeNodes:
              description:
              - Should nodes be removed from Bright Cluster Manager configuration upon
                the node termination
              type: bool
              required: false
              default: false
            leaveFailedNodes:
              description:
              - Failed nodes will not be touched in order to allow administrator to investigate
                why they were failed
              type: bool
              required: false
              default: true
            neverTerminate:
              description:
              - Number of nodes that cm-scale powers off and allows to remain, instead
                of terminating
              type: int
              required: false
              default: 32
            neverTerminateNodes:
              description:
              - List of particular nodes that cm-scale powers off and allows to remain,
                instead of terminating
              type: list
              required: false
              default: []
        resourceProviders_ScaleStaticNodesProvider:
          description:
          - List of resource providers
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Resource provider name
              type: str
              required: true
            enabled:
              description:
              - Resource provider is currently enabled
              type: bool
              required: false
              default: true
            priority:
              description:
              - Node provider priority
              type: int
              required: false
              default: 0
            wholeTime:
              description:
              - A compute node running time (in minutes) before it is stopped if no workload
                requires it
              type: int
              required: false
              default: 0
            stoppingAllowancePeriod:
              description:
              - A time (in minutes) just before the end of the wholeTime period prior
                to which all power off (or terminate) operations must be started
              type: int
              required: false
              default: 0
            keepRunning:
              description:
              - Nodes that should not be stopped or terminated even if they are unused
                (range format)
              type: str
              required: false
            extraNodes:
              description:
              - Nodes that should be started before regular nodes
              type: list
              required: false
              default: []
            extraNodeIdleTime:
              description:
              - Time that extra nodes can remain unused (after this time they are stopped)
              type: int
              required: false
              default: 3600
            extraNodeStart:
              description:
              - Automatically start extra node before the first compute node is started
              type: bool
              required: false
              default: true
            extraNodeStop:
              description:
              - Automatically stop extra node after the last compute node stops
              type: bool
              required: false
              default: true
            allocationProlog:
              description:
              - Script that is executed when a node is allocated to a workload
              type: str
              required: false
            allocationEpilog:
              description:
              - Script that is executed when a node is deallocated
              type: str
              required: false
            allocationScriptsTimeout:
              description:
              - Allocation scripts timeout
              type: int
              required: false
              default: 10
            defaultResources:
              description:
              - List of default resources in format [name=value]
              type: list
              required: false
              default: []
            shutdownEnabled:
              description:
              - Shutdown nodes instead of just power off, and wait until a set timeout
                before doing a hard power off
              type: bool
              required: false
              default: true
            shutdownTimeout:
              description:
              - Shutdown timeout before powering off
              type: int
              required: false
              default: 180
            longStartingNodeAction:
              description:
              - Action applied to nodes that start for too long
              type: str
              required: false
              default: NONE
              choices:
              - NONE
              - POWEROFF
              - TERMINATE
            longStartingNodeTimeout:
              description:
              - How long Auto Scaler should wait before the action is applied for long
                starting nodes
              type: int
              required: false
              default: 600
            options:
              description:
              - Additional resource provider related parameters that will be passed to
                cm-scale daemon
              type: list
              required: false
              default: []
            nodes:
              description:
              - List of managed nodes
              type: list
              required: false
              default: []
            nodegroups:
              description:
              - List of managed nodegroups
              type: list
              required: false
              default: []
    roles_SlurmServerRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        wlmCluster:
          description:
          - WLM cluster link to this WLM role
          type: str
          required: false
        externalServer:
          description:
          - Slurm server daemons are running on some external machine
          type: bool
          required: false
          default: false
        slurmctldStartPolicy:
          description:
          - Determines when slurmctld must be running across slurm servernodes
          type: str
          required: false
          default: ALWAYS
          choices:
          - ALWAYS
          - TAKEOVER
          - ACTIVEONLY
    roles_DockerHostRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        spool:
          description:
          - Root of the Docker runtime
          type: str
          required: false
          default: /var/lib/docker
        tmpDir:
          description:
          - Location used for temporary files (token $spool is replaced to path to docker
            runtime root directory)
          type: str
          required: false
          default: $spool/tmp
        enableSelinux:
          description:
          - Enable selinux support in docker daemon
          type: bool
          required: false
          default: true
        defaultUlimits:
          description:
          - Set the default ulimit options to use for all containers
          type: list
          required: false
          default: []
        debug:
          description:
          - Enable debug mode
          type: bool
          required: false
          default: false
        logLevel:
          description:
          - Set the logging level
          type: str
          required: false
          default: info
          choices:
          - ''
          - debug
          - info
          - warn
          - error
          - fatal
        bridgeIp:
          description:
          - Network bridge IP
          type: str
          required: false
        bridge:
          description:
          - Attach containers to a network bridge
          type: str
          required: false
        mtu:
          description:
          - Set the containers network MTU (in bytes)
          type: int
          required: false
          default: 0
        apiSockets:
          description:
          - Daemon socket(s) to connect to (-H docker daemon option)
          type: list
          required: false
          default:
          - unix:///var/run/docker.sock
        iptables:
          description:
          - Enable addition of iptables rules
          type: bool
          required: false
          default: true
        userNamespaceRemap:
          description:
          - User/Group setting for user namespaces
          type: str
          required: false
        insecureRegistries:
          description:
          - 'If you have a registry secured with https but do not have proper certs distributed,
            you can tell docker to not look for full authorization by adding the registry
            to this list. Accepted Format : CIDR or hostname:port'
          type: list
          required: false
          default: []
        enableTls:
          description:
          - Use TLS
          type: bool
          required: false
          default: false
        verifyTls:
          description:
          - Use TLS and verify the remote
          type: bool
          required: false
          default: false
        tlsCa:
          description:
          - Trust certs signed only by this CA
          type: str
          required: false
        tlsCertificate:
          description:
          - Path to TLS certificate file
          type: str
          required: false
        tlsKey:
          description:
          - Path to TLS key file
          type: str
          required: false
        certificatesPath:
          description:
          - Path to docker certificates
          type: str
          required: false
          default: /etc/docker
        containerdSocket:
          description:
          - Path to containerd socket
          type: str
          required: false
        runtime:
          description:
          - Docker runtime
          type: str
          required: false
          default: runc
        options:
          description:
          - Additional parameters for docker daemon
          type: list
          required: false
          default: []
        storageBackends_DockerStorageOverlay2Backend:
          description:
          - Docker storage backends
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Docker storage backend name
              type: str
              required: true
            overrideKernelCheck:
              description:
              - Override the kernel check to allow overlay2
              type: bool
              required: false
              default: false
            size:
              description:
              - Default max size of the container (empty = unlimited)
              type: str
              required: false
            options:
              description:
              - Extra options used for the Overlay2 storage backend
              type: list
              required: false
              default: []
    roles_KubernetesApiServerProxyRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        workerConnections:
          description:
          - Number of worker connections
          type: int
          required: false
          default: 1024
        sendFile:
          description:
          - Allow files to be sent
          type: bool
          required: false
          default: true
        tcpNoPush:
          description: []
          type: bool
          required: false
          default: true
        tcpNoDelay:
          description:
          - TCP no delay
          type: bool
          required: false
          default: true
        keepAliveTimeout:
          description:
          - Keep alive timeout
          type: int
          required: false
          default: 65
        typesHashMaxSize:
          description:
          - Types hash max size
          type: int
          required: false
          default: 2048
        kubeClusters:
          description:
          - The Kubernetes cluster instances (pointers)
          type: list
          required: false
          default: []
    roles_FSPartRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        fsparts:
          description:
          - FSParts
          type: list
          required: false
          default: []
        fspartSource:
          description:
          - Server as source for all these FSParts
          type: bool
          required: false
          default: true
    roles_KubernetesIngressServerProxyRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        workerConnections:
          description:
          - Number of worker connections
          type: int
          required: false
          default: 1024
        sendFile:
          description:
          - Allow files to be sent
          type: bool
          required: false
          default: true
        tcpNoPush:
          description: []
          type: bool
          required: false
          default: true
        tcpNoDelay:
          description:
          - TCP no delay
          type: bool
          required: false
          default: true
        keepAliveTimeout:
          description:
          - Keep alive timeout
          type: int
          required: false
          default: 65
        typesHashMaxSize:
          description:
          - Types hash max size
          type: int
          required: false
          default: 2048
        listenPort:
          description:
          - TCP port listening for incoming connections
          type: int
          required: false
          default: 443
        ingressPort:
          description:
          - Specify manually the Ingress controller port. (Use 0 to disable)
          type: int
          required: false
          default: 0
        kubeClusters:
          description:
          - The Kubernetes cluster instances (pointers)
          type: list
          required: false
          default: []
    roles_HeadNodeRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        failoverId:
          description: []
          type: int
          required: false
          default: 0
        disableAutomaticExports:
          description:
          - Disable creation of automatic filesystem exports
          type: bool
          required: false
          default: false
    roles_SubnetManagerRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        interconnect:
          description:
          - Type of interconnect
          type: str
          required: false
          default: IB
          choices:
          - IB
          - OMNI
        ibl2mtu:
          description:
          - IB L2 MTU Value
          type: str
          required: false
          default: MTU_L2_2K
          choices:
          - MTU_L2_2K
          - MTU_L2_4K
    roles_PRSClientRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        staticPowerUsage:
          description:
          - Static power usage
          type: int
          required: false
          default: 0
        staticPowerUsageDown:
          description:
          - Static power usage
          type: int
          required: false
          default: 0
        minPowerLimitCPU:
          description:
          - Overwrite the hardware min power limit for the CPUs
          type: int
          required: false
          default: 0
        maxPowerLimitCPU:
          description:
          - Overwrite the hardware max power limit for the CPUs
          type: int
          required: false
          default: 0
        minPowerLimitGPU:
          description:
          - Overwrite the hardware min power limit for the GPUs
          type: int
          required: false
          default: 0
        maxPowerLimitGPU:
          description:
          - Overwrite the hardware max power limit for the GPUs
          type: int
          required: false
          default: 0
    roles_LdapServerRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        nodegroups:
          description:
          - List of node groups which can boot from this node
          type: list
          required: false
          default: []
        categories:
          description:
          - List of categories which can boot from this node
          type: list
          required: false
          default: []
        racks:
          description:
          - List of racks which can boot from this node
          type: list
          required: false
          default: []
    roles_FirewallRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        shorewall:
          description:
          - Manage shorewall
          type: bool
          required: false
          default: false
        openPorts:
          description:
          - The list of ports that will be opened on the node's firewall
          type: list
          required: false
          default: []
          elements: dict
          options:
            action:
              description:
              - Specifies the action to be taken if the connection request matches the
                rule
              type: str
              required: false
              default: ACCEPT
              choices:
              - ACCEPT
              - DNAT
              - DROP
              - REJECT
            network:
              description:
              - Network
              type: str
              required: false
              default: net
            port:
              description:
              - Port
              type: int
              required: false
              default: 0
            count:
              description:
              - Number of ports starting from port
              type: int
              required: false
              default: 1
            protocol:
              description:
              - Protocol, any implies TCP and UDP
              type: str
              required: false
              default: Any
              choices:
              - Any
              - TCP
              - UDP
              - ICMP
            address:
              description:
              - Network Address
              type: str
              required: false
              default: 0.0.0.0/0
            destination:
              description:
              - Destination hosts to which the rule applies
              type: str
              required: false
              default: fw
            description:
              description:
              - Description
              type: str
              required: false
        zones:
          description:
          - The list of extra zones that will be defined in the node's firewall
          type: list
          required: false
          default: []
          elements: dict
          options:
            zone:
              description:
              - Zone
              type: str
              required: false
              default: loc
            zone_type:
              description:
              - Type
              type: str
              required: false
              default: ipv4
              choices:
              - ipv4
              - ipv6
            options:
              description:
              - Options
              type: str
              required: false
        interfaces:
          description:
          - The list of extra interfaces that will be defined in the node's firewall
          type: list
          required: false
          default: []
          elements: dict
          options:
            zone:
              description:
              - Zone
              type: str
              required: false
              default: loc
            interface:
              description:
              - Interface
              type: str
              required: false
              default: eth1
            broadcast:
              description:
              - Broadcast
              type: str
              required: false
            options:
              description:
              - Options
              type: str
              required: false
        policies:
          description:
          - The list of extra policies that will be defined in the node's firewall
          type: list
          required: false
          default: []
          elements: dict
          options:
            source:
              description:
              - Source
              type: str
              required: false
              default: loc
            dest:
              description:
              - Dest
              type: str
              required: false
              default: net
            policy:
              description:
              - Policy
              type: str
              required: false
              default: ACCEPT
              choices:
              - ACCEPT
              - BLACKLIST
              - CONTINUE
              - DROP
              - NFQUEUE
              - NONE
              - QUEUE
              - REJECT
            log:
              description:
              - Log
              type: str
              required: false
            options:
              description:
              - Options
              type: str
              required: false
            extra_values:
              description: []
              type: json
              required: false
        routes:
          description:
          - The list of extra routes that will be defined in the node's firewall
          type: list
          required: false
          default: []
          elements: dict
          options:
            provider:
              description:
              - Provider
              type: str
              required: false
            destination:
              description:
              - Destination
              type: str
              required: false
            gateway:
              description:
              - Gateway
              type: str
              required: false
            device:
              description:
              - Device
              type: str
              required: false
            options:
              description:
              - Options
              type: str
              required: false
    roles_DIGITSRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        version:
          description:
          - DIGITS version
          type: str
          required: false
        port:
          description:
          - DIGITS port
          type: int
          required: false
          default: 5000
        jobsDir:
          description:
          - Location where job files are stored. Defined in DIGITS_JOBS_DIR
          type: str
          required: false
          default: $DIGITS_ROOT/digits/jobs
        logfileFilename:
          description:
          - File for saving log messages. Defined in DIGITS_LOGFILE_FILENAME
          type: str
          required: false
          default: $DIGITS_ROOT/digits/digits.log
        logfileLevel:
          description:
          - Minimum log message level to be saved (DEBUG/INFO/WARNING/ERROR/CRITICAL).
            Defined in DIGITS_LOGFILE_LEVEL
          type: str
          required: false
          default: INFO
          choices:
          - DEBUG
          - INFO
          - WARNING
          - ERROR
          - CRITICAL
        serverName:
          description:
          - The name of the server (accessible in the UI under 'Info'). Default is the
            system hostname. Defined in DIGITS_SERVER_NAME
          type: str
          required: false
          default: $hostname
        modelStoreUrl:
          description:
          - A list of URL's, separated by comma. Default is the official NVIDIA store.
            Defined in DIGITS_MODEL_STORE_URL
          type: str
          required: false
        urlPrefix:
          description:
          - A path to prepend before every URL. Sets the home-page to be at 'http://localhost/custom-prefix'
            instead of 'http://localhost/'. Defined in DIGITS_URL_PREFIX
          type: str
          required: false
        caffeRoot:
          description:
          - Path to your local Caffe build. Should contain build/tools/caffe and python/caffe/.
            Defined in CAFFE_ROOT
          type: str
          required: false
        torchRoot:
          description:
          - Path to your local Torch build. Should contain install/bin/th. Defined in
            TORCH_ROOT
          type: str
          required: false
        tensorflowRoot:
          description:
          - Path to your local TensorFlow build. Defined in TENSORFLOW_ROOT
          type: str
          required: false
    roles_NginxRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        workerConnections:
          description:
          - Number of worker connections
          type: int
          required: false
          default: 1024
        sendFile:
          description:
          - Allow files to be sent
          type: bool
          required: false
          default: true
        tcpNoPush:
          description: []
          type: bool
          required: false
          default: true
        tcpNoDelay:
          description:
          - TCP no delay
          type: bool
          required: false
          default: true
        keepAliveTimeout:
          description:
          - Keep alive timeout
          type: int
          required: false
          default: 65
        typesHashMaxSize:
          description:
          - Types hash max size
          type: int
          required: false
          default: 2048
        nginxReverseProxy:
          description:
          - Nginx Reverse Proxy Configuration
          type: list
          required: false
          default: []
          elements: dict
          options:
            port:
              description:
              - Port
              type: int
              required: false
              default: 0
            address:
              description:
              - Destination Network Address
              type: str
              required: false
              default: 0.0.0.0
            node:
              description:
              - Destination hostname(only for nodes)
              type: str
              required: false
            destport:
              description:
              - Port
              type: int
              required: false
              default: 0
            description:
              description:
              - Description
              type: str
              required: false
    roles_CapiRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        labels:
          description:
          - labels to attach to the ByoHost CR in the form labelname=labelVal for e.g.
            '--label site=apac --label cores=2'
          type: list
          required: false
          default: []
        metricsBindAddress:
          description:
          - metricsbindaddress is the TCP address that the controller should bind to for
            serving prometheus metrics. It can be set to '0' to disable the metrics serving
            (default ':8888')
          type: str
          required: false
          default: :8888
        level:
          description:
          - Number for the log level verbosity
          type: int
          required: false
          default: 0
        options:
          description:
          - Additional parameters for byoh host agent
          type: list
          required: false
          default: []
        kubeCluster:
          description:
          - The Kubernetes cluster instance (pointer)
          type: str
          required: false
    roles_BeeGFSClientRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        configurations:
          description:
          - List of BeeGFS client configurations
          type: list
          required: false
          default: []
          elements: dict
          options:
            ref_beegfs_cluster_uuid:
              description:
              - BeeGFS cluster
              - (Field should be formatted as a UUID)
              type: str
              required: true
              default: None
            enableQuota:
              description:
              - Enable quota
              type: bool
              required: false
              default: false
            createHardlinksAsSymlinks:
              description:
              - Create a symlink when an application tries to create a hardlink
              type: bool
              required: false
              default: false
            mountSanityCheck:
              description:
              - Time in ms server has to respond after mount sanity check
              type: float
              required: false
              default: 11.0
            sessionCheckOnClose:
              description:
              - Check for valid sessions on storage server when a file is closed
              type: bool
              required: false
              default: false
            syncOnClose:
              description:
              - Sync file content on close
              type: bool
              required: false
              default: false
            targetOfflineTimeout:
              description:
              - Timeout until all storage targets are considered offlinewhen no target
                state updates can be fetched from management server
              type: int
              required: false
              default: 900
            updateTargetStatesTime:
              description:
              - Interval for storage targets states check
              type: float
              required: false
              default: 60
            enableXAttrs:
              description:
              - Enable xattrs
              type: bool
              required: false
              default: false
            enableACLs:
              description:
              - Enable ACLs
              type: bool
              required: false
              default: false
            fileCacheType:
              description:
              - File read/write cache type
              type: str
              required: false
              default: buffered
            preferredMetaFile:
              description:
              - Path to a file with preffered metadata servers
              type: str
              required: false
            preferredStorageFile:
              description:
              - Path to a file with preffered storage targets
              type: str
              required: false
            preferredMetadataServers:
              description:
              - Preferred metadata server IDs
              type: list
              required: false
              default: []
            preferredStorageServers:
              description:
              - Preferred metadata server IDs
              type: list
              required: false
              default: []
            remoteFSync:
              description:
              - Should fsync be executed on server to flush cached file
              type: bool
              required: false
              default: true
            useGlobalAppendLocks:
              description:
              - Should files, opened in append mode, be protected by locks on local machine
                (YES) or on servers (NO)
              type: bool
              required: false
              default: false
            useGlobalFileLocks:
              description:
              - Should advisory locks be checked on local machine (YES) or on servers
                (NO)
              type: bool
              required: false
              default: false
            connectionSettings:
              description:
              - Submode containing BeeGFS client connection settings
              type: dict
              required: false
              options:
                portUDP:
                  description:
                  - UDP port for the client daemon
                  type: int
                  required: false
                  default: 8004
                maxInternodeNumber:
                  description:
                  - Max number of simultaneous connections to the same node
                  type: int
                  required: false
                  default: 12
                communicationRetry:
                  description:
                  - Time for retries in case of a network failure
                  type: int
                  required: false
                  default: 600
                fallbackExpiration:
                  description:
                  - Time after which a connection to a fallback interface expires
                  type: int
                  required: false
                  default: 900
                interfacesFile:
                  description:
                  - Path to the file with a list of interfaces for communication
                  type: str
                  required: false
                interfacesList:
                  description:
                  - List of interfaces for communication
                  type: list
                  required: false
                  default: []
                maxConcurrentAttempts:
                  description:
                  - This may help in case  establishing new connections keeps failing
                    and produces fallbacks
                  type: int
                  required: false
                  default: 0
                netFilterFile:
                  description:
                  - Path to a file with a list of allowed IP subnets
                  type: str
                  required: false
                tcpOnlyFilterFile:
                  description:
                  - Path to a file with a list of no-RDMA IP ranges
                  type: str
                  required: false
                useRDMA:
                  description:
                  - Use RDMA
                  type: bool
                  required: false
                  default: true
                rdmaBuffersNumber:
                  description:
                  - Number of RDMA buffers
                  type: int
                  required: false
                  default: 70
                rdmaBufferSize:
                  description:
                  - Maximum size of a buffer that will be sent over the network
                  type: int
                  required: false
                  default: 8192
                rdmaTypeOfService:
                  description:
                  - RDMA type of service
                  type: int
                  required: false
                  default: 0
                unmountRetries:
                  description:
                  - If communication error occurs during unmount, the unsuccessful communications
                    will be retried normally.
                  type: bool
                  required: false
                  default: true
            logType:
              description:
              - Send log messages to the helper daemon or syslog to send them to the system
                logger
              type: str
              required: false
              default: SYSLOG
              choices:
              - SYSLOG
              - HELPERD
            level:
              description:
              - Log level
              type: int
              required: false
              default: 3
            addClientId:
              description:
              - Defines whether the ClientID should appear in each log line
              type: bool
              required: false
              default: false
            helperIp:
              description:
              - Defines the IP address of the node on which the beegfs-helperd runs for
                remote logging
              type: str
              required: false
              default: 0.0.0.0
    roles_DnsRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        nodegroups:
          description:
          - List of node groups which can boot from this node
          type: list
          required: false
          default: []
        categories:
          description:
          - List of categories which can boot from this node
          type: list
          required: false
          default: []
        racks:
          description:
          - List of racks which can boot from this node
          type: list
          required: false
          default: []
        allowQuery:
          description:
          - List of additional free hosts to allow queries from
          type: list
          required: false
          default: []
        options:
          description:
          - List of additional key=value pairs to add to the options
          type: list
          required: false
          default: []
        maxCacheSize:
          description:
          - Maximum cache size
          type: int
          required: false
          default: 0
        cleaningInterval:
          description:
          - Cleaning cache interval
          type: int
          required: false
          default: 0
        maxCacheTTL:
          description:
          - Maximal cache TTL
          type: int
          required: false
          default: 0
        maxNegativeCacheTTL:
          description:
          - Maximal cache negative response TTL
          type: int
          required: false
          default: 0
    roles_MQTTRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        caPath:
          description:
          - CA certificate path
          type: str
          required: false
          default: /cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages/pythoncm/etc/cacert.pem
        privateKeyPath:
          description:
          - Certificate path
          type: str
          required: false
          default: /cm/local/apps/cmd/cm-mqtt/etc/mqtt.key
        certificatePath:
          description:
          - Private key path
          type: str
          required: false
          default: /cm/local/apps/cmd/cm-mqtt/etc/mqtt.pem
        writeNamedPipePath:
          description:
          - Named pipe to which cmd writes data back to MQTT servers
          type: str
          required: false
          default: /var/spool/cmd/mqtt.pipe
        servers:
          description:
          - Servers
          type: list
          required: false
          default: []
          elements: dict
          options:
            server:
              description:
              - Server
              type: str
              required: true
            port:
              description:
              - Port
              type: int
              required: false
              default: 1883
            topic:
              description:
              - Server
              type: str
              required: false
              default: BCM/#
            disabled:
              description:
              - Disabled
              type: bool
              required: false
              default: false
            username:
              description:
              - Username
              type: str
              required: false
            password:
              description:
              - Password
              type: str
              required: false
            transport:
              description:
              - Transport
              type: str
              required: false
              default: TCP
              choices:
              - TCP
              - WEBSOCKETS
            protocol:
              description:
              - Protocol
              type: str
              required: false
              default: V311
              choices:
              - V311
              - V5
            certRequired:
              description:
              - Server certificate required
              type: bool
              required: false
              default: true
            checkHostname:
              description:
              - Check hostname
              type: bool
              required: false
              default: true
            cacert:
              description:
              - The CA certificate of the server
              type: str
              required: false
            certificate:
              description:
              - The certificate used to connect to the server
              type: str
              required: false
            privateKey:
              description:
              - The certificate private key used to connect to the server
              type: str
              required: false
    roles_ProvisioningRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        maxProvisioningNodes:
          description:
          - Maximum number of nodes that can be provisioned in parallel
          type: int
          required: false
          default: 10
        loadWeight:
          description:
          - Load weight factor, higher factor will reduce the virtual load on the node
            and make it be used less. Value will be set to 1 if defined lower as lower
            than 1.
          type: float
          required: false
          default: 0
        localImages:
          description:
          - List of software images provided from local disk
          type: list
          required: false
          default: []
        includeRevisionsOfLocalImages:
          description:
          - Include revisions of local images
          type: bool
          required: false
          default: true
        sharedImages:
          description:
          - List of software images provided from shared storage
          type: list
          required: false
          default: []
        allImages:
          description:
          - When set, the role will provide all available images. (The images property
            will then be ignored.)
          type: str
          required: false
          default: NOTALLIMAGES
          choices:
          - LOCALDISK
          - SHAREDSTORAGE
          - NOTALLIMAGES
          - LOCALUNLESSSHARED
        nodegroups:
          description:
          - List of node groups for which to provide images
          type: list
          required: false
          default: []
        categories:
          description:
          - List of categories for which to provide images
          type: list
          required: false
          default: []
        racks:
          description:
          - List of racks for which to provide images
          type: list
          required: false
          default: []
        localProvisioning:
          description:
          - Speeds up initial provisioning of cloud directors and cloud provisioning nodes.
            When enabled, if a software image is used as the rootfs of the provisioning
            node and is also to be used by that node to provision other cloud nodes, during
            the initial FULL install that image will be transferred only once to the provisioning
            node, instead of twice.
          type: bool
          required: false
          default: true
    roles_BeeGFSHelperRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        configurations:
          description:
          - List of BeeGFS helper configurations
          type: list
          required: false
          default: []
          elements: dict
          options:
            ref_beegfs_cluster_uuid:
              description:
              - BeeGFS cluster
              - (Field should be formatted as a UUID)
              type: str
              required: true
              default: None
            runDaemonized:
              description:
              - Run the helper as a daemon
              type: bool
              required: false
              default: true
            workersNumber:
              description:
              - Number of worker threads for helper service
              type: int
              required: false
              default: 2
            connectionSettings:
              description:
              - Submode containing BeeGFS helper connection settings
              type: dict
              required: false
              options:
                portTCP:
                  description:
                  - TCP port for the service
                  type: int
                  required: false
                  default: 8006
            logSettings:
              description:
              - Submode containing BeeGFS logging settings
              type: dict
              required: false
              options:
                logType:
                  description:
                  - Defines the logger type. This can either be 'syslog' to send log messages
                    to the general system logger or 'logfile'
                  type: str
                  required: false
                  default: SYSLOG
                  choices:
                  - SYSLOG
                  - LOGFILE
                level:
                  description:
                  - Log level
                  type: int
                  required: false
                  default: 2
                noDate:
                  description:
                  - Do not show date along with time in log
                  type: bool
                  required: false
                  default: false
                numberOfLines:
                  description:
                  - Number of lines in log file, after which it will be rotated
                  type: int
                  required: false
                  default: 50000
                numberOfRotatedFiles:
                  description:
                  - Number of old log files to keep
                  type: int
                  required: false
                  default: 5
                file:
                  description:
                  - Path to the log file, empty means logs go to the journal
                  type: str
                  required: false
    roles_MonitoringRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        numberOfBackups:
          description:
          - Minimum number of backups of the monitoring data
          type: int
          required: false
          default: 2
        backupRing:
          description:
          - Only backup to nodes within the same ring
          type: int
          required: false
          default: 0
        maximumNumberOfNodes:
          description:
          - Maximum number of nodes the monitoring can handle, set to 0 for no limit
          type: int
          required: false
          default: 16384
        delayAfterUp:
          description:
          - Delay after node becomes up before it can take over from other nodes
          type: int
          required: false
          default: 60
        delayAfterDown:
          description:
          - Delay after node goes down before the workload will be offloaded to other
            nodes
          type: int
          required: false
          default: 600
        backupOnShutdown:
          description:
          - Take a backup when the node is shutdown via RPC
          type: bool
          required: false
          default: false
        backupOnReboot:
          description:
          - Take a backup when the node is reboot via RPC
          type: bool
          required: false
          default: false
        backupOnPowerOff:
          description:
          - Take a backup when the node is power off via RPC
          type: bool
          required: false
          default: false
        backupOnPowerReset:
          description:
          - Take a backup when the node is powered reset via RPC
          type: bool
          required: false
          default: false
        backupOnTerminate:
          description:
          - Take a backup when the cloud node is terminated via RPC
          type: bool
          required: false
          default: false
        nodeFilters_MonitoringResourceExecutionFilter:
          description:
          - Filter nodes that can be monitored by this node, clear this list for automatic
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            filterOperation:
              description:
              - The filter operation to be performed
              type: str
              required: false
              default: INCLUDE
              choices:
              - NONE
              - INCLUDE
              - EXCLUDE
            resources:
              description:
              - Resources
              type: list
              required: false
              default: []
            op:
              description:
              - Operator
              type: str
              required: false
              default: OR
              choices:
              - OR
              - AND
        nodeFilters_MonitoringOverlayListExecutionFilter:
          description:
          - Filter nodes that can be monitored by this node, clear this list for automatic
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            filterOperation:
              description:
              - The filter operation to be performed
              type: str
              required: false
              default: INCLUDE
              choices:
              - NONE
              - INCLUDE
              - EXCLUDE
            overlays:
              description:
              - List of overlays belonging to this group
              type: list
              required: false
              default: []
        nodeFilters_MonitoringTypeExecutionFilter:
          description:
          - Filter nodes that can be monitored by this node, clear this list for automatic
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            filterOperation:
              description:
              - The filter operation to be performed
              type: str
              required: false
              default: INCLUDE
              choices:
              - NONE
              - INCLUDE
              - EXCLUDE
            headNode:
              description:
              - Head node
              type: bool
              required: false
              default: false
            physicalNode:
              description:
              - Physical node
              type: bool
              required: false
              default: false
            cloudNode:
              description:
              - Cloud node
              type: bool
              required: false
              default: false
            liteNode:
              description:
              - Lite node
              type: bool
              required: false
              default: false
            dpuNode:
              description:
              - DPU node
              type: bool
              required: false
              default: false
        nodeFilters_MonitoringNodeListExecutionFilter:
          description:
          - Filter nodes that can be monitored by this node, clear this list for automatic
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            filterOperation:
              description:
              - The filter operation to be performed
              type: str
              required: false
              default: INCLUDE
              choices:
              - NONE
              - INCLUDE
              - EXCLUDE
            nodes:
              description:
              - List of nodes belonging to this group
              type: list
              required: false
              default: []
        nodeFilters_MonitoringLuaExecutionFilter:
          description:
          - Filter nodes that can be monitored by this node, clear this list for automatic
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            filterOperation:
              description:
              - The filter operation to be performed
              type: str
              required: false
              default: INCLUDE
              choices:
              - NONE
              - INCLUDE
              - EXCLUDE
            code:
              description:
              - Lua code
              type: str
              required: false
            notes:
              description:
              - Notes
              type: str
              required: false
        nodeFilters_MonitoringCategoryListExecutionFilter:
          description:
          - Filter nodes that can be monitored by this node, clear this list for automatic
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            filterOperation:
              description:
              - The filter operation to be performed
              type: str
              required: false
              default: INCLUDE
              choices:
              - NONE
              - INCLUDE
              - EXCLUDE
            categories:
              description:
              - List of categories belonging to this group
              type: list
              required: false
              default: []
    roles_SlurmAccountingRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        ha:
          description:
          - Generate a high availability configuration
          type: bool
          required: false
          default: false
        primary:
          description:
          - Primary server where slurmdbd will run
          type: str
          required: false
        dbdPort:
          description:
          - The port number that the Slurm Database Daemon (slurmdbd) listens to for work
          type: int
          required: false
          default: 6819
        storageHost:
          description:
          - Defines the name of the host the MySQL database is running where slurmdbd
            is going to store the data
          type: str
          required: false
          default: master
        storagePort:
          description:
          - The port number that the Slurm Database Daemon (slurmdbd) communicates with
            the database
          type: int
          required: false
          default: 3306
        storageLoc:
          description:
          - The name of the database as the location where slurmdbd accounting records
            are written
          type: str
          required: false
          default: slurm_acct_db
        storageUser:
          description:
          - Defines the name of the user to connect to the MySQL database with to store
            the job accounting data
          type: str
          required: false
          default: slurm
        slurmWlmClusters:
          description:
          - List of Slurm clusters which can make use of this SlurmAccountingRole (slurmdbd)
          type: list
          required: false
          default: []
    roles_BeeGFSStorageRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        configurations:
          description:
          - List of BeeGFS storage configurations
          type: list
          required: false
          default: []
          elements: dict
          options:
            ref_beegfs_cluster_uuid:
              description:
              - BeeGFS cluster
              - (Field should be formatted as a UUID)
              type: str
              required: true
              default: None
            dataDirs:
              description:
              - Path to the data directories
              type: list
              required: false
              default:
              - /var/lib/beegfs/storage
            targetOfflineTimeout:
              description:
              - Timeout until targets on a storage server are considered offline when
                no target status is received
              type: int
              required: false
              default: 180
            useAggressiveStreamPoll:
              description:
              - Actively poll for events instead of sleeping until an event occur
              type: bool
              required: false
              default: false
            usePerTargetWorkers:
              description:
              - Create a separate set of workers and attach it for each storage target
              type: bool
              required: false
              default: true
            usePerUserMsgQueues:
              description:
              - Use per-user queues for pending requests
              type: bool
              required: false
              default: false
            runDaemonized:
              description:
              - Run the storage service as a daemon
              type: bool
              required: false
              default: true
            bindToNumaZone:
              description:
              - Zero-based NUMA zone number to which all threads of metadata process should
                be bound
              type: str
              required: false
            resyncSafetyThreshold:
              description:
              - Add an extra amount of time to the last successful communication timestamp,
                in case of a potential cache loss
              type: int
              required: false
              default: 600
            fileReadAheadSize:
              description:
              - Byte range submitted to the kernel for read-ahead after number of bytes
                was already read from target
              type: int
              required: false
              default: 0
            fileReadAheadTriggerSize:
              description:
              - Number of bytes after reading which the read-ahead is triggered
              type: int
              required: false
              default: 4000000
            fileReadSize:
              description:
              - Maximum amount of data server should read in a single operation
              type: int
              required: false
              default: 128000000
            fileWriteSize:
              description:
              - Maximum amount of data server should write in a single operation
              type: int
              required: false
              default: 128000000
            fileWriteSyncSize:
              description:
              - Number of bytes after which kernel will be advised to commit data
              type: int
              required: false
              default: 128000000
            workerBufferSize:
              description:
              - Size of network and io buffers, allocated for each worker
              type: int
              required: false
              default: 4000000
            numberOfResyncGatherSlaves:
              description:
              - Number of threads to gather filesystem information for a buddy mirror
                resync
              type: int
              required: false
              default: 6
            numberOfResyncSlaves:
              description:
              - Number of threads to sync filesystem information for a buddy mirror resync
              type: int
              required: false
              default: 12
            numberOfStreamListeners:
              description:
              - Number of threads waiting for incoming data events
              type: int
              required: false
              default: 1
            numberOfWorkers:
              description:
              - Number of worker threads
              type: int
              required: false
              default: 12
            startByCMDaemon:
              description:
              - Start service by CMDaemon or manually
              type: bool
              required: false
              default: true
            connectionSettings:
              description:
              - Submode containing BeeGFS storage connection settings
              type: dict
              required: false
              options:
                portTCP:
                  description:
                  - TCP port for the service
                  type: int
                  required: false
                  default: 8003
                portUDP:
                  description:
                  - UDP port for the service
                  type: int
                  required: false
                  default: 8003
                backlogTCP:
                  description:
                  - TCP listen backlog
                  type: int
                  required: false
                  default: 128
                maxInternodeNumber:
                  description:
                  - Max number of simultaneous connections to the same node
                  type: int
                  required: false
                  default: 12
                interfacesFile:
                  description:
                  - Path to the file with a list of interfaces for communication
                  type: str
                  required: false
                interfacesList:
                  description:
                  - List of interfaces for communication
                  type: list
                  required: false
                  default: []
                netFilterFile:
                  description:
                  - Path to a file with a list of allowed IP subnets
                  type: str
                  required: false
                tcpOnlyFilterFile:
                  description:
                  - Path to a file with a list of no-RDMA IP ranges
                  type: str
                  required: false
                useRDMA:
                  description:
                  - Use RDMA
                  type: bool
                  required: false
                  default: true
                rdmaTypeOfService:
                  description:
                  - RDMA type of service
                  type: int
                  required: false
                  default: 0
            logSettings:
              description:
              - Submode containing BeeGFS logging settings
              type: dict
              required: false
              options:
                logType:
                  description:
                  - Defines the logger type. This can either be 'syslog' to send log messages
                    to the general system logger or 'logfile'
                  type: str
                  required: false
                  default: SYSLOG
                  choices:
                  - SYSLOG
                  - LOGFILE
                level:
                  description:
                  - Log level
                  type: int
                  required: false
                  default: 2
                noDate:
                  description:
                  - Do not show date along with time in log
                  type: bool
                  required: false
                  default: false
                numberOfLines:
                  description:
                  - Number of lines in log file, after which it will be rotated
                  type: int
                  required: false
                  default: 50000
                numberOfRotatedFiles:
                  description:
                  - Number of old log files to keep
                  type: int
                  required: false
                  default: 5
                file:
                  description:
                  - Path to the log file, empty means logs go to the journal
                  type: str
                  required: false
    roles_CloudDirectorRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        syncFSParts:
          description:
          - Sync FSParts mode
          type: str
          required: false
          default: AUTO
          choices:
          - AUTO
          - ALL
          - CUSTOM
        fsparts:
          description:
          - FSParts
          type: list
          required: false
          default: []
        disableAutomaticExports:
          description:
          - Disable creation of automatic filesystem exports
          type: bool
          required: false
          default: false
        createHomeDirectories:
          description:
          - Create home directories for ldap users
          type: str
          required: false
          default: NEVER
          choices:
          - NEVER
          - ALWAYS
          - WHITELIST
        whitelistUsers:
          description:
          - Whitelist users
          type: list
          required: false
          default: []
        whitelistGroups:
          description:
          - Whitelist groups
          type: list
          required: false
          default: []
        bootImageFromProvisioningRole:
          description:
          - Only allow nodes to boot from images defined in the provisioning role
          type: bool
          required: false
          default: true
    roles_EdgeDirectorRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        syncFSParts:
          description:
          - Sync FSParts mode
          type: str
          required: false
          default: AUTO
          choices:
          - AUTO
          - ALL
          - CUSTOM
        fsparts:
          description:
          - FSParts
          type: list
          required: false
          default: []
        disableAutomaticExports:
          description:
          - Disable creation of automatic filesystem exports
          type: bool
          required: false
          default: false
        createHomeDirectories:
          description:
          - Create home directories for ldap users
          type: str
          required: false
          default: NEVER
          choices:
          - NEVER
          - ALWAYS
          - WHITELIST
        whitelistUsers:
          description:
          - Whitelist users
          type: list
          required: false
          default: []
        whitelistGroups:
          description:
          - Whitelist groups
          type: list
          required: false
          default: []
        nodePowerOperations:
          description:
          - Execute all power operations of nodes in the edge site on the director
          type: bool
          required: false
          default: true
        directorPowerOperations:
          description:
          - Execute all power operation of the director on the director, note that this
            means it cannot be powered on
          type: bool
          required: false
          default: false
        nodeSelectionBootRole:
          description:
          - Use the edge site as a node selection mechanism for the boot role
          type: bool
          required: false
          default: false
        nodeSelectionDnsRole:
          description:
          - Use the edge site as a node selection mechanism for the DNS role
          type: bool
          required: false
          default: false
        nodeSelectionProvisioningRole:
          description:
          - Use the edge site as a node selection mechanism for the provisioning role
          type: bool
          required: false
          default: true
        addNamedService:
          description:
          - Add named service to the node
          type: bool
          required: false
          default: true
        addSlapdService:
          description:
          - Add slapd service to the node
          type: bool
          required: false
          default: true
        addNtpdService:
          description:
          - Add ntpd service to the node
          type: bool
          required: false
          default: true
        openTCPPortsOnHeadNode:
          description:
          - The list of TCP ports that will be opened in shorewall on the head node
          type: list
          required: false
          default: []
        openUDPPortsOnHeadNode:
          description:
          - The list of UDP ports that will be opened in shorewall on the head node
          type: list
          required: false
          default: []
        externallyVisibleIp:
          description:
          - IP that will be seen by other nodes when the director connects
          type: str
          required: false
          default: 0.0.0.0
        externallyVisibleHeadNodeIp:
          description:
          - Head node IP that will be use by this director
          type: str
          required: false
          default: 0.0.0.0
        syncCmShared:
          description:
          - Sync /cm/shared if required
          type: bool
          required: false
          default: true
    roles_LSFSubmitRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        lsfWlmClusters:
          description:
          - List of LSF clusters which the role belongs to
          type: list
          required: false
          default: []
        hostType:
          description:
          - Host type (possible values are defined in lsf.shared)
          type: str
          required: false
          default: LINUX
    roles_GenericRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        services:
          description:
          - Services managed by this role
          type: list
          required: false
          default: []
        extraEnvironment:
          description:
          - Additional environment to be passed to scripts
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            value:
              description:
              - Value
              type: str
              required: false
            nodeEnvironment:
              description:
              - Update the node environment variables
              type: bool
              required: false
              default: false
        excludeListSnippets:
          description: []
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            excludeList:
              description:
              - Excluded paths in the node image update
              type: list
              required: false
              default: []
            disabled:
              description:
              - Disabled
              type: bool
              required: false
              default: false
            noNewFiles:
              description:
              - No new files
              type: bool
              required: false
              default: false
            modeSync:
              description:
              - Include this snippet when mode is sync
              type: bool
              required: false
              default: true
            modeFull:
              description:
              - Include this snippet when mode is full
              type: bool
              required: false
              default: false
            modeUpdate:
              description:
              - Include this snippet when mode is update
              type: bool
              required: false
              default: true
            modeGrab:
              description:
              - Include this snippet when mode is grab
              type: bool
              required: false
              default: false
            modeGrabNew:
              description:
              - Include this snippet when mode is grab new
              type: bool
              required: false
              default: false
        dataNode:
          description:
          - If enabled the node will never do a FULL install without explicit user confirmation
          type: bool
          required: false
          default: false
        configuration_GenericRoleTemplatedConfiguration:
          description:
          - Configurations
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            createDirectory:
              description:
              - Create directory if it doesn't exist
              type: bool
              required: false
              default: true
            filename:
              description:
              - Filename
              type: str
              required: false
            mask:
              description:
              - Filemask directory
              type: int
              required: false
              default: 420
            userName:
              description:
              - User ownership applied to the file
              type: str
              required: false
            groupName:
              description:
              - Group ownership applied to the file
              type: str
              required: false
            disabled:
              description:
              - Disabled
              type: bool
              required: false
              default: false
            serviceActionOnWrite:
              description:
              - Action performed on service if the file changed
              type: str
              required: false
              default: RESTART
              choices:
              - NONE
              - RELOAD
              - RESTART
            serviceStopOnFailure:
              description:
              - Stop services if the file write failed
              type: bool
              required: false
              default: true
            templateContent:
              description:
              - Template to use for writing file
              type: str
              required: false
        configuration_GenericRoleStaticConfiguration:
          description:
          - Configurations
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            createDirectory:
              description:
              - Create directory if it doesn't exist
              type: bool
              required: false
              default: true
            filename:
              description:
              - Filename
              type: str
              required: false
            mask:
              description:
              - Filemask directory
              type: int
              required: false
              default: 420
            userName:
              description:
              - User ownership applied to the file
              type: str
              required: false
            groupName:
              description:
              - Group ownership applied to the file
              type: str
              required: false
            disabled:
              description:
              - Disabled
              type: bool
              required: false
              default: false
            serviceActionOnWrite:
              description:
              - Action performed on service if the file changed
              type: str
              required: false
              default: RESTART
              choices:
              - NONE
              - RELOAD
              - RESTART
            serviceStopOnFailure:
              description:
              - Stop services if the file write failed
              type: bool
              required: false
              default: true
            content:
              description:
              - Content to write into file
              type: str
              required: false
            filemask:
              description:
              - Filemask
              type: int
              required: false
              default: 420
        configuration_GenericRoleSymlinkConfiguration:
          description:
          - Configurations
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            createDirectory:
              description:
              - Create directory if it doesn't exist
              type: bool
              required: false
              default: true
            filename:
              description:
              - Filename
              type: str
              required: false
            mask:
              description:
              - Filemask directory
              type: int
              required: false
              default: 420
            userName:
              description:
              - User ownership applied to the file
              type: str
              required: false
            groupName:
              description:
              - Group ownership applied to the file
              type: str
              required: false
            disabled:
              description:
              - Disabled
              type: bool
              required: false
              default: false
            serviceActionOnWrite:
              description:
              - Action performed on service if the file changed
              type: str
              required: false
              default: RESTART
              choices:
              - NONE
              - RELOAD
              - RESTART
            serviceStopOnFailure:
              description:
              - Stop services if the file write failed
              type: bool
              required: false
              default: true
            sourceFilename:
              description:
              - Source filename
              type: str
              required: false
            watch:
              description:
              - Watch source file for changes, and treat as file change
              type: bool
              required: false
              default: false
        configuration_GenericRoleGeneratedConfiguration:
          description:
          - Configurations
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            createDirectory:
              description:
              - Create directory if it doesn't exist
              type: bool
              required: false
              default: true
            filename:
              description:
              - Filename
              type: str
              required: false
            mask:
              description:
              - Filemask directory
              type: int
              required: false
              default: 420
            userName:
              description:
              - User ownership applied to the file
              type: str
              required: false
            groupName:
              description:
              - Group ownership applied to the file
              type: str
              required: false
            disabled:
              description:
              - Disabled
              type: bool
              required: false
              default: false
            serviceActionOnWrite:
              description:
              - Action performed on service if the file changed
              type: str
              required: false
              default: RESTART
              choices:
              - NONE
              - RELOAD
              - RESTART
            serviceStopOnFailure:
              description:
              - Stop services if the file write failed
              type: bool
              required: false
              default: true
            script:
              description:
              - Script
              type: str
              required: false
            arguments:
              description:
              - Arguments
              type: list
              required: false
              default: []
            timeout:
              description:
              - Timeout
              type: int
              required: false
              default: 15
            watch:
              description:
              - Watch script for changes, and rerun
              type: bool
              required: false
              default: false
    roles_LSFServerRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        wlmCluster:
          description:
          - WLM cluster link to this WLM role
          type: str
          required: false
        externalServer:
          description:
          - LSF server daemons are running on some external machine
          type: bool
          required: false
          default: false
    roles_BackupRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        directory:
          description:
          - Directory where backups for other nodes are saved
          type: str
          required: false
          default: /var/spool/cmd/backup
        disabled:
          description:
          - Disabled nodes will no longer be used
          type: bool
          required: false
          default: false
        backupRing:
          description:
          - Only backup to nodes within the same ring
          type: int
          required: false
          default: 0
        maximumNumberOfBackups:
          description:
          - Maximum number of backups this node should be used for, set 0 for unlimited
          type: int
          required: false
          default: 0
    roles_LSFClientRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        wlmCluster:
          description:
          - WLM cluster link to this WLM role
          type: str
          required: false
        slots:
          description:
          - Number of slots available on this node/category
          type: str
          required: false
          default: auto
        queues:
          description:
          - Queues this node/nodes in this category belongs to
          type: list
          required: false
          default: []
        allQueues:
          description:
          - When set, the role will provide all available queues (the queues property
            will then be ignored)
          type: bool
          required: false
          default: false
        gpus:
          description:
          - Number of gpus
          type: int
          required: false
          default: 0
        gpuDevices:
          description:
          - /dev/* available to workload management
          type: list
          required: false
          default: []
        server:
          description:
          - Is LSF server (can run jobs)
          type: bool
          required: false
          default: true
        IMEX:
          description:
          - Start IMEX daemon from prolog/epilog
          type: bool
          required: false
          default: false
        hostModel:
          description:
          - Host model (possible values are defined in lsf.shared)
          type: str
          required: false
        hostType:
          description:
          - Host type (possible values are defined in lsf.shared)
          type: str
          required: false
          default: LINUX
        nodeCustomizations:
          description:
          - LSF node custom properties
          type: list
          required: false
          default: []
          elements: dict
          options:
            key:
              description:
              - Name of the key
              type: str
              required: false
            value:
              description:
              - Value for the key
              type: str
              required: false
            enabled:
              description:
              - Add the key/value to workload menegment node configuration or not
              type: bool
              required: false
              default: true
            notes:
              description:
              - Administrator notes
              type: str
              required: false
    roles_FailoverRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        syncCmShared:
          description:
          - Passive head node has a local copy of /cm/shared
          type: bool
          required: false
          default: false
    roles_JupyterHubRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        version:
          description:
          - JupyterHub version
          type: str
          required: false
        port:
          description:
          - Port for proxy (JupyterHub.port)
          type: int
          required: false
          default: 8000
        hubPort:
          description:
          - Port for hub (JupyterHub.hub_port)
          type: int
          required: false
          default: 8082
        hubIp:
          description:
          - The ip address or hostname for the Hub process to bind to (JupyterHub.hub_ip)
          type: str
          required: false
          default: 0.0.0.0
        proxyApiUrl:
          description:
          - The URL which the hub uses to connect to the proxy's API (c.ConfigurableHTTPProxy.api_url)
          type: str
          required: false
          default: http://127.0.0.1:8902
        dataFilesPath:
          description:
          - The location of jupyterhub data files (JupyterHub.data_files_path)
          type: str
          required: false
          default: /cm/shared/apps/jupyter/current/share/jupyterhub
        pamOpenSessions:
          description:
          - Enable SSL communication with HTTPS (PAMAuthenticator.open_sessions)
          type: bool
          required: false
          default: false
        ca:
          description:
          - Filename containing the PEM-encoded certificate used for the Certification
            authority (CA)
          type: str
          required: false
          default: /cm/local/apps/jupyter/conf/certs/my_sslca.cert
        cakey:
          description:
          - Filename containing the corresponding PEM-encoded private key used for the
            Certification authority (CA)
          type: str
          required: false
          default: /cm/local/apps/jupyter/conf/certs/my_sslca.key
        cert:
          description:
          - Path to the ssl certificate file (JupyterHub.ssl_cert)
          type: str
          required: false
          default: /cm/local/apps/jupyter/conf/certs/my_ssl.cert
        key:
          description:
          - Path to the ssl key file (JupyterHub.ssl_key)
          type: str
          required: false
          default: /cm/local/apps/jupyter/conf/certs/my_ssl.key
        adminUsers:
          description:
          - User with administrator privileges (Authenticator.admin_users)
          type: list
          required: false
          default: []
        userForService:
          description:
          - User for running cm-jupyterhub service (defined as User in /usr/lib/systemd/system/cm-jupyterhub.service)
          type: str
          required: false
          default: root
        trustedDomains:
          description:
          - Trusted domains to be included in JupyterHub certificates as Alt Subjects.
          type: list
          required: false
          default: []
        configs:
          description:
          - Configuration options JupyterHub
          type: list
          required: false
          default: []
          elements: dict
          options:
            key:
              description:
              - Configuration key
              type: str
              required: true
            value:
              description:
              - The value for the given configuration key, needs to be literal (include
                quotes for strings)
              type: str
              required: false
    roles_PbsProClientRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        wlmCluster:
          description:
          - WLM cluster link to this WLM role
          type: str
          required: false
        slots:
          description:
          - Number of slots available on this node/category
          type: str
          required: false
          default: AUTO
        queues:
          description:
          - Queues this node/nodes in this category belongs to
          type: list
          required: false
          default: []
        allQueues:
          description:
          - When set, the role will provide all available queues. (The queues property
            will then be ignored.)
          type: bool
          required: false
          default: false
        gpus:
          description:
          - Number of gpus
          type: int
          required: false
          default: 0
        gpuDevices:
          description:
          - /dev/* available to workload management
          type: list
          required: false
          default: []
        properties:
          description:
          - Node properties (a 'pnames' node attribute)
          type: list
          required: false
          default: []
        IMEX:
          description:
          - Start IMEX daemon from prolog/epilog
          type: bool
          required: false
          default: false
        momSettings:
          description:
          - Submode containing pbs_mom daemon settings
          type: dict
          required: false
          options:
            outputHostname:
              description:
              - Host to which all job standard output and standard error are delivered
                (PBS_OUTPUT_HOST_NAME parameter in pbs.conf)
              type: str
              required: false
            leafRouters:
              description:
              - Location of endpoint's pbs_comm daemon (PBS_LEAF_ROUTERS parameter in
                pbs.conf)
              type: list
              required: false
              default: []
            leafName:
              description:
              - Leaf name (PBS_LEAF_NAME parameter in pbs.conf)
              type: str
              required: false
            leafManagementFqdn:
              description:
              - Leaf name in pbs.conf is appended with FQDN from management network
              type: bool
              required: false
              default: false
            startMom:
              description:
              - Configure pbs_mom daemon start (PBS_START_MOM parameter in pbs.conf)
              type: bool
              required: false
              default: true
            spool:
              description:
              - PBS Pro mom spool directory
              type: str
              required: false
        commSettings:
          description:
          - Submode containing pbs_comm settings
          type: dict
          required: false
          options:
            commRouters:
              description:
              - Tells a pbs_comm where to find its fellow communication daemons (PBS_COMM_ROUTERS
                parameter in pbs.conf)
              type: list
              required: false
              default: []
            commThreads:
              description:
              - Tells pbs_comm how many threads to start (PBS_COMM_THREADS parameter in
                pbs.conf)
              type: int
              required: false
              default: 4
            startComm:
              description:
              - Configure pbs_com daemon start (PBS_START_COMM parameter in pbs.conf)
              type: bool
              required: false
              default: false
        nodeCustomizations:
          description:
          - PBS Pro node custom properties
          type: list
          required: false
          default: []
          elements: dict
          options:
            key:
              description:
              - Name of the key
              type: str
              required: false
            value:
              description:
              - Value for the key
              type: str
              required: false
            enabled:
              description:
              - Add the key/value to workload menegment node configuration or not
              type: bool
              required: false
              default: true
            notes:
              description:
              - Administrator notes
              type: str
              required: false
    roles_SnmpTrapRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        event:
          description:
          - Enable events
          type: bool
          required: false
          default: true
        mail:
          description:
          - Enable mail
          type: bool
          required: false
          default: true
        recipients:
          description:
          - Recipients
          type: list
          required: false
          default: []
        allAdministrators:
          description:
          - Also send e-mail to all administrators as defined in partition
          type: bool
          required: false
          default: false
        access:
          description:
          - Access string
          type: str
          required: false
          default: public
        server:
          description:
          - The SNMP server
          type: str
          required: false
        sender:
          description:
          - The sender of the e-mail
          type: str
          required: false
        arguments:
          description:
          - Additional script arguments
          type: list
          required: false
          default: []
        alternativeScript:
          description:
          - Alternative script
          type: str
          required: false
    roles_CloudGatewayRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
    roles_StorageRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        nfsThreads:
          description:
          - Number of nfs threads (0 for don't touch the current config file value)
          type: int
          required: false
          default: 0
        disableNFS1:
          description:
          - Disable NFS1, NFS threads needs to bet set
          type: bool
          required: false
          default: false
        disableNFS2:
          description:
          - Disable NFS2, NFS threads needs to bet set
          type: bool
          required: false
          default: false
        disableNFS3:
          description:
          - Disable NFS3, NFS threads needs to bet set
          type: bool
          required: false
          default: false
        disableNFS4:
          description:
          - Disable NFS4, NFS threads needs to bet set
          type: bool
          required: false
          default: false
        nfs4grace:
          description:
          - NFS4 grace period (0 for don't touch the current config file value)
          type: int
          required: false
          default: 0
        statdPort:
          description:
          - Stat daemon port (0 for don't touch the current config file value)
          type: int
          required: false
          default: 0
        statdOutgoingPort:
          description:
          - Stat daemon outgoing port (0 for don't touch the current config file value)
          type: int
          required: false
          default: 0
        mountdPort:
          description:
          - Mount daemon port (0 for don't touch the current config file value)
          type: int
          required: false
          default: 0
        rquotadPort:
          description:
          - Rquota daemon port (0 for don't touch the current config file value)
          type: int
          required: false
          default: 0
        lockdTcpPort:
          description:
          - Lock daemon TCP port (0 for don't touch the current config file value)
          type: int
          required: false
          default: 0
        lockdUdpPort:
          description:
          - Lock daemon UDP port (0 for don't touch the current config file value)
          type: int
          required: false
          default: 0
        rdmaPort:
          description:
          - RDMA port (0 for don't touch the current config file value)
          type: int
          required: false
          default: 0
    roles_SlurmClientRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        wlmCluster:
          description:
          - WLM cluster link to this WLM role
          type: str
          required: false
        slots:
          description:
          - Number of slots available on this node/category (set 0 for default)
          type: str
          required: false
          default: '0'
        queues:
          description:
          - Queues this node/nodes in this category belongs to
          type: list
          required: false
          default: []
        allQueues:
          description:
          - When set, the role will provide all available queues (the queues property
            will then be ignored)
          type: bool
          required: false
          default: false
        nodeAddr:
          description:
          - Name that a node should be referred to in establishing a communications path
          type: str
          required: false
        coresPerSocket:
          description:
          - Number of cores in a single physical processor socket
          type: int
          required: false
          default: 0
        features:
          description:
          - A list of arbitrary strings indicative of some characteristic associated with
            the node
          type: list
          required: false
          default: []
        tcpPort:
          description:
          - The port number that the Slurm compute node daemon, slurmd, listens to for
            work on this particular node
          type: int
          required: false
          default: 0
        realMemory:
          description:
          - Size of real memory on the node - The value will be truncated to the MiB
          type: int
          required: false
          default: 0
        sockets:
          description:
          - Number of physical processor sockets/chips on the node
          type: int
          required: false
          default: 0
        threadsPerCore:
          description:
          - Number of logical threads in a single physical core
          type: int
          required: false
          default: 0
        tmpDisk:
          description:
          - Total size of temporary disk storage in TmpFS in MegaBytes
          type: int
          required: false
          default: 0
        weight:
          description:
          - The priority of the node for scheduling purposes
          type: int
          required: false
          default: 0
        boards:
          description:
          - Number of baseboards in nodes with a baseboard controller
          type: int
          required: false
          default: 0
        socketsPerBoard:
          description:
          - Number of physical processor sockets/chips on a baseboard
          type: int
          required: false
          default: 0
        reason:
          description:
          - Identifies the reason for a node being in a particular state
          type: str
          required: false
        cpuSpecList:
          description:
          - A comma delimited list of Slurm abstract CPU IDs on which Slurm compute node
            daemons (slurmd, slurmstepd) will be confined
          type: list
          required: false
          default: []
        coreSpecCount:
          description:
          - Number of cores in a single physical processor socket
          type: int
          required: false
          default: 0
        memSpecLimit:
          description:
          - Limit on combined real memory allocation for compute node daemons (slurmd,
            slurmstepd)
          type: int
          required: false
          default: 0
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
        nodeCustomizations:
          description:
          - Slurm node custom properties
          type: list
          required: false
          default: []
          elements: dict
          options:
            key:
              description:
              - Name of the key
              type: str
              required: false
            value:
              description:
              - Value for the key
              type: str
              required: false
            enabled:
              description:
              - Add the key/value to workload menegment node configuration or not
              type: bool
              required: false
              default: true
            notes:
              description:
              - Administrator notes
              type: str
              required: false
        genericResources:
          description:
          - Slurm generic resources settings
          type: list
          required: false
          default: []
          elements: dict
          options:
            alias:
              description:
              - Unique alias name of the generic resource
              type: str
              required: false
            name:
              description:
              - Name of the generic resource in Slurm
              type: str
              required: false
            count:
              description:
              - Number of resources of this type available on this node (a suffix K, M,
                G, T or P may be used to multiply the number by 1024, 1048576, etc. respectively)
              type: str
              required: false
            cores:
              description:
              - Specify the first thread CPU index numbers for the specific cores which
                can use this resource (e.g. '0,1,2,3' or '0-3')
              type: str
              required: false
            type:
              description:
              - An arbitrary string identifying the type of device
              type: str
              required: false
            file:
              description:
              - Fully qualified pathname of the device files associated with a resource
                (simple regular expressions are supported)
              type: str
              required: false
            consumable:
              description:
              - Multiple jobs can use the same generic resource
              type: bool
              required: false
              default: true
            addToGresConfig:
              description:
              - Add the generic resource entity to gres.conf
              type: bool
              required: false
              default: true
            Flags:
              description:
              - Optional flags that can be specified to change configured behavior of
                the GRES
              type: list
              required: false
              default: []
            Links:
              description:
              - A list of numbers identifying the number of connections between this device
                and other devices to allow coscheduling of better connected devices
              type: list
              required: false
              default: []
            MultipleFiles:
              description:
              - A list of device file paths (in the range format) associated with the
                GRES
              type: list
              required: false
              default: []
        cpuBind:
          description:
          - Bindings from task to resources
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
        hardwareAutoDetection:
          description:
          - The actual hardware configuration probed by slurmd -C
          type: bool
          required: false
          default: true
        memoryAutoDetectionSlack:
          description:
          - Autodetected memory will be reduced by this percentage when put in slurm.conf
          type: float
          required: false
          default: 0.1
        IMEX:
          description:
          - Start IMEX daemon from prolog/epilog
          type: bool
          required: false
          default: false
        forceWriteProcs:
          description:
          - Always add Procs to autodetected CPU parameters in slurm.conf
          type: bool
          required: false
          default: false
        useProcsOnly:
          description:
          - Whether only Procs parameter (and not autodetected CPU parameters) will be
            written in slurm.conf
          type: bool
          required: false
          default: false
        nodesets:
          description:
          - List of nodesets where nodes with this role will be added
          type: list
          required: false
          default: []
        nodesetFeatures:
          description:
          - List of features that will be added to the Slurm nodes, together with nodesets
            that will be created in Slurm for these features
          type: list
          required: false
          default: []
        wpps:
          description:
          - Workload power profile settings mode
          type: dict
          required: false
          options:
            disabled:
              description:
              - Disable jobs from changing NVIDIA workload profiles
              type: bool
              required: false
              default: true
            failOnError:
              description:
              - Should prolog and epilog fail when workload power profile change fails
              type: bool
              required: false
              default: false
            jobKeyword:
              description:
              - Keyword used by WLM job to specify the workload profile settings
              type: str
              required: false
              default: wpps
            jobsProfilesDir:
              description:
              - Directory where prolog creates job ID directories that include workload
                power profile subdirectories.
              type: str
              required: false
              default: /var/run/nvidia/workload-power-profiles
            debug:
              description:
              - Enable prolog and epilog debug mode
              type: bool
              required: false
              default: false
            debugLogDir:
              description:
              - Debug log directory where prolog and epilog will create log files per
                job
              type: str
              required: false
              default: /var/spool/cmd/wlm/wpps
        addToTopology:
          description:
          - When set, the node is added to topology.conf if topology generation is configured
          type: bool
          required: false
          default: true
    roles_KubeletRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        kubeCluster:
          description:
          - The Kubernetes cluster instance (pointer)
          type: str
          required: false
        controlPlane:
          description:
          - Control plane node
          type: bool
          required: false
          default: true
        worker:
          description:
          - Worker node
          type: bool
          required: false
          default: true
        containerRuntimeService:
          description:
          - The container runtime systemd service
          type: str
          required: false
          default: docker.service
        maxPods:
          description:
          - Number of Pods that can run on this node
          type: int
          required: false
          default: 110
        options:
          description:
          - Options to overrule flags for Kube components
          type: json
          required: false
        custom_yaml:
          description:
          - Custom YAML to apply to /var/lib/kubelet/config.yaml
          type: str
          required: false
    roles_SlurmSubmitRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        slurmJobQueueAcccessList:
          description:
          - List of slurm clusters and their associated queues that can be submitted to
          type: list
          required: false
          default: []
          elements: dict
          options:
            wlmCluster:
              description:
              - WLM cluster link to this job queue access list
              type: str
              required: false
            slurmJobQueue:
              description:
              - List of queues that can be submitted to. If none is specified, this access
                list will submit to all job queues in the specified WlmCluster.
              type: list
              required: false
              default: []
    roles_PRSServerRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        configServerPort:
          description:
          - Port for the PRS config service
          type: int
          required: false
          default: 8880
        jobSchedulerServerPort:
          description:
          - Port for the job scheduler serverv
          type: int
          required: false
          default: 8881
        timeout:
          description:
          - Service pythoncm RPC timeout
          type: int
          required: false
          default: 10
        interval:
          description:
          - Service loop interval
          type: int
          required: false
          default: 30
        window:
          description:
          - Number of samples in the history taken into account
          type: int
          required: false
          default: 5
        serverCertificatePath:
          description:
          - PRS certificate path for the web server
          type: str
          required: false
          default: /cm/local/apps/prs/etc/server.pem
        serverPrivateKeyPath:
          description:
          - PRS private key path for the web server
          type: str
          required: false
          default: /cm/local/apps/prs/etc/server.key
        serverCACertificatePath:
          description:
          - CA certificate path
          type: str
          required: false
          default: /cm/local/apps/prs/etc/ca.pem
        serverCAPrivateKeyPath:
          description:
          - CA certificate path
          type: str
          required: false
          default: /cm/local/apps/prs/etc/ca.key
        cmdCertificatePath:
          description:
          - Certificate path for CMD to call the PRS server
          type: str
          required: false
          default: /cm/local/apps/prs/etc/cmd.pem
        cmdPrivateKeyPath:
          description:
          - Private key path for CMD to call the PRS server
          type: str
          required: false
          default: /cm/local/apps/prs/etc/cmd.key
        clientCertificatePath:
          description:
          - PRS client certificate path to call CMD
          type: str
          required: false
          default: /cm/local/apps/prs/etc/prs.pem
        clientPrivateKeyPath:
          description:
          - PRS client private key path to call CMD
          type: str
          required: false
          default: /cm/local/apps/prs/etc/prs.key
        clientCACertificatePath:
          description:
          - CA certificate path of CMD
          type: str
          required: false
          default: /cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages/pythoncm/etc/cacert.pem
        domains:
          description:
          - Domains
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            powerBudget:
              description:
              - Power budget
              type: int
              required: false
              default: 0
            powerDrawFactor:
              description:
              - Power draw factor
              type: float
              required: false
              default: 1.0
            powerDrawModel:
              description:
              - Power draw model
              type: str
              required: false
              default: LINEAR
              choices:
              - LINEAR
            powerBudgetModel:
              description:
              - Power budget model
              type: str
              required: false
              default: SCALAR
              choices:
              - SCALAR
            groupBy:
              description:
              - Create a domain per group
              type: str
              required: false
              default: ALL
              choices:
              - ALL
              - RACK
              - ROW
              - ROOM
              - BUILDING
              - LOCATION
              - CIRCUIT
            autostart:
              description:
              - Auto start domain on creation
              type: bool
              required: false
              default: true
            excludeNodes:
              description:
              - List of nodes to exclude from the domain
              type: list
              required: false
              default: []
            excludeRacks:
              description:
              - List of racks to exclude from the domain
              type: list
              required: false
              default: []
    roles_BeeGFSMetadataRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        configurations:
          description:
          - List of BeeGFS metadata configurations
          type: list
          required: false
          default: []
          elements: dict
          options:
            ref_beegfs_cluster_uuid:
              description:
              - BeeGFS cluster
              - (Field should be formatted as a UUID)
              type: str
              required: true
              default: None
            dataDir:
              description:
              - Path to the data directory
              type: str
              required: false
              default: /var/lib/beegfs/metadata
            bindToNumaZone:
              description:
              - Zero-based NUMA zone number to which all threads of metadata process should
                be bound
              type: str
              required: false
            runDaemonized:
              description:
              - Run the storage service as a daemon
              type: bool
              required: false
              default: true
            clientXAttrs:
              description:
              - Enable client-side extended attributes
              type: bool
              required: false
              default: false
            clientACLs:
              description:
              - Enable handling and storage of client-side ACLs
              type: bool
              required: false
              default: false
            useExtendedAttributes:
              description:
              - Store metadata as extended attributes or not
              type: bool
              required: false
              default: true
            allowUserSetPattern:
              description:
              - Allow non-privileged users to modify stripe pattern settings for directories
                they own
              type: bool
              required: false
              default: false
            useAggressiveStreamPoll:
              description:
              - Actively poll for events instead of sleeping until an event occur
              type: bool
              required: false
              default: false
            usePerUserMsgQueues:
              description:
              - Use per-user queues for pending requests
              type: bool
              required: false
              default: false
            targetChooser:
              description:
              - The algorithm to choose storage targets for file creation
              type: str
              required: false
              default: RANDOMIZED
              choices:
              - RANDOMIZED
              - ROUNDROBIN
              - RANDOMROBIN
              - RANDOMINTERNODE
              - RANDOMINTRANODE
            targetOfflineTimeout:
              description:
              - Timeout until targets on a storage server are considered offline when
                no target status is received
              type: int
              required: false
              default: 180
            targetAttachmentFile:
              description:
              - File with a list of targets to be grouped within the same domain for randominternode
              type: str
              required: false
            numberOfStreamListeners:
              description:
              - The number of threads waiting for incoming data events
              type: int
              required: false
              default: 1
            numberOfWorkers:
              description:
              - Number of worker threads
              type: int
              required: false
              default: 0
            startByCMDaemon:
              description:
              - Start service by CMDaemon or manually
              type: bool
              required: false
              default: true
            connectionSettings:
              description:
              - Submode containing BeeGFS metadata connection settings
              type: dict
              required: false
              options:
                portTCP:
                  description:
                  - TCP port for the service
                  type: int
                  required: false
                  default: 8005
                portUDP:
                  description:
                  - UDP port for the service
                  type: int
                  required: false
                  default: 8005
                backlogTCP:
                  description:
                  - TCP listen backlog
                  type: int
                  required: false
                  default: 128
                maxInternodeNumber:
                  description:
                  - Max number of simultaneous connections to the same node
                  type: int
                  required: false
                  default: 12
                fallbackExpiration:
                  description:
                  - Time after which a connection to a fallback interface expires
                  type: int
                  required: false
                  default: 900
                interfacesFile:
                  description:
                  - Path to the file with a list of interfaces for communication
                  type: str
                  required: false
                interfacesList:
                  description:
                  - List of interfaces for communication
                  type: list
                  required: false
                  default: []
                netFilterFile:
                  description:
                  - Path to a file with a list of allowed IP subnets
                  type: str
                  required: false
                tcpOnlyFilterFile:
                  description:
                  - Path to a file with a list of no-RDMA IP ranges
                  type: str
                  required: false
                useRDMA:
                  description:
                  - Use RDMA
                  type: bool
                  required: false
                  default: true
                rdmaTypeOfService:
                  description:
                  - RDMA type of service
                  type: int
                  required: false
                  default: 0
            logSettings:
              description:
              - Submode containing BeeGFS logging settings
              type: dict
              required: false
              options:
                logType:
                  description:
                  - Defines the logger type. This can either be 'syslog' to send log messages
                    to the general system logger or 'logfile'
                  type: str
                  required: false
                  default: SYSLOG
                  choices:
                  - SYSLOG
                  - LOGFILE
                level:
                  description:
                  - Log level
                  type: int
                  required: false
                  default: 2
                noDate:
                  description:
                  - Do not show date along with time in log
                  type: bool
                  required: false
                  default: false
                numberOfLines:
                  description:
                  - Number of lines in log file, after which it will be rotated
                  type: int
                  required: false
                  default: 50000
                numberOfRotatedFiles:
                  description:
                  - Number of old log files to keep
                  type: int
                  required: false
                  default: 5
                file:
                  description:
                  - Path to the log file, empty means logs go to the journal
                  type: str
                  required: false
    roles_PbsProServerRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        wlmCluster:
          description:
          - WLM cluster link to this WLM role
          type: str
          required: false
        externalServer:
          description:
          - PBS Pro server daemons are running on some external machine
          type: bool
          required: false
          default: false
        commSettings:
          description:
          - Submode containing pbs_comm settings
          type: dict
          required: false
          options:
            commRouters:
              description:
              - Tells a pbs_comm where to find its fellow communication daemons (PBS_COMM_ROUTERS
                parameter in pbs.conf)
              type: list
              required: false
              default: []
            commThreads:
              description:
              - Tells pbs_comm how many threads to start (PBS_COMM_THREADS parameter in
                pbs.conf)
              type: int
              required: false
              default: 4
            startComm:
              description:
              - Configure pbs_com daemon start (PBS_START_COMM parameter in pbs.conf)
              type: bool
              required: false
              default: false
    roles_EtcdHostRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        memberName:
          description:
          - Human-readable name for this member ($hostname will be replaced to the node
            hostname)
          type: str
          required: false
          default: $hostname
        spool:
          description:
          - Path to the data directory
          type: str
          required: false
          default: /var/lib/etcd
        listenClientUrls:
          description:
          - List of URLs to listen on for client traffic
          type: list
          required: false
          default:
          - https://0.0.0.0:2379
        listenPeerUrls:
          description:
          - List of URLs to listen on for peer traffic
          type: list
          required: false
          default:
          - https://0.0.0.0:2380
        advertiseClientUrls:
          description:
          - List of this member's client URLs to advertise to the public
          type: list
          required: false
          default:
          - https://$ip:2379
        advertisePeerUrls:
          description:
          - List of this member's peer URLs to advertise to the rest of the cluster
          type: list
          required: false
          default:
          - https://$ip:2380
        snapshotCount:
          description:
          - Number of committed transactions to trigger a snapshot to disk
          type: int
          required: false
          default: 100000
        maxSnapshots:
          description:
          - Maximum number of snapshot files to retain (0 is unlimited)
          type: int
          required: false
          default: 5
        loglevel:
          description:
          - Log level, only supports debug, info, warn, error, panic, or fatal.
          type: str
          required: false
          default: INFO
          choices:
          - INFO
          - DEBUG
          - WARN
          - ERROR
          - PANIC
          - FATAL
        options:
          description:
          - Additional parameters for etcd daemon
          type: list
          required: false
          default: []
        etcdCluster:
          description:
          - The Etcd cluster instance
          type: str
          required: false
        memberCertificate:
          description:
          - Etcd member certificate, signed with CA specified in the Etcd Cluster. When
            set it will overrule the value from the EtcdCluster object.
          type: str
          required: false
        memberCertificateKey:
          description:
          - Etcd member certificate key, signed with CA specified in the Etcd Cluster.
            When set it will overrule the value from the EtcdCluster object.
          type: str
          required: false
    roles_BootRole:
      description:
      - Assign the roles
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        addServices:
          description:
          - Add services to nodes which belong to this node. Be careful setting this to
            false.
          type: bool
          required: false
          default: true
        nodegroups:
          description:
          - List of node groups which can boot from this node
          type: list
          required: false
          default: []
        categories:
          description:
          - List of categories which can boot from this node
          type: list
          required: false
          default: []
        racks:
          description:
          - List of racks which can boot from this node
          type: list
          required: false
          default: []
        softwareImages:
          description:
          - List of software images from which can be booted, leave empty for all images
          type: list
          required: false
          default: []
        allowRamdiskCreation:
          description:
          - Allow the node to create ramdisks by itself, instead of waiting for them to
            be rsynced from the headnode
          type: bool
          required: false
          default: false
        disableAutomaticExports:
          description:
          - Disable creation of automatic filesystem exports
          type: bool
          required: false
          default: false
        imagesFromProvisioningRole:
          description:
          - Only allow nodes to boot from images defined in the provisioning role
          type: bool
          required: false
          default: false
        syncFSParts:
          description:
          - Sync FSParts mode
          type: str
          required: false
          default: AUTO
          choices:
          - AUTO
          - ALL
          - CUSTOM
        fsparts:
          description:
          - FSParts
          type: list
          required: false
          default: []
        extra_values:
          description: []
          type: json
          required: false

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
configuration_overlay:
  type: complex
  description: Configuration overlay
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
    allHeadNodes:
      type: bool
      description: All head nodes
      returned: success
    nodes:
      type: list
      description: List of nodes belonging to this group
      returned: success
    categories:
      type: list
      description: List of categories belonging to this group
      returned: success
    customizationFiles:
      type: list
      description: Config file customizations
      returned: success
    roles:
      type: list
      description: Assign the roles
      returned: success
    priority:
      type: int
      description: Priority of the roles, node roles have a 750 priority, and category
        roles 250, set to -1 disable the overlay
      returned: success

"""
############################
# Imports
############################

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import ConfigurationOverlay
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.configuration_overlay import ConfigurationOverlay_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=ConfigurationOverlay_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, ConfigurationOverlay)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(ConfigurationOverlay, params, commit=not module.check_mode)
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