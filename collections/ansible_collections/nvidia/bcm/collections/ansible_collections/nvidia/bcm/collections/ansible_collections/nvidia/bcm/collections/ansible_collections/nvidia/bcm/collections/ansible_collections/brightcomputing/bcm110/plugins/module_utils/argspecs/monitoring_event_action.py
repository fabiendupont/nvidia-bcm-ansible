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

class MonitoringEventAction_ArgSpec:
    argument_spec = {'allowedTime': {'type': 'str'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'disable': {'default': False, 'type': 'bool'},
                     'extra_values': {'type': 'json'},
                     'mergeDelay': {'default': 1.0, 'type': 'float'},
                     'name': {'required': True, 'type': 'str'},
                     'profiles': {'type': 'list'},
                     'runOn': {'choices': ['NODE', 'ACTIVE', 'MONITORING_NODE'],
                               'default': 'ACTIVE',
                               'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'suppressedByGoingDown': {'default': False, 'type': 'bool'},
                     'userNames': {'type': 'list'}}