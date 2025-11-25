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

class SlurmJobQueue_ArgSpec:
    argument_spec = {'SelectTypeParameters': {'type': 'str'},
                     'allocNodes': {'type': 'list'},
                     'allowAccounts': {'default': 'ALL', 'type': 'str'},
                     'allowGroups': {'default': 'ALL', 'type': 'str'},
                     'allowQos': {'default': 'ALL', 'type': 'str'},
                     'alternate': {'type': 'str'},
                     'categories': {'type': 'list'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'computeNodes': {'type': 'list'},
                     'cpuBind': {'choices': ['NONE', 'BOARD', 'SOCKET', 'LDOM', 'CORE', 'THREAD'],
                                 'default': 'NONE',
                                 'type': 'str'},
                     'defCpuPerGPU': {'default': 'UNLIMITED', 'type': 'str'},
                     'defMemPerCPU': {'default': 'UNLIMITED', 'type': 'str'},
                     'defMemPerGPU': {'default': 'UNLIMITED', 'type': 'str'},
                     'defMemPerNode': {'default': 'UNLIMITED', 'type': 'str'},
                     'defaultQueue': {'default': False, 'type': 'bool'},
                     'defaultTime': {'default': 'UNLIMITED', 'type': 'str'},
                     'denyAccounts': {'type': 'str'},
                     'denyQos': {'type': 'str'},
                     'disableRoot': {'default': False, 'type': 'bool'},
                     'exclusiveUser': {'default': False, 'type': 'bool'},
                     'graceTime': {'default': 0, 'type': 'int'},
                     'hidden': {'default': False, 'type': 'bool'},
                     'lln': {'default': False, 'type': 'bool'},
                     'maxCPUsPerNode': {'default': 'UNLIMITED', 'type': 'str'},
                     'maxMemPerCPU': {'default': 'UNLIMITED', 'type': 'str'},
                     'maxMemPerNode': {'default': 'UNLIMITED', 'type': 'str'},
                     'maxNodes': {'default': 'UNLIMITED', 'type': 'str'},
                     'maxTime': {'default': 'UNLIMITED', 'type': 'str'},
                     'minNodes': {'default': '1', 'type': 'str'},
                     'name': {'required': True, 'type': 'str'},
                     'nodegroups': {'type': 'list'},
                     'nodesets': {'type': 'list'},
                     'options': {'type': 'list'},
                     'ordering': {'default': 0, 'type': 'int'},
                     'overSubscribe': {'default': 'NO', 'type': 'str'},
                     'overlays': {'type': 'list'},
                     'preemptMode': {'default': 'OFF', 'type': 'str'},
                     'priorityJobFactor': {'default': 1, 'type': 'int'},
                     'priorityTier': {'default': 1, 'type': 'int'},
                     'qos': {'type': 'str'},
                     'reqResv': {'default': 'NO', 'type': 'str'},
                     'rootOnly': {'default': False, 'type': 'bool'},
                     'state': {'choices': ['NONE', 'UP', 'DOWN', 'DRAIN', 'INACTIVE'],
                               'default': 'NONE',
                               'type': 'str'},
                     'tresBillingWeights': {'type': 'list'},
                     'wlmCluster': {'type': 'str'}}