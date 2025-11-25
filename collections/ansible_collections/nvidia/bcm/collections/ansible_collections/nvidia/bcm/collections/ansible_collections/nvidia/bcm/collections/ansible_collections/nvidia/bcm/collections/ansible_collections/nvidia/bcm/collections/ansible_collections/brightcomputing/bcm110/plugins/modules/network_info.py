#!/cm/local/apps/python3/bin/python
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

from __future__ import annotations


############################
# Docs
############################
DOCUMENTATION = r"""
---
module: network_info
description: Query cmdaemon for entity of type Network
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
network:
  type: list
  description: Network
  returned: success
  contains:
    uuid:
      type: str
      description: ''
      returned: success
    baseType:
      type: str
      description: ''
      returned: success
    childType:
      type: str
      description: ''
      returned: success
    revision:
      type: str
      description: ''
      returned: success
    modified:
      type: bool
      description: ''
      returned: success
    is_committed:
      type: bool
      description: ''
      returned: success
    to_be_removed:
      type: bool
      description: ''
      returned: success
    extra_values:
      type: json
      description: ''
      returned: success
    name:
      type: str
      description: Name
      returned: success
    IPv6:
      type: bool
      description: IPv6 enabled
      returned: success
    ipv6NetmaskBits:
      type: int
      description: Netmask or Classless Inter-Domain Routing for IPv6
      returned: success
    netmaskBits:
      type: int
      description: Netmask or Classless Inter-Domain Routing
      returned: success
    ipv6BaseAddress:
      type: str
      description: Base IP address for Ipv6
      returned: success
    baseAddress:
      type: str
      description: Base IP address
      returned: success
    domainName:
      type: str
      description: Domain name
      returned: success
    type:
      type: str
      description: 'Type of network, internal: local cluster network, external: connection
        to outside world, global: unique network accros the cloud, tunnel: cloud network,
        netmap: virtual network user by cloud nodes to connect to nodes inside the
        cluster'
      returned: success
    mtu:
      type: int
      description: The maximum transmission unit.
      returned: success
    bootable:
      type: bool
      description: If set compute nodes can boot using this network
      returned: success
    dynamicRangeStart:
      type: str
      description: First IP address in the networks dynamic range
      returned: success
    dynamicRangeEnd:
      type: str
      description: Last IP address in the networks dynamic range
      returned: success
    lockDownDhcpd:
      type: bool
      description: Don't respond to dhcp request of new nodes via this network
      returned: success
    management:
      type: bool
      description: If set, the network can be used as a management network
      returned: success
    gateway:
      type: str
      description: Gateway
      returned: success
    gatewayMetric:
      type: int
      description: Gateway metric
      returned: success
    ipv6Gateway:
      type: str
      description: IPv6 Gateway
      returned: success
    layer3:
      type: bool
      description: Create a network routed on layer3 with /31 netmask
      returned: success
    layer3route:
      type: str
      description: Layer3 routing
      returned: success
    layer3ecmp:
      type: bool
      description: Create a layer3 network with equal-cost multi-path
      returned: success
    layer3splitStaticRoute:
      type: bool
      description: Create a layer3 network with equal-cost multi-path
      returned: success
    notes:
      type: str
      description: Administrator notes
      returned: success
    cloudSubnetID:
      type: str
      description: The Cloud ID of the subnet
      returned: success
    EC2AvailabilityZone:
      type: str
      description: The AWS availability zone inside which the subnet exists
      returned: success
    allowAutosign:
      type: str
      description: Specify if certificate request from node installers can be signed
        automatically
      returned: success
    generateDNSZone:
      type: str
      description: Specify which DNS zones should be written
      returned: success
    excludeFromSearchDomain:
      type: bool
      description: Exlude from search domain in /etc/resolv.conf file
      returned: success
    searchDomainIndex:
      type: int
      description: Search domain index in /etc/resolv.conf file, set to 0 for automatic
      returned: success
    disableAutomaticExports:
      type: bool
      description: Disable creation of automatic filesystem exports
      returned: success

"""
############################
# Imports
############################

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import Network
    from pythoncm.entity_to_json_encoder import EntityToJSONEncoder
except ImportError:
    HAS_PYTHONCM = False
    PYTHONCM_IMP_ERR = traceback.format_exc()
else:
    HAS_PYTHONCM = True
    PYTHONCM_IMP_ERR = None


from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.core import EntityQuery
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.utils import entity_to_dict

############################
# main
############################


def main():

    module = AnsibleModule(
        argument_spec={'format': {'choices': ['list', 'dict'], 'default': 'list', 'type': 'str'}, 'depth': {'default': 3, 'type': 'int'}, 'include_id': {'default': False, 'type': 'bool'}, 'for_update': {'default': False, 'type': 'bool'}},
        supports_check_mode=True,
    )

    if not HAS_PYTHONCM:
        module.fail_json(msg=missing_required_lib("cmdaemon-pythoncm"), exception=PYTHONCM_IMP_ERR)

    cluster = Cluster()  # TODO make this configurable

    entity_query = EntityQuery(cluster)

    results = entity_query.find(Network)

    format = module.params["format"]

    depth = module.params["depth"]

    include_id = module.params["include_id"]

    for_update = module.params["for_update"]

    if format == "list":
        json_ready_result = [
            entity_to_dict(
                entity,
                depth=depth,
                for_update=for_update,
                include_id=include_id,
            )
            for entity in results
        ] if results else []

    if format == "dict":
        json_ready_result = {
            entity.resolve_name: entity_to_dict(
                entity,
                depth=depth,
                for_update=for_update,
                include_id=include_id,
            )
            for entity in results
        } if results else {}

    cluster.disconnect()

    json_ready_result = json.loads(json.dumps(json_ready_result, cls=EntityToJSONEncoder))

    module.exit_json(networks=json_ready_result, changed=False)


if __name__ == '__main__':
    main()