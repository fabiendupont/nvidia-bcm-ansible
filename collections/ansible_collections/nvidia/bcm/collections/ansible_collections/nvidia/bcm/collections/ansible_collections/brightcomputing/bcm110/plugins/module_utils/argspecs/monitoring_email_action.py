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

class MonitoringEmailAction_ArgSpec:
    argument_spec = {'allAdministrators': {'default': False, 'type': 'bool'},
                     'allowedTime': {'type': 'str'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'disable': {'default': False, 'type': 'bool'},
                     'extra_values': {'type': 'json'},
                     'info': {'type': 'str'},
                     'mergeDelay': {'default': 0.0, 'type': 'float'},
                     'mergeMeasurable': {'default': False, 'type': 'bool'},
                     'mergeTrigger': {'default': False, 'type': 'bool'},
                     'name': {'required': True, 'type': 'str'},
                     'recipients': {'type': 'list'},
                     'runOn': {'choices': ['NODE', 'ACTIVE', 'MONITORING_NODE'],
                               'default': 'ACTIVE',
                               'type': 'str'},
                     'sender': {'type': 'str'},
                     'server': {'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'suppressedByGoingDown': {'default': False, 'type': 'bool'},
                     'timeout': {'default': 15, 'type': 'int'}}