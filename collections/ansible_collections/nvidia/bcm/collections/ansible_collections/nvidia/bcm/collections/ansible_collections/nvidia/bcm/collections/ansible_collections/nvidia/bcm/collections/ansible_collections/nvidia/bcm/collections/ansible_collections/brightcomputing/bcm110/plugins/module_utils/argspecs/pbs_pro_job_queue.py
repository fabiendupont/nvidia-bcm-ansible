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

class PbsProJobQueue_ArgSpec:
    argument_spec = {'aclHostEnable': {'default': False, 'type': 'bool'},
                     'categories': {'type': 'list'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'computeNodes': {'type': 'list'},
                     'defaultQueue': {'default': False, 'type': 'bool'},
                     'defaultWalltime': {'type': 'str'},
                     'enabled': {'default': True, 'type': 'bool'},
                     'fromRouteOnly': {'default': False, 'type': 'bool'},
                     'maxQueued': {'default': 0, 'type': 'int'},
                     'maxRunning': {'default': 0, 'type': 'int'},
                     'maxWalltime': {'default': '240:00:00', 'type': 'str'},
                     'minWalltime': {'default': '00:00:00', 'type': 'str'},
                     'name': {'required': True, 'type': 'str'},
                     'nodegroups': {'type': 'list'},
                     'options': {'type': 'list'},
                     'overlays': {'type': 'list'},
                     'priority': {'default': 0, 'type': 'int'},
                     'queueType': {'choices': ['EXECUTION', 'ROUTE'],
                                   'default': 'EXECUTION',
                                   'type': 'str'},
                     'routeHeldJobs': {'default': False, 'type': 'bool'},
                     'routeLifetime': {'default': 0, 'type': 'int'},
                     'routeRetryTime': {'default': 0, 'type': 'int'},
                     'routeWaitingJobs': {'default': False, 'type': 'bool'},
                     'routes': {'type': 'list'},
                     'started': {'default': True, 'type': 'bool'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'wlmCluster': {'type': 'str'}}