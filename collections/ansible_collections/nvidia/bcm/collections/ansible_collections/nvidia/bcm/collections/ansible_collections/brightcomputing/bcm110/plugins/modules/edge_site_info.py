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
module: edge_site_info
description: Query cmdaemon for entity of type EdgeSite
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
edge_site:
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
    contact:
      type: str
      description: Names of contacts
      returned: success
    adminEmail:
      type: str
      description: Administrator's email
      returned: success
    address:
      type: str
      description: Address
      returned: success
    city:
      type: str
      description: City
      returned: success
    country:
      type: str
      description: Country
      returned: success
    timeZoneSettings:
      type: complex
      description: Time zone
      returned: success
    notes:
      type: str
      description: Notes
      returned: success
    nodes:
      type: list
      description: List of nodes in this site
      returned: success
    switches:
      type: list
      description: List of switches in this site
      returned: success
    genericDevices:
      type: list
      description: List of generic devices in this site
      returned: success
    powerDistributionUnits:
      type: list
      description: List of power distribution units in this site
      returned: success
    racks:
      type: list
      description: List of racks in this site
      returned: success
    secret:
      type: str
      description: Edge site secret
      returned: success
    metaDataDeviceLabel:
      type: str
      description: Meta data device label which to mount in order get the meta data
      returned: success
    metaDataUrl:
      type: str
      description: Meta data URL that contains information for edge directors
      returned: success
    createISO:
      type: str
      description: Edge site site ISO/script for USB
      returned: success
    createIMG:
      type: str
      description: Edge site site IMG/script for MMC
      returned: success
    includeCMSharedOnMedia:
      type: bool
      description: Include /cm/shared on media to reduce the amount of rsync during
        edge director installation
      returned: success
    includeImagesOnMedia:
      type: bool
      description: Include images on media to reduce the amount of rsync during edge
        director installation
      returned: success
    preStageRequestID:
      type: str
      description: Pre-staging request ID
      returned: success
    preStageRequestIDCreationTime:
      type: int
      description: Pre-staging request ID creation time
      returned: success

"""
############################
# Imports
############################

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import EdgeSite
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

    results = entity_query.find(EdgeSite)

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

    module.exit_json(edge_sites=json_ready_result, changed=False)


if __name__ == '__main__':
    main()