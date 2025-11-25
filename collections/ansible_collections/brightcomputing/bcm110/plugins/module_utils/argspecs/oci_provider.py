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

class OCIProvider_ArgSpec:
    argument_spec = {'APIRegionName': {'type': 'str'},
                     'authFingerprint': {'type': 'str'},
                     'authKeyContent': {'type': 'str'},
                     'authTenancy': {'type': 'str'},
                     'authUser': {'type': 'str'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'computeClusterID': {'type': 'str'},
                     'defaultAvailabilityDomain': {'type': 'str'},
                     'defaultCompartmentId': {'type': 'str'},
                     'defaultNodeInstallerImageId': {'type': 'str'},
                     'defaultRegion': {'type': 'str'},
                     'defaultShape': {'type': 'str'},
                     'definedTags': {'type': 'list'},
                     'imagesCompartmentId': {'type': 'str'},
                     'imagesManifestBaseURL': {'type': 'str'},
                     'name': {'required': True, 'type': 'str'},
                     'regions': {'type': 'list'},
                     'securityGroupNode': {'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'tags': {'type': 'list'}}