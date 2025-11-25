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
module: category_info
description: Query cmdaemon for entity of type Category
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""
- name: register all categories
  register: result
  brightcomputing.bcm110.category_info: {}
- name: display categories details
  debug:
    msg:
    - 'name: {{ item.name }}'
    - 'managementNetwork: {{ item.managementNetwork.name }}'
    - 'softwareImage: {{ item.softwareImageProxy.parentSoftwareImage.name }}'
    - 'fsmounts: {{ item.fsmounts|map(attribute=''device'')|join(''|'') }}'
  loop: '{{ result.categories }}'
  loop_control:
    label: '{{ item.name }}'

"""

RETURN = r"""
---
category:
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
    name:
      type: str
      description: Name of category
      returned: success
    fsmounts:
      type: list
      description: Configure the entries placed in /etc/fstab
      returned: success
    staticRoutes:
      type: list
      description: Configure static routes for the interfaces
      returned: success
    roles:
      type: list
      description: Assign the roles the node should play
      returned: success
    notes:
      type: str
      description: Administrator notes
      returned: success
    gpuSettings:
      type: list
      description: Configure the GPUs
      returned: success
    softwareImageProxy:
      type: complex
      description: Software image the category will use
      returned: success
    defaultGateway:
      type: str
      description: Default gateway for the category
      returned: success
    defaultGatewayMetric:
      type: int
      description: Default gateway metric
      returned: success
    nameServers:
      type: str
      description: List of name servers the category will use
      returned: success
    timeServers:
      type: str
      description: List of time servers the category will use
      returned: success
    searchDomains:
      type: str
      description: Search domains for the category
      returned: success
    disksetup:
      type: str
      description: Node specific disk setup
      returned: success
    biosSetup:
      type: json
      description: BIOS setup
      returned: success
    installMode:
      type: str
      description: Installmode to be used by default, if none is specified in the
        node
      returned: success
    newNodeInstallMode:
      type: str
      description: Installmode to be used by default, for new nodes
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
    initialize:
      type: str
      description: Initialize script to be used for category
      returned: success
    finalize:
      type: str
      description: Finalize script to be used for category
      returned: success
    raidconf:
      type: str
      description: Node specific Hardware RAID configuration
      returned: success
    fsexports:
      type: list
      description: Configure the entries placed in /etc/exports
      returned: success
    services:
      type: list
      description: Manage operating system services
      returned: success
    bmcSettings:
      type: complex
      description: Configure the baseboard management controller settings
      returned: success
    seLinuxSettings:
      type: complex
      description: Configure the SELinux settings
      returned: success
    dpuSettings:
      type: complex
      description: Configure the DPU settings
      returned: success
    proxySettings:
      type: complex
      description: Configure the proxy server settings
      returned: success
    accessSettings:
      type: complex
      description: Configure the cluster wide Access settings
      returned: success
    nodeInstallerDisk:
      type: bool
      description: The node has its own node installer disk
      returned: success
    installBootRecord:
      type: bool
      description: Install boot record on local disk
      returned: success
    managementNetwork:
      type: complex
      description: Determines what network should be used for management traffic.
        If not set, partition setting is used.
      returned: success
    interactiveUser:
      type: str
      description: Allow user login on node
      returned: success
    dataNode:
      type: bool
      description: If enabled the node will never do a FULL install without explicit
        user confirmation
      returned: success
    allowNetworkingRestart:
      type: bool
      description: Allow nodes to update ifcfg files and restart networking
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
      description: Manage kernel modules loaded in this image
      returned: success
    versionConfigFiles:
      type: bool
      description: Keep old versions of all config files for all nodes in this category
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
    authenticationService:
      type: str
      description: Authentication service
      returned: success
    timeZoneSettings:
      type: complex
      description: Time zone
      returned: success
    ztpSettings:
      type: complex
      description: Configure the ZTP settings
      returned: success

"""
############################
# Imports
############################

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import Category
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

    results = entity_query.find(Category)

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

    module.exit_json(categories=json_ready_result, changed=False)


if __name__ == '__main__':
    main()