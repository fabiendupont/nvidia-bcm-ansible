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

class OCIShape_ArgSpec:
    argument_spec = {'cloneFrom': {'default': '', 'type': 'str'},
                     'cpu': {'type': 'str'},
                     'cpusMax': {'default': 0, 'type': 'int'},
                     'cpusMin': {'default': 0, 'type': 'int'},
                     'description': {'type': 'str'},
                     'disks': {'type': 'str'},
                     'gpu': {'type': 'str'},
                     'isFlexible': {'default': False, 'type': 'bool'},
                     'maxVnics': {'default': 0, 'type': 'int'},
                     'memory': {'type': 'str'},
                     'memoryMax': {'default': 0, 'type': 'int'},
                     'memoryMaxPerCpu': {'default': 0, 'type': 'int'},
                     'memoryMin': {'default': 0, 'type': 'int'},
                     'memoryMinPerCpu': {'default': 0, 'type': 'int'},
                     'name': {'required': True, 'type': 'str'},
                     'networkPorts': {'default': 0, 'type': 'int'},
                     'provider': {'type': 'str'},
                     'rdmaPorts': {'default': 0, 'type': 'int'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'}}