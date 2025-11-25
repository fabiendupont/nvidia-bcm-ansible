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

class GCPProvider_ArgSpec:
    argument_spec = {'cloneFrom': {'default': '', 'type': 'str'},
                     'defaultBootDiskType': {'type': 'str'},
                     'defaultBootImageURI': {'type': 'str'},
                     'defaultMachineType': {'type': 'str'},
                     'defaultMaintenancePolicy': {'type': 'str'},
                     'defaultProvisioningModel': {'type': 'str'},
                     'defaultReservationName': {'type': 'str'},
                     'defaultReservationType': {'type': 'str'},
                     'defaultResourcePolicies': {'type': 'list'},
                     'defaultServiceAccount': {'type': 'str'},
                     'defaultZone': {'type': 'str'},
                     'imageStorageLocation': {'type': 'str'},
                     'name': {'required': True, 'type': 'str'},
                     'projectId': {'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'tags': {'type': 'list'}}