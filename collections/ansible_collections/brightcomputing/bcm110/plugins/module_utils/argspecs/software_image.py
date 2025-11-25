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

class SoftwareImage_ArgSpec:
    argument_spec = {'SOLFlowControl': {'default': True, 'type': 'bool'},
                     'SOLPort': {'default': 'ttyS1', 'type': 'str'},
                     'SOLSpeed': {'choices': ['115200',
                                              '57600',
                                              '38400',
                                              '19200',
                                              '9600',
                                              '4800',
                                              '2400',
                                              '1200'],
                                  'default': '115200',
                                  'type': 'str'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'enableSOL': {'default': False, 'type': 'bool'},
                     'kernelOutputConsole': {'default': 'tty0', 'type': 'str'},
                     'kernelParameters': {'type': 'str'},
                     'kernelVersion': {'type': 'str'},
                     'modules': {'elements': 'dict',
                                 'options': {'name': {'required': True, 'type': 'str'},
                                             'parameters': {'type': 'str'}},
                                 'type': 'list'},
                     'name': {'required': True, 'type': 'str'},
                     'notes': {'type': 'str'},
                     'path': {'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'}}