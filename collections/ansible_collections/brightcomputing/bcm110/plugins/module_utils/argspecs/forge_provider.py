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

class ForgeProvider_ArgSpec:
    argument_spec = {'authApiKey': {'type': 'str'},
                     'authOrganizationId': {'type': 'str'},
                     'authSiteId': {'type': 'str'},
                     'authTenantId': {'type': 'str'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'consoleKeyGroupId': {'type': 'str'},
                     'defaultInstanceType': {'type': 'str'},
                     'name': {'required': True, 'type': 'str'},
                     'ngcApiUrl': {'type': 'str'},
                     'ngcAuthScope': {'choices': ['NGC', 'NGC_STG', 'NONE'],
                                      'default': 'NONE',
                                      'type': 'str'},
                     'ngcAuthUrl': {'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'tags': {'type': 'list'},
                     'vpcId': {'type': 'str'}}