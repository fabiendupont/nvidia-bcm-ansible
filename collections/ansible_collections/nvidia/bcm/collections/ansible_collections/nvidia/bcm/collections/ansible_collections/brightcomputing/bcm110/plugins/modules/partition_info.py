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
module: partition_info
description: Query cmdaemon for entity of type Partition
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
partition:
  type: list
  description: Partition
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
      description: Partition name
      returned: success
    clusterName:
      type: str
      description: Cluster name
      returned: success
    clusterReferenceArchitecture:
      type: str
      description: Description of the cluster architecture
      returned: success
    primaryHeadNode:
      type: complex
      description: Primary head node
      returned: success
    failover:
      type: complex
      description: Manage failover setup for this cluster
      returned: success
    timeZoneSettings:
      type: complex
      description: Time zone
      returned: success
    adminEmail:
      type: str
      description: Administrator email
      returned: success
    slaveName:
      type: str
      description: Default prefix to identify nodes. eg node003 (basename = node)
      returned: success
    slaveDigits:
      type: int
      description: Number of digits used to identify nodes. eg node003 (digits = 3)
      returned: success
    nameServers:
      type: str
      description: Name servers
      returned: success
    nameServersFromDhcp:
      type: str
      description: Name servers provided by DHCP, edit the name servers property instead
      returned: success
    timeServers:
      type: str
      description: NTP time servers
      returned: success
    searchDomains:
      type: str
      description: DNS search domains
      returned: success
    externallyVisibleIp:
      type: str
      description: IP that external sites see when headnode connects
      returned: success
    externalNetwork:
      type: complex
      description: The external network
      returned: success
    defaultCategory:
      type: complex
      description: Default category for new nodes
      returned: success
    archOS:
      type: list
      description: Architecture operating system
      returned: success
    burnConfigs:
      type: list
      description: Available burn configurations
      returned: success
    failoverGroups:
      type: list
      description: Failover group configurations
      returned: success
    resourcePools:
      type: list
      description: Resource pools
      returned: success
    defaultBurnConfig:
      type: complex
      description: Default burn configuration
      returned: success
    bmcSettings:
      type: complex
      description: Configure the baseboard management controller settings
      returned: success
    snmpSettings:
      type: complex
      description: Configure the cluster wide SNMP settings
      returned: success
    dpuSettings:
      type: complex
      description: Configure the DPU settings
      returned: success
    ztpSettings:
      type: complex
      description: Configure the ZTP settings
      returned: success
    ztpNewSwitchSettings:
      type: complex
      description: Configure the ZTP settings
      returned: success
    seLinuxSettings:
      type: complex
      description: Configure the SELinux settings
      returned: success
    accessSettings:
      type: complex
      description: Configure the cluster wide Access settings
      returned: success
    netQSettings:
      type: complex
      description: Configure NetQ settings
      returned: success
    ufmSettings:
      type: complex
      description: Configure UFM settings
      returned: success
    nmxmSettings:
      type: complex
      description: Configure NMX Manager settings
      returned: success
    managementNetwork:
      type: complex
      description: Determines what network should be used for management traffic.
      returned: success
    notes:
      type: str
      description: Administrator notes
      returned: success
    provisioningSettings:
      type: complex
      description: Configure the provisioning settings
      returned: success
    relayHost:
      type: str
      description: SMTP mail relay host
      returned: success
    noZeroConf:
      type: bool
      description: Add nozeroconf to network configuration
      returned: success
    proxySettings:
      type: complex
      description: Configure the proxy server settings
      returned: success
    wlmJobPowerUsageSettings:
      type: complex
      description: Configure the Wlm job power usage settings
      returned: success
    leakActionPolicies:
      type: list
      description: Leak action policies
      returned: success
    activeLeakActionPolicy:
      type: complex
      description: Active leak action policy
      returned: success
    autosign:
      type: str
      description: Sign certificates for node installer request according to network
        settings.
      returned: success
    bms:
      type: str
      description: Specify the type of BMS
      returned: success
    bmsPath:
      type: str
      description: The path/url used to push information to BMS
      returned: success
    bmsCertificate:
      type: str
      description: The certificate used to push information to BMS url
      returned: success
    bmsPrivateKey:
      type: str
      description: The private key used to push information to BMS url
      returned: success
    prometheusMetricForwarders:
      type: list
      description: Prometheus metric forwarders
      returned: success

"""
############################
# Imports
############################

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import Partition
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

    results = entity_query.find(Partition)

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

    module.exit_json(partitions=json_ready_result, changed=False)


if __name__ == '__main__':
    main()