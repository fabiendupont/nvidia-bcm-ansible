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
module: gcp_provider_info
description: Query cmdaemon for entity of type GCPProvider
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
gcp_provider:
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

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import GCPProvider
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

    results = entity_query.find(GCPProvider)

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

    module.exit_json(gcp_providers=json_ready_result, changed=False)


if __name__ == '__main__':
    main()