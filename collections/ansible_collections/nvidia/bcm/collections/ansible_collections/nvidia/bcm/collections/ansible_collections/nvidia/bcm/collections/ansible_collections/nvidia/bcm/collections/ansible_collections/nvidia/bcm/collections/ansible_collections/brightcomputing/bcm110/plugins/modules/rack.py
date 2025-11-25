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
module: rack
description: ['Rack']
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
    location:
      description:
      - Location
      type: str
      required: false
    building:
      description:
      - Building
      type: str
      required: false
    room:
      description:
      - Room
      type: str
      required: false
    row:
      description:
      - Row
      type: str
      required: false
    partNumber:
      description:
      - Part number
      type: str
      required: false
    serialNumber:
      description:
      - Serial number
      type: str
      required: false
    model:
      description:
      - Model
      type: str
      required: false
    type:
      description:
      - Type
      type: str
      required: false
    xCoordinate:
      description:
      - Position in the room
      type: int
      required: false
      default: 0
    yCoordinate:
      description:
      - Position in the room
      type: int
      required: false
      default: 0
    height:
      description:
      - Height
      type: int
      required: false
      default: 42
    width:
      description:
      - Width
      type: int
      required: false
      default: 19
    depth:
      description:
      - Depth
      type: int
      required: false
      default: 34
    angle:
      description:
      - Angle of the rack, 90 face right, 180 face backwards, 270 face left
      type: int
      required: false
      default: 0
    inverted:
      description:
      - Inverted racks have position 1 at the bottom
      type: bool
      required: false
      default: false
    notes:
      description:
      - Administrator notes
      type: str
      required: false
    twin:
      description:
      - Rack twin that makes up the NV link domain
      type: str
      required: false

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
rack:
  type: complex
  description: Rack
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
    location:
      type: str
      description: Location
      returned: success
    building:
      type: str
      description: Building
      returned: success
    room:
      type: str
      description: Room
      returned: success
    row:
      type: str
      description: Row
      returned: success
    partNumber:
      type: str
      description: Part number
      returned: success
    serialNumber:
      type: str
      description: Serial number
      returned: success
    model:
      type: str
      description: Model
      returned: success
    type:
      type: str
      description: Type
      returned: success
    xCoordinate:
      type: int
      description: Position in the room
      returned: success
    yCoordinate:
      type: int
      description: Position in the room
      returned: success
    height:
      type: int
      description: Height
      returned: success
    width:
      type: int
      description: Width
      returned: success
    depth:
      type: int
      description: Depth
      returned: success
    angle:
      type: int
      description: Angle of the rack, 90 face right, 180 face backwards, 270 face
        left
      returned: success
    inverted:
      type: bool
      description: Inverted racks have position 1 at the bottom
      returned: success
    notes:
      type: str
      description: Administrator notes
      returned: success
    twin:
      type: complex
      description: Rack twin that makes up the NV link domain
      returned: success

"""
############################
# Imports
############################

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import Rack
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.rack import Rack_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=Rack_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, Rack)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(Rack, params, commit=not module.check_mode)
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