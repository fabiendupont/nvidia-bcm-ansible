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

class PrometheusQuery_ArgSpec:
    argument_spec = {'access': {'choices': ['PUBLIC', 'PRIVATE', 'INDIVIDUAL'],
                                'default': 'PUBLIC',
                                'type': 'str'},
                     'alias': {'type': 'str'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'cumulative': {'default': True, 'type': 'bool'},
                     'currency': {'default': '$', 'type': 'str'},
                     'description': {'type': 'str'},
                     'drilldown': {'elements': 'dict',
                                   'options': {'name': {'required': True, 'type': 'str'},
                                               'parameters': {'type': 'list'},
                                               'query': {'type': 'str'}},
                                   'type': 'list'},
                     'endTime': {'type': 'str'},
                     'extra_values': {'type': 'json'},
                     'interval': {'default': 0, 'type': 'float'},
                     'name': {'required': True, 'type': 'str'},
                     'notes': {'type': 'str'},
                     'preference': {'default': 0, 'type': 'int'},
                     'price': {'default': 0.0, 'type': 'float'},
                     'query': {'type': 'str'},
                     'startTime': {'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'typeClass': {'type': 'str'},
                     'unit': {'type': 'str'}}