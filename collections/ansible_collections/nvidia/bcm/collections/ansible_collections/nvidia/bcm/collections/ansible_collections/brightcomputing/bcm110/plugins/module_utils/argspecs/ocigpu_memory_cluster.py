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

class OCIGPUMemoryCluster_ArgSpec:
    argument_spec = {'cloneFrom': {'default': '', 'type': 'str'},
                     'gpuMemoryFabricId': {'type': 'str'},
                     'id': {'type': 'str'},
                     'name': {'required': True, 'type': 'str'},
                     'provider': {'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'}}