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

class User_ArgSpec:
    argument_spec = {'ID': {'type': 'str'},
                     'allowGPUWorkloadPowerProfiles': {'default': False, 'type': 'bool'},
                     'authorizedSshKeys': {'type': 'str'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'commonName': {'type': 'str'},
                     'createSshKey': {'default': False, 'type': 'bool'},
                     'disablePasswordSsh': {'default': False, 'type': 'bool'},
                     'email': {'type': 'str'},
                     'groupID': {'type': 'str'},
                     'homeDirOperation': {'default': True, 'type': 'bool'},
                     'homeDirectory': {'type': 'str'},
                     'homePage': {'type': 'str'},
                     'loginShell': {'type': 'str'},
                     'name': {'required': True, 'type': 'str'},
                     'notes': {'type': 'str'},
                     'password': {'no_log': True, 'type': 'str'},
                     'profile': {'type': 'str'},
                     'projectManager': {'options': {'accounts': {'type': 'list'},
                                                    'op': {'choices': ['AND', 'OR'],
                                                           'default': 'OR',
                                                           'type': 'str'},
                                                    'users': {'type': 'list'}},
                                        'type': 'dict'},
                     'shadowExpire': {'default': 24837, 'type': 'int'},
                     'shadowInactive': {'default': 0, 'type': 'int'},
                     'shadowMax': {'default': 999999, 'type': 'int'},
                     'shadowMin': {'default': 0, 'type': 'int'},
                     'shadowWarning': {'default': 7, 'type': 'int'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'surname': {'type': 'str'},
                     'writeSshProxyConfig': {'default': False, 'type': 'bool'}}