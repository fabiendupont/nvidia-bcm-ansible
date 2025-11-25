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

class ChargeBackRequest_ArgSpec:
    argument_spec = {'accountingInfo': {'type': 'json'},
                     'accounts': {'type': 'list'},
                     'calculatePrediction': {'default': False, 'type': 'bool'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'currency': {'default': '$', 'type': 'str'},
                     'endTime': {'default': 'now/M', 'type': 'str'},
                     'groupByAccount': {'default': False, 'type': 'bool'},
                     'groupByAccountingInfo': {'type': 'list'},
                     'groupByGroup': {'default': False, 'type': 'bool'},
                     'groupByJobId': {'default': False, 'type': 'bool'},
                     'groupByJobName': {'default': False, 'type': 'bool'},
                     'groupByUser': {'default': False, 'type': 'bool'},
                     'groups': {'type': 'list'},
                     'includeRunning': {'default': False, 'type': 'bool'},
                     'jobIds': {'type': 'list'},
                     'jobNames': {'type': 'list'},
                     'name': {'required': True, 'type': 'str'},
                     'notes': {'type': 'str'},
                     'preference': {'default': 0, 'type': 'int'},
                     'pricePerCPUCoreSecond': {'default': 0.0, 'type': 'float'},
                     'pricePerCPUSecond': {'default': 0.0, 'type': 'float'},
                     'pricePerGPUSecond': {'default': 0.0, 'type': 'float'},
                     'pricePerMemoryByteSecond': {'default': 0.0, 'type': 'float'},
                     'pricePerSlotSecond': {'default': 0.0, 'type': 'float'},
                     'pricePerWattSecond': {'default': 0.0, 'type': 'float'},
                     'startTime': {'default': 'now/M', 'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'users': {'type': 'list'},
                     'utc': {'default': False, 'type': 'bool'},
                     'wlmClusters': {'type': 'list'}}