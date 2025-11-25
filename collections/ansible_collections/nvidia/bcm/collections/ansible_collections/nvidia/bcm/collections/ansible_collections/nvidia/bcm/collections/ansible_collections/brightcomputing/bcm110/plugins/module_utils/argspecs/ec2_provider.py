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

class EC2Provider_ArgSpec:
    argument_spec = {'APIRegionName': {'type': 'str'},
                     'JobAccountTagName': {'default': 'BCM_JOB_ACCOUNT', 'type': 'str'},
                     'JobIdTagName': {'default': 'BCM_JOB_ID', 'type': 'str'},
                     'JobNameTagName': {'default': 'BCM_JOB_NAME', 'type': 'str'},
                     'JobUserTagName': {'default': 'BCM_JOB_USER', 'type': 'str'},
                     'VPCs': {'elements': 'dict',
                              'options': {'baseAddress': {'default': '10.0.0.0', 'type': 'str'},
                                          'defaultImageId': {'type': 'str'},
                                          'enforceDirectorIP': {'default': '0.0.0.0',
                                                                'type': 'str'},
                                          'extra_values': {'type': 'json'},
                                          'internetGatewayID': {'type': 'str'},
                                          'name': {'required': True, 'type': 'str'},
                                          'netmaskBits': {'default': 16, 'type': 'int'},
                                          'privateACL': {'type': 'str'},
                                          'publicACL': {'type': 'str'},
                                          'region': {'type': 'str'},
                                          'routeTableIdPrivate': {'type': 'str'},
                                          'routeTableIdPublic': {'type': 'str'},
                                          'securityGroupDirector': {'type': 'str'},
                                          'securityGroupNode': {'type': 'str'},
                                          'setDirectorAsDefaultGateway': {'default': True,
                                                                          'type': 'bool'},
                                          'subnets': {'type': 'list'},
                                          'useInternalIPForDirectorIP': {'default': False,
                                                                         'type': 'bool'},
                                          'vpcID': {'type': 'str'}},
                              'type': 'list'},
                     'accessKeyId': {'type': 'str'},
                     'accessKeySecret': {'type': 'str'},
                     'addJobBasedTag': {'default': False, 'type': 'bool'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'defaultDirectorType': {'type': 'str'},
                     'defaultRegion': {'type': 'str'},
                     'defaultType': {'type': 'str'},
                     'iamRoleName': {'type': 'str'},
                     'imageOwners': {'default': ['137677339600', '197943594779'], 'type': 'list'},
                     'marketplaceUsePolicy': {'choices': ['ALWAYS', 'NEVER', 'AS_NEEDED'],
                                              'default': 'NEVER',
                                              'type': 'str'},
                     'name': {'required': True, 'type': 'str'},
                     'regions': {'type': 'list'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'tags': {'type': 'list'}}