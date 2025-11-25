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

class OSCloudProvider_ArgSpec:
    argument_spec = {'authUrl': {'type': 'str'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'cloudApiType': {'default': 'rackspace', 'type': 'str'},
                     'defaultDirectorFlavor': {'type': 'str'},
                     'defaultFlavor': {'type': 'str'},
                     'defaultImage': {'type': 'str'},
                     'defaultRegion': {'type': 'str'},
                     'extensions': {'elements': 'dict',
                                    'options': {'defaultCnodeSecGroupId': {'type': 'str'},
                                                'defaultDirectorSecGroupId': {'type': 'str'},
                                                'extraField': {'type': 'list'},
                                                'floatingIpNetworkId': {'type': 'str'},
                                                'name': {'required': True, 'type': 'str'},
                                                'network': {'type': 'str'},
                                                'region': {'type': 'str'},
                                                'stackId': {'type': 'str'}},
                                    'type': 'list'},
                     'keyPairName': {'type': 'str'},
                     'name': {'required': True, 'type': 'str'},
                     'openStackVersion': {'type': 'str'},
                     'openStackVersionName': {'type': 'str'},
                     'password': {'no_log': True, 'type': 'str'},
                     'projectDomainId': {'type': 'str'},
                     'projectId': {'type': 'str'},
                     'projectName': {'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'tags': {'type': 'list'},
                     'userDomainId': {'type': 'str'},
                     'username': {'type': 'str'}}