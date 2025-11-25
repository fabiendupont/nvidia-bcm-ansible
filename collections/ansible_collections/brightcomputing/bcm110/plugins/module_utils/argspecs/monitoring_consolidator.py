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

class MonitoringConsolidator_ArgSpec:
    argument_spec = {'cloneFrom': {'default': '', 'type': 'str'},
                     'consolidators': {'elements': 'dict',
                                       'options': {'interval': {'default': 3600, 'type': 'float'},
                                                   'kind': {'choices': ['AVERAGE',
                                                                        'MINIMUM',
                                                                        'MAXIMUM'],
                                                            'default': 'AVERAGE',
                                                            'type': 'str'},
                                                   'maxAge': {'default': 0.0, 'type': 'float'},
                                                   'maxSamples': {'default': 65536, 'type': 'int'},
                                                   'name': {'required': True, 'type': 'str'},
                                                   'offset': {'default': 0.0, 'type': 'float'}},
                                       'type': 'list'},
                     'disabled': {'default': False, 'type': 'bool'},
                     'name': {'required': True, 'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'}}