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
module: ec2_provider_info
description: Query cmdaemon for entity of type EC2Provider
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
ec2_provider:
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
    APIRegionName:
      type: str
      description: AWS region to be used for listing available regions
      returned: success
    accessKeyId:
      type: str
      description: AWS access key ID
      returned: success
    accessKeySecret:
      type: str
      description: AWS secret access key
      returned: success
    iamRoleName:
      type: str
      description: IAM role to get AWS credentials from. The role must be assigned
        to the COD-AWS head node.
      returned: success
    VPCs:
      type: list
      description: List of VPCs
      returned: success
    regions:
      type: list
      description: ''
      returned: success
    defaultRegion:
      type: complex
      description: Default region to start instances in
      returned: success
    defaultType:
      type: complex
      description: Default type for instances
      returned: success
    defaultDirectorType:
      type: complex
      description: Default type for cloud director instances
      returned: success
    imageOwners:
      type: str
      description: AWS Account IDs to be used to search for images
      returned: success
    addJobBasedTag:
      type: bool
      description: Enable automatic tagging of cloud resources with information of
        running cloud jobs to allow cost monitoring
      returned: success
    JobIdTagName:
      type: str
      description: The name of the tag that contains the job ID when using job based
        tagging
      returned: success
    JobAccountTagName:
      type: str
      description: The name of the tag that contains the job account when using job
        based tagging
      returned: success
    JobUserTagName:
      type: str
      description: The name of the tag that contains the user name when using job
        based tagging
      returned: success
    JobNameTagName:
      type: str
      description: The name of the tag that contains the job name when using job based
        tagging
      returned: success
    marketplaceUsePolicy:
      type: str
      description: Preference towards using marketplace AMIs
      returned: success

"""
############################
# Imports
############################

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import EC2Provider
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

    results = entity_query.find(EC2Provider)

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

    module.exit_json(ec2_providers=json_ready_result, changed=False)


if __name__ == '__main__':
    main()