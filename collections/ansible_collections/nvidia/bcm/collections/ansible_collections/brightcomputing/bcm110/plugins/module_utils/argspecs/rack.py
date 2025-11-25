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

class Rack_ArgSpec:
    argument_spec = {'angle': {'default': 0, 'type': 'int'},
                     'building': {'type': 'str'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'depth': {'default': 34, 'type': 'int'},
                     'height': {'default': 42, 'type': 'int'},
                     'inverted': {'default': False, 'type': 'bool'},
                     'location': {'type': 'str'},
                     'model': {'type': 'str'},
                     'name': {'required': True, 'type': 'str'},
                     'notes': {'type': 'str'},
                     'partNumber': {'type': 'str'},
                     'room': {'type': 'str'},
                     'row': {'type': 'str'},
                     'serialNumber': {'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'twin': {'type': 'str'},
                     'type': {'type': 'str'},
                     'width': {'default': 19, 'type': 'int'},
                     'xCoordinate': {'default': 0, 'type': 'int'},
                     'yCoordinate': {'default': 0, 'type': 'int'}}