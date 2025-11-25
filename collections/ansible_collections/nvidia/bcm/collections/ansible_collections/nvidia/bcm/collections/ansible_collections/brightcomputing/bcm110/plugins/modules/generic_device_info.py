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
module: generic_device_info
description: Query cmdaemon for entity of type GenericDevice
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
generic_device:
  type: list
  description: ''
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
    hostname:
      type: str
      description: Hostname
      returned: success
    mac:
      type: str
      description: MAC address
      returned: success
    defaultGateway:
      type: str
      description: Default gateway for the device
      returned: success
    defaultGatewayMetric:
      type: int
      description: Default gateway metric
      returned: success
    creationTime:
      type: int
      description: Date on which node was defined
      returned: success
    partition:
      type: complex
      description: Partition to which this device belongs
      returned: success
    switchPorts:
      type: list
      description: Switch ports
      returned: success
    powerDistributionUnits:
      type: list
      description: List of outlets on powerdistributionunits
      returned: success
    rackPosition:
      type: complex
      description: Name of the rack in which the device resides
      returned: success
    chassisPosition:
      type: complex
      description: Chassis position in which the device resides
      returned: success
    accessSettings:
      type: complex
      description: Configure the cluster wide Access settings
      returned: success
    bmcSettings:
      type: complex
      description: Configure the baseboard management controller settings
      returned: success
    powerControl:
      type: str
      description: 'Specifies which type of power control feature is being used (values:
        none, apc, custom, cloud, ipmi0, ilo0, drac0, rf0, cimc0 or rshim0)'
      returned: success
    customPowerScript:
      type: str
      description: Script that will be used to perform power on/off/reset/status operations
      returned: success
    customPowerScriptArgument:
      type: str
      description: Argument for the custom power script
      returned: success
    customPingScript:
      type: str
      description: Script that will be used to ping a device
      returned: success
    customPingScriptArgument:
      type: str
      description: Argument for the custom ping script
      returned: success
    notes:
      type: str
      description: Administrator notes
      returned: success
    interfaces:
      type: list
      description: IP on the management network
      returned: success
    provisioningInterface:
      type: complex
      description: Network interface on which the node will receive software image
        updates
      returned: success
    managementNetwork:
      type: complex
      description: Determines what network should be used for management traffic.
        If not set, category or partition setting is used.
      returned: success
    userdefined1:
      type: str
      description: A free text field passed to custom scripts
      returned: success
    userdefined2:
      type: str
      description: A free text field passed to custom scripts
      returned: success
    userDefinedResources:
      type: str
      description: User defined resources used to filter monitoring data producers
      returned: success
    supportsGNSS:
      type: bool
      description: Supports GNSS location
      returned: success
    partNumber:
      type: str
      description: Part number
      returned: success
    serialNumber:
      type: str
      description: Serial number
      returned: success
    prometheusMetricForwarders:
      type: list
      description: Prometheus metric forwarders
      returned: success
    model:
      type: str
      description: Device model name
      returned: success

"""
############################
# Imports
############################

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import GenericDevice
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

    results = entity_query.find(GenericDevice)

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

    module.exit_json(generic_devices=json_ready_result, changed=False)


if __name__ == '__main__':
    main()