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

class BeeGFSCluster_ArgSpec:
    argument_spec = {'authFile': {'type': 'str'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'mountpoint': {'default': '/mnt/beegfs', 'type': 'str'},
                     'multiMode': {'default': True, 'type': 'bool'},
                     'name': {'required': True, 'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'}}