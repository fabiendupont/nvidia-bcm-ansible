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
module: network
description: ['Network']
options:
    state:
      type: str
      choices:
      - present
      - absent
      default: present
      description:
      - The state the resource should have
    cloneFrom:
      type: str
      default: ''
      description:
      - The id or name of the entity that the new entity will be cloned from.
      - ' (take effect only at entity creation)'
    name:
      description:
      - Name
      type: str
      required: true
    IPv6:
      description:
      - IPv6 enabled
      type: bool
      required: false
      default: false
    ipv6NetmaskBits:
      description:
      - Netmask or Classless Inter-Domain Routing for IPv6
      type: int
      required: false
      default: 0
    netmaskBits:
      description:
      - Netmask or Classless Inter-Domain Routing
      type: int
      required: false
      default: 16
    ipv6BaseAddress:
      description:
      - Base IP address for Ipv6
      type: str
      required: false
      default: ::0
    baseAddress:
      description:
      - Base IP address
      type: str
      required: false
      default: 0.0.0.0
    domainName:
      description:
      - Domain name
      type: str
      required: false
    type:
      description:
      - 'Type of network, internal: local cluster network, external: connection to outside
        world, global: unique network accros the cloud, tunnel: cloud network, netmap:
        virtual network user by cloud nodes to connect to nodes inside the cluster'
      type: str
      required: false
      default: INTERNAL
      choices:
      - INTERNAL
      - EXTERNAL
      - TUNNEL
      - GLOBAL
      - CLOUD
      - NETMAP
      - EDGE_INTERNAL
      - EDGE_EXTERNAL
    mtu:
      description:
      - The maximum transmission unit.
      type: int
      required: false
      default: 1500
    bootable:
      description:
      - If set compute nodes can boot using this network
      type: bool
      required: false
      default: false
    dynamicRangeStart:
      description:
      - First IP address in the networks dynamic range
      type: str
      required: false
      default: 0.0.0.0
    dynamicRangeEnd:
      description:
      - Last IP address in the networks dynamic range
      type: str
      required: false
      default: 0.0.0.0
    lockDownDhcpd:
      description:
      - Don't respond to dhcp request of new nodes via this network
      type: bool
      required: false
      default: false
    management:
      description:
      - If set, the network can be used as a management network
      type: bool
      required: false
      default: false
    gateway:
      description:
      - Gateway
      type: str
      required: false
      default: 0.0.0.0
    gatewayMetric:
      description:
      - Gateway metric
      type: int
      required: false
      default: 0
    ipv6Gateway:
      description:
      - IPv6 Gateway
      type: str
      required: false
      default: ::0
    layer3:
      description:
      - Create a network routed on layer3 with /31 netmask
      type: bool
      required: false
      default: false
    layer3route:
      description:
      - Layer3 routing
      type: str
      required: false
      default: NONE
      choices:
      - NONE
      - STATIC
      - DEFAULT
    layer3ecmp:
      description:
      - Create a layer3 network with equal-cost multi-path
      type: bool
      required: false
      default: false
    layer3splitStaticRoute:
      description:
      - Create a layer3 network with equal-cost multi-path
      type: bool
      required: false
      default: false
    notes:
      description:
      - Administrator notes
      type: str
      required: false
    cloudSubnetID:
      description:
      - The Cloud ID of the subnet
      type: str
      required: false
    EC2AvailabilityZone:
      description:
      - The AWS availability zone inside which the subnet exists
      type: str
      required: false
    allowAutosign:
      description:
      - Specify if certificate request from node installers can be signed automatically
      type: str
      required: false
      default: AUTOMATIC
      choices:
      - AUTOMATIC
      - ALWAYS
      - NEVER
      - SECRET
    generateDNSZone:
      description:
      - Specify which DNS zones should be written
      type: str
      required: false
      default: BOTH
      choices:
      - BOTH
      - FORWARD
      - REVERSE
      - NEITHER
    excludeFromSearchDomain:
      description:
      - Exlude from search domain in /etc/resolv.conf file
      type: bool
      required: false
      default: false
    searchDomainIndex:
      description:
      - Search domain index in /etc/resolv.conf file, set to 0 for automatic
      type: int
      required: false
      default: 0
    disableAutomaticExports:
      description:
      - Disable creation of automatic filesystem exports
      type: bool
      required: false
      default: false
    extra_values:
      description: []
      type: json
      required: false

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
network:
  type: complex
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

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import Network
except ImportError:
    HAS_PYTHONCM = False
    PYTHONCM_IMP_ERR = traceback.format_exc()
else:
    HAS_PYTHONCM = True
    PYTHONCM_IMP_ERR = None

try:
    import deepdiff
except ImportError:
    HAS_DEEPDIFF = False
    DEEPDIFF_IMP_ERR = traceback.format_exc()
else:
    HAS_DEEPDIFF = True
    DEEPDIFF_IMP_ERR = None

try:
    from box import Box
except ImportError:
    HAS_BOX = False
    BOX_IMP_ERR = traceback.format_exc()
else:
    HAS_BOX = True
    BOX_IMP_ERR = None

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.base_module import BaseModule
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.core import EntityManager
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.utils import json_encode_entity
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.network import Network_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=Network_ArgSpec.argument_spec,
        supports_check_mode=True,
    )

    if not HAS_PYTHONCM:
        module.fail_json(msg=missing_required_lib("cmdaemon-pythoncm"), exception=PYTHONCM_IMP_ERR)

    if not HAS_DEEPDIFF:
        module.fail_json(msg=missing_required_lib("deepdiff"), exception=DEEPDIFF_IMP_ERR)

    if not HAS_BOX:
        module.fail_json(msg=missing_required_lib("python-box"), exception=BOX_IMP_ERR)

    params =  module.bright_params

    cluster = Cluster()  # TODO make this configurable

    entity_manager = EntityManager(cluster, module.log)

    entity = entity_manager.lookup_entity(params, Network)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(Network, params, commit=not module.check_mode)
            changed = True
    else:

        if desired_state == "present":
            diff = entity_manager.check_diff(entity, params)
            if diff:
                entity, res = entity_manager.update_resource(entity, params, commit=not module.check_mode)
                changed = True

        if desired_state == "absent":
            entity, res = entity_manager.delete_resource(entity, params, commit=not module.check_mode)
            changed = True

    entity_as_dict = json_encode_entity(entity)

    cluster.disconnect()

    if not changed:
        module.exit_json(changed=changed, **entity_as_dict)

    if res.good:
        module.exit_json(changed=changed, diff=diff, **entity_as_dict)
    else:
        if hasattr(res, 'validation'):
            msg = "|".join(it.message for it in res.validation)
        else:
            msg = "Operation failed."
        module.fail_json(msg=msg, **entity_as_dict)


if __name__ == '__main__':
    main()