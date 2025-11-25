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

class MonitoringScriptAction_ArgSpec:
    argument_spec = {'allowedTime': {'type': 'str'},
                     'arguments': {'type': 'list'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'disable': {'default': False, 'type': 'bool'},
                     'extra_values': {'type': 'json'},
                     'mergeDelay': {'default': 0.0, 'type': 'float'},
                     'mergeMeasurable': {'default': False, 'type': 'bool'},
                     'mergeTrigger': {'default': False, 'type': 'bool'},
                     'name': {'required': True, 'type': 'str'},
                     'nodeEnvironment': {'default': False, 'type': 'bool'},
                     'runInShell': {'default': False, 'type': 'bool'},
                     'runOn': {'choices': ['NODE', 'ACTIVE', 'MONITORING_NODE'],
                               'default': 'ACTIVE',
                               'type': 'str'},
                     'script': {'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'suppressedByGoingDown': {'default': False, 'type': 'bool'},
                     'timeout': {'default': 5, 'type': 'int'}}