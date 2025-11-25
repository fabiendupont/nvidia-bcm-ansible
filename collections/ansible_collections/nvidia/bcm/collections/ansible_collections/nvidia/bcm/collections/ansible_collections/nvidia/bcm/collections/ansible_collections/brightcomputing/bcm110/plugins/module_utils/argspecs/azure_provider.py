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

class AzureProvider_ArgSpec:
    argument_spec = {'clientId': {'type': 'str'},
                     'clientSecret': {'type': 'str'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'cloudName': {'default': 'AzureCloud', 'type': 'str'},
                     'defaultDirectorVMSize': {'type': 'str'},
                     'defaultHyperVGeneration': {'choices': ['V1', 'V2'],
                                                 'default': 'V1',
                                                 'type': 'str'},
                     'defaultLocation': {'type': 'str'},
                     'defaultNodeInstallerImage': {'type': 'str'},
                     'defaultVMSize': {'type': 'str'},
                     'extensions': {'elements': 'dict',
                                    'options': {'extraField': {'type': 'list'},
                                                'location': {'type': 'str'},
                                                'name': {'required': True, 'type': 'str'},
                                                'network': {'type': 'str'},
                                                'resourceGroup': {'type': 'str'}},
                                    'type': 'list'},
                     'freeImageType': {'choices': ['VHD', 'MARKETPLACE'],
                                       'default': 'MARKETPLACE',
                                       'type': 'str'},
                     'marketplaceUsePolicy': {'choices': ['ALWAYS', 'NEVER', 'AS_NEEDED'],
                                              'default': 'NEVER',
                                              'type': 'str'},
                     'name': {'required': True, 'type': 'str'},
                     'regions': {'type': 'list'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'subscriptionId': {'type': 'str'},
                     'tags': {'type': 'list'},
                     'tenantId': {'type': 'str'}}