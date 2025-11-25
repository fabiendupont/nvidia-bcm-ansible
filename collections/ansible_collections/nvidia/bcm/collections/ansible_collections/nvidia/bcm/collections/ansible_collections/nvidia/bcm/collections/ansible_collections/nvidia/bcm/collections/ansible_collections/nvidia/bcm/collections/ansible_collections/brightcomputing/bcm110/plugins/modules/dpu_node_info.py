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
module: dpu_node_info
description: Query cmdaemon for entity of type DPUNode
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
dpu_node:
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
    cmdaemonUrl:
      type: str
      description: ''
      returned: success
    fsmounts:
      type: list
      description: Configure the entries placed in /etc/fstab
      returned: success
    fsexports:
      type: list
      description: Configure the entries placed in /etc/exports
      returned: success
    staticRoutes:
      type: list
      description: Configure static routes for the interfaces
      returned: success
    roles:
      type: list
      description: Assign the roles the node should play
      returned: success
    services:
      type: list
      description: Manage operating system services
      returned: success
    pxelabel:
      type: str
      description: PXE Label to be displayed when this node boots
      returned: success
    customRemoteConsoleScript:
      type: str
      description: Script that will be used to remote console a device
      returned: success
    customRemoteConsoleScriptArgument:
      type: str
      description: Argument for the custom remote console script
      returned: success
    provisioningTransport:
      type: str
      description: Defines what transport protocol should be used for provisioning.
        Options are RSYNCSSH or RSYNCDAEMON. The latter is the default, is a bit less
        secure but faster.
      returned: success
    gpuSettings:
      type: list
      description: Configure the GPUs
      returned: success
    excludeListManipulateScript:
      type: str
      description: A user defined script that can be used to do custom last minute
        changes to the exclude lists used by cmdaemon to rsync
      returned: success
    ioScheduler:
      type: str
      description: The I/O scheduler for the disks
      returned: success
    useExclusivelyFor:
      type: str
      description: 'Use node exclusively for desired function: stop all other services'
      returned: success
    seLinuxSettings:
      type: complex
      description: Configure the SELinux settings
      returned: success
    proxySettings:
      type: complex
      description: Configure the proxy server settings
      returned: success
    versionConfigFiles:
      type: bool
      description: Keep old versions of all config files for this node
      returned: success
    forceFullEnvironment:
      type: bool
      description: Force this node to create the environment for all nodes
      returned: success
    authenticationService:
      type: str
      description: Authentication service
      returned: success
    biosSetup:
      type: json
      description: BIOS setup
      returned: success
    timeZoneSettings:
      type: complex
      description: Time zone
      returned: success
    installMode:
      type: str
      description: Installmode to be used by default, if empty use category installMode
      returned: success
    nextBootInstallMode:
      type: str
      description: Installmode to be used during the next boot, will be cleared during
        boot
      returned: success
    blockDevicesClearedOnNextBoot:
      type: str
      description: List of block devices that will be cleared during the next boot
      returned: success
    initialize:
      type: str
      description: Node specific initialize script
      returned: success
    finalize:
      type: str
      description: Node specific finalize script
      returned: success
    raidconf:
      type: str
      description: Node specific Hardware RAID configuration
      returned: success
    category:
      type: complex
      description: Category to which this node belongs
      returned: success
    disksetup:
      type: str
      description: Node specific disk setup
      returned: success
    excludeListFull:
      type: str
      description: Exclude list for full install
      returned: success
    excludeListSync:
      type: str
      description: Exclude list for sync install
      returned: success
    excludeListUpdate:
      type: str
      description: Exclude list for update
      returned: success
    excludeListGrab:
      type: str
      description: Exclude list for grabbing to an existing image
      returned: success
    excludeListGrabnew:
      type: str
      description: Exclude list for grabbing to a new image
      returned: success
    nodeInstallerDisk:
      type: bool
      description: The node has its own node installer disk
      returned: success
    installBootRecord:
      type: bool
      description: Install boot record on local disk
      returned: success
    dataNode:
      type: bool
      description: If enabled the node will never do a FULL install without explicit
        user confirmation
      returned: success
    allowNetworkingRestart:
      type: bool
      description: Allow node to update ifcfg files and restart networking
      returned: success
    softwareImageProxy:
      type: complex
      description: Software image used by node
      returned: success
    kernelVersion:
      type: str
      description: Kernel version used
      returned: success
    kernelParameters:
      type: str
      description: Additional kernel parameters passed to the kernel at boot time
      returned: success
    kernelOutputConsole:
      type: str
      description: Kernel output console used at boot time
      returned: success
    modules:
      type: list
      description: Manage kernel modules loaded in this node
      returned: success
    bootLoader:
      type: str
      description: Boot loader
      returned: success
    bootLoaderProtocol:
      type: str
      description: Boot loader protocol for retrieving initrd and vmlinuz
      returned: success
    bootLoaderFile:
      type: str
      description: Alternative boot loader file
      returned: success
    fips:
      type: str
      description: Federal Information Processing Standard Security Requirements
      returned: success
    templateNode:
      type: bool
      description: Indicate this is a template node and should not be powered on and
        booted
      returned: success
    fromTemplateNode:
      type: str
      description: Indicate from which template node this node was copied
      returned: success
    dpuSettings:
      type: complex
      description: Submode containing all DPU node settings
      returned: success
    hostNode:
      type: complex
      description: Host node
      returned: success

"""
############################
# Imports
############################

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import DPUNode
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

    results = entity_query.find(DPUNode)

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

    module.exit_json(dpu_nodes=json_ready_result, changed=False)


if __name__ == '__main__':
    main()