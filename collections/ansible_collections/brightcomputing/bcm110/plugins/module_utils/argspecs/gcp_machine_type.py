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

class GCPMachineType_ArgSpec:
    argument_spec = {'architecture': {'type': 'str'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'cpu': {'type': 'str'},
                     'description': {'type': 'str'},
                     'disks': {'type': 'str'},
                     'gpu': {'type': 'str'},
                     'isSharedCPU': {'default': False, 'type': 'bool'},
                     'maximumPersistentDisksSizeGb': {'default': 0, 'type': 'int'},
                     'memory': {'type': 'str'},
                     'name': {'required': True, 'type': 'str'},
                     'provider': {'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'}}