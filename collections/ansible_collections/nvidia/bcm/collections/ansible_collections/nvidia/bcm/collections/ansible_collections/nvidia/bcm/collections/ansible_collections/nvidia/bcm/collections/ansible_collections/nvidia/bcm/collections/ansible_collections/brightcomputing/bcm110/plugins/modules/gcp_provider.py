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
module: gcp_provider
description: ['Manages gcp_providers']
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
    tags:
      description:
      - List of tags that will be assigned to all resources created by BCM under this
        cloud provider
      type: list
      required: false
      default: []
    projectId:
      description:
      - GCP project ID
      type: str
      required: false
    defaultBootDiskType:
      description:
      - Default boot disk type. Used if bootDiskType in cloudsettings is empty.
      type: str
      required: false
    defaultBootImageURI:
      description:
      - Default boot image URI. Used if bootImageURI in cloudsettings is empty.
      type: str
      required: false
    defaultMachineType:
      description:
      - Default machine type. Used if machineType in cloudsettings is empty.
      type: str
      required: false
    defaultMaintenancePolicy:
      description:
      - Default maintenance policy. Used if maintenancePolicy in cloudsettings is empty.
      type: str
      required: false
    defaultProvisioningModel:
      description:
      - Default provisioning model. Used if provisioningModel in cloudsettings is empty.
      type: str
      required: false
    defaultReservationName:
      description:
      - Default reservation name. Used if reservationName in cloudsettings is empty.
      type: str
      required: false
    defaultReservationType:
      description:
      - Default reservation type. Used if reservationType in cloudsettings is empty.
      type: str
      required: false
    defaultResourcePolicies:
      description:
      - Default resource policies. Used if resourcePolicies in cloudsettings is empty.
      type: list
      required: false
      default: []
    defaultServiceAccount:
      description:
      - Default service account. Used if serviceAccount in cloudsettings is empty.
      type: str
      required: false
    defaultZone:
      description:
      - Default zone. Used if zone in cloudsettings is empty.
      type: str
      required: false
    imageStorageLocation:
      description:
      - Storage location of newly created image resources. The location may be a GCP region
        or multiregion (e.g. 'eu').
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
gcp_provider:
  type: complex
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
      description: Name
      returned: success
    tags:
      type: str
      description: List of tags that will be assigned to all resources created by
        BCM under this cloud provider
      returned: success
    projectId:
      type: str
      description: GCP project ID
      returned: success
    defaultBootDiskType:
      type: str
      description: Default boot disk type. Used if bootDiskType in cloudsettings is
        empty.
      returned: success
    defaultBootImageURI:
      type: str
      description: Default boot image URI. Used if bootImageURI in cloudsettings is
        empty.
      returned: success
    defaultMachineType:
      type: complex
      description: Default machine type. Used if machineType in cloudsettings is empty.
      returned: success
    defaultMaintenancePolicy:
      type: str
      description: Default maintenance policy. Used if maintenancePolicy in cloudsettings
        is empty.
      returned: success
    defaultProvisioningModel:
      type: str
      description: Default provisioning model. Used if provisioningModel in cloudsettings
        is empty.
      returned: success
    defaultReservationName:
      type: str
      description: Default reservation name. Used if reservationName in cloudsettings
        is empty.
      returned: success
    defaultReservationType:
      type: str
      description: Default reservation type. Used if reservationType in cloudsettings
        is empty.
      returned: success
    defaultResourcePolicies:
      type: str
      description: Default resource policies. Used if resourcePolicies in cloudsettings
        is empty.
      returned: success
    defaultServiceAccount:
      type: str
      description: Default service account. Used if serviceAccount in cloudsettings
        is empty.
      returned: success
    defaultZone:
      type: complex
      description: Default zone. Used if zone in cloudsettings is empty.
      returned: success
    imageStorageLocation:
      type: str
      description: Storage location of newly created image resources. The location
        may be a GCP region or multiregion (e.g. 'eu').
      returned: success

"""
############################
# Imports
############################

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import GCPProvider
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.gcp_provider import GCPProvider_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=GCPProvider_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, GCPProvider)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(GCPProvider, params, commit=not module.check_mode)
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