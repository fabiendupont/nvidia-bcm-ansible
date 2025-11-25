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

class LSFWlmCluster_ArgSpec:
    argument_spec = {'accounting': {'options': {'extractAccountingInfo': {'default': True,
                                                                          'type': 'bool'},
                                                'jobCommentLabels': {'type': 'list'},
                                                'managedHierarchy': {'type': 'list'},
                                                'separator': {'default': '_', 'type': 'str'}},
                                    'type': 'dict'},
                     'cgroups': {'options': {'jobCgroupTemplate': {'default': 'lsf/$CLUSTER/job.$JOBID.*',
                                                                   'type': 'str'},
                                             'linuxCgroupAccounting': {'default': True,
                                                                       'type': 'bool'},
                                             'mountPoint': {'default': '/sys/fs/cgroup',
                                                            'type': 'str'},
                                             'processTracking': {'default': True, 'type': 'bool'},
                                             'resourceEnforce': {'default': ['memory', 'cpu'],
                                                                 'type': 'list'}},
                                 'type': 'dict'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'dcgmPort': {'default': 0, 'type': 'int'},
                     'doBackups': {'default': True, 'type': 'bool'},
                     'dynamicCloudNodes': {'default': False, 'type': 'bool'},
                     'dynamicHostWaitTime': {'default': 18000, 'type': 'int'},
                     'enableEgo': {'default': False, 'type': 'bool'},
                     'enablePostJob': {'default': False, 'type': 'bool'},
                     'enablePreJob': {'default': False, 'type': 'bool'},
                     'gpuAutoconfig': {'default': False, 'type': 'bool'},
                     'gpuNewSyntax': {'default': False, 'type': 'bool'},
                     'hostAddressRange': {'default': '*.*', 'type': 'str'},
                     'localVar': {'default': '/cm/local/apps/lsf/var', 'type': 'str'},
                     'logDir': {'default': '/cm/local/apps/lsf/var/log', 'type': 'str'},
                     'manageMIG': {'default': False, 'type': 'bool'},
                     'moduleFileTemplate': {'type': 'str'},
                     'name': {'required': True, 'type': 'str'},
                     'network': {'type': 'str'},
                     'noQueueHostsString': {'type': 'str'},
                     'placeholders': {'elements': 'dict',
                                      'options': {'baseNodeName': {'default': 'placeholder',
                                                                   'type': 'str'},
                                                  'maxNodes': {'default': 0, 'type': 'int'},
                                                  'queue': {'type': 'str'},
                                                  'templateNode': {'type': 'str'}},
                                      'type': 'list'},
                     'prefix': {'type': 'str'},
                     'primaryServer': {'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'tracingJobs': {'type': 'list'},
                     'unitForLimits': {'default': 'MB', 'type': 'str'},
                     'var': {'default': '/cm/shared/apps/lsf/var', 'type': 'str'},
                     'version': {'choices': ['10.1'], 'type': 'str'}}