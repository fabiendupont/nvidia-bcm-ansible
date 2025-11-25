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
module: software_image_info
description: Query cmdaemon for entity of type SoftwareImage
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""
- name: list all software images
  register: result
  brightcomputing.bcm110.software_image_info: {}
- name: debug display all software images
  debug:
    msg:
    - 'name: {{item.name}}'
    - 'id: {{item.id}}'
    - 'path: {{item.path}}'
    - 'creation time: {{item.creationTime}}'
    - 'kernel version: {{item.kernelVersion}}'
    - 'kernel modules names: {{item.modules|map(attribute=''name'')|join('' '')}}'
  loop: '{{ result.software_images }}'
  loop_control:
    label: '{{ item.name }}'
- name: set default_image variable
  set_fact:
    default_image: '{{result.software_images | selectattr(''name'', ''equalto'', ''default-image'')
      | first}}'
- name: debug display default-image software image
  debug:
    msg:
    - 'name: {{default_image.name}}'
    - 'id: {{default_image.id}}'
    - 'path: {{default_image.path}}'
    - 'creation time: {{default_image.creationTime}}'
    - 'kernel version: {{default_image.kernelVersion}}'
    - 'kernel modules names: {{default_image.modules|map(attribute=''name'')|join(''
      '')}}'

"""

RETURN = r"""
---
software_image:
  type: list
  description: Software image
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
    path:
      type: str
      description: Base directory of the image
      returned: success
    originalImage:
      type: str
      description: Image from which this one will be cloned
      returned: success
    fileOperationInProgress:
      type: bool
      description: ''
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
    creationTime:
      type: int
      description: Creation time
      returned: success
    modules:
      type: list
      description: Manage kernel modules loaded in this image
      returned: success
    enableSOL:
      type: bool
      description: Enable Serial console Over LAN
      returned: success
    SOLPort:
      type: str
      description: Serial port to use for SOL, usually ttyS0 or ttyS1
      returned: success
    SOLSpeed:
      type: str
      description: Baud rate to use for SOL
      returned: success
    SOLFlowControl:
      type: bool
      description: Enable to use hardware flow control for SOL
      returned: success
    notes:
      type: str
      description: Administrator notes
      returned: success
    fspart:
      type: complex
      description: Internal pointer to the FSPart associated with this image
      returned: success
    bootfspart:
      type: complex
      description: Internal pointer to the FSPart associated with the boot directory
        of this image
      returned: success
    revisionID:
      type: int
      description: ''
      returned: success
    parentSoftwareImage:
      type: complex
      description: ''
      returned: success
    revisionHistory:
      type: list
      description: ''
      returned: success

"""
############################
# Imports
############################

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import SoftwareImage
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

    results = entity_query.find(SoftwareImage)

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

    module.exit_json(software_images=json_ready_result, changed=False)


if __name__ == '__main__':
    main()