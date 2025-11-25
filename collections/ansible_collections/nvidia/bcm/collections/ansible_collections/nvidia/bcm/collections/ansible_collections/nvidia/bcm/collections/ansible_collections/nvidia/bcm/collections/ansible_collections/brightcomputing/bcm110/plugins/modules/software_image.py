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
module: software_image
description: ['Software image']
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
    path:
      description:
      - Base directory of the image
      type: str
      required: false
    kernelVersion:
      description:
      - Kernel version used
      type: str
      required: false
    kernelParameters:
      description:
      - Additional kernel parameters passed to the kernel at boot time
      type: str
      required: false
    kernelOutputConsole:
      description:
      - Kernel output console used at boot time
      type: str
      required: false
      default: tty0
    modules:
      description:
      - Manage kernel modules loaded in this image
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - The name of the kernel module.
          type: str
          required: true
        parameters:
          description:
          - Options to be passed to the module.
          type: str
          required: false
    enableSOL:
      description:
      - Enable Serial console Over LAN
      type: bool
      required: false
      default: false
    SOLPort:
      description:
      - Serial port to use for SOL, usually ttyS0 or ttyS1
      type: str
      required: false
      default: ttyS1
    SOLSpeed:
      description:
      - Baud rate to use for SOL
      type: str
      required: false
      default: '115200'
      choices:
      - '115200'
      - '57600'
      - '38400'
      - '19200'
      - '9600'
      - '4800'
      - '2400'
      - '1200'
    SOLFlowControl:
      description:
      - Enable to use hardware flow control for SOL
      type: bool
      required: false
      default: true
    notes:
      description:
      - Administrator notes
      type: str
      required: false

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""
- name: clone a software image from default-image
  brightcomputing.bcm110.software_image:
    name: cloned-image
    cloneFrom: default-image
    path: /cm/images/cloned-image
- name: update my-software-image software image
  brightcomputing.bcm110.software_image:
    state: present
    name: my-software-image
    notes: my notes for my-software-image
    path: /cm/images/my-software-image

"""

RETURN = r"""
---
software_image:
  type: complex
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

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import SoftwareImage
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.software_image import SoftwareImage_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=SoftwareImage_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, SoftwareImage)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(SoftwareImage, params, commit=not module.check_mode)
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