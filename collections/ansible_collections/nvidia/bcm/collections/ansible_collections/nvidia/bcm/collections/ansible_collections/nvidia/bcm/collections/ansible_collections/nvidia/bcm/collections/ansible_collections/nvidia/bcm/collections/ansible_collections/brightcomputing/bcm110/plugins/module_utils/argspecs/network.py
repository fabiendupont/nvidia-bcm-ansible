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

class Network_ArgSpec:
    argument_spec = {'EC2AvailabilityZone': {'type': 'str'},
                     'IPv6': {'default': False, 'type': 'bool'},
                     'allowAutosign': {'choices': ['AUTOMATIC', 'ALWAYS', 'NEVER', 'SECRET'],
                                       'default': 'AUTOMATIC',
                                       'type': 'str'},
                     'baseAddress': {'default': '0.0.0.0', 'type': 'str'},
                     'bootable': {'default': False, 'type': 'bool'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'cloudSubnetID': {'type': 'str'},
                     'disableAutomaticExports': {'default': False, 'type': 'bool'},
                     'domainName': {'type': 'str'},
                     'dynamicRangeEnd': {'default': '0.0.0.0', 'type': 'str'},
                     'dynamicRangeStart': {'default': '0.0.0.0', 'type': 'str'},
                     'excludeFromSearchDomain': {'default': False, 'type': 'bool'},
                     'extra_values': {'type': 'json'},
                     'gateway': {'default': '0.0.0.0', 'type': 'str'},
                     'gatewayMetric': {'default': 0, 'type': 'int'},
                     'generateDNSZone': {'choices': ['BOTH', 'FORWARD', 'REVERSE', 'NEITHER'],
                                         'default': 'BOTH',
                                         'type': 'str'},
                     'ipv6BaseAddress': {'default': '::0', 'type': 'str'},
                     'ipv6Gateway': {'default': '::0', 'type': 'str'},
                     'ipv6NetmaskBits': {'default': 0, 'type': 'int'},
                     'layer3': {'default': False, 'type': 'bool'},
                     'layer3ecmp': {'default': False, 'type': 'bool'},
                     'layer3route': {'choices': ['NONE', 'STATIC', 'DEFAULT'],
                                     'default': 'NONE',
                                     'type': 'str'},
                     'layer3splitStaticRoute': {'default': False, 'type': 'bool'},
                     'lockDownDhcpd': {'default': False, 'type': 'bool'},
                     'management': {'default': False, 'type': 'bool'},
                     'mtu': {'default': 1500, 'type': 'int'},
                     'name': {'required': True, 'type': 'str'},
                     'netmaskBits': {'default': 16, 'type': 'int'},
                     'notes': {'type': 'str'},
                     'searchDomainIndex': {'default': 0, 'type': 'int'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'},
                     'type': {'choices': ['INTERNAL',
                                          'EXTERNAL',
                                          'TUNNEL',
                                          'GLOBAL',
                                          'CLOUD',
                                          'NETMAP',
                                          'EDGE_INTERNAL',
                                          'EDGE_EXTERNAL'],
                              'default': 'INTERNAL',
                              'type': 'str'}}