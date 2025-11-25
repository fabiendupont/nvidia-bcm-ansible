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

class MonitoringMeasurableHealthCheck_ArgSpec:
    argument_spec = {'access': {'choices': ['PUBLIC', 'PRIVATE', 'INDIVIDUAL', 'INHERIT'],
                                'default': 'INHERIT',
                                'type': 'str'},
                     'associatedUser': {'type': 'str'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'consolidator': {'type': 'str'},
                     'description': {'type': 'str'},
                     'disableTriggers': {'default': False, 'type': 'bool'},
                     'disabled': {'default': False, 'type': 'bool'},
                     'gap': {'default': 0, 'type': 'int'},
                     'introduceNaN': {'default': False, 'type': 'bool'},
                     'maxAge': {'default': 0.0, 'type': 'float'},
                     'maxSamples': {'default': 0, 'type': 'int'},
                     'name': {'required': True, 'type': 'str'},
                     'parameter': {'type': 'str'},
                     'producer': {'type': 'str'},
                     'sourceType': {'choices': ['ANY', 'BRIGHT', 'PROMETHEUS', 'BOTH'],
                                    'default': 'BRIGHT',
                                    'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'suppressedByGoingDown': {'default': False, 'type': 'bool'},
                     'typeClass': {'type': 'str'}}