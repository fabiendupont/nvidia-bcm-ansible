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

class MonitoringMeasurableMetric_ArgSpec:
    argument_spec = {'access': {'choices': ['PUBLIC', 'PRIVATE', 'INDIVIDUAL', 'INHERIT'],
                                'default': 'INHERIT',
                                'type': 'str'},
                     'associatedUser': {'type': 'str'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'consolidator': {'type': 'str'},
                     'cumulative': {'default': False, 'type': 'bool'},
                     'description': {'type': 'str'},
                     'disableTriggers': {'default': False, 'type': 'bool'},
                     'disabled': {'default': False, 'type': 'bool'},
                     'gap': {'default': 0, 'type': 'int'},
                     'integer': {'default': False, 'type': 'bool'},
                     'introduceNaN': {'default': False, 'type': 'bool'},
                     'maxAge': {'default': 0.0, 'type': 'float'},
                     'maxSamples': {'default': 0, 'type': 'int'},
                     'maximum': {'default': 0.0, 'type': 'float'},
                     'minimum': {'default': 0.0, 'type': 'float'},
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
                     'typeClass': {'type': 'str'},
                     'unit': {'type': 'str'}}