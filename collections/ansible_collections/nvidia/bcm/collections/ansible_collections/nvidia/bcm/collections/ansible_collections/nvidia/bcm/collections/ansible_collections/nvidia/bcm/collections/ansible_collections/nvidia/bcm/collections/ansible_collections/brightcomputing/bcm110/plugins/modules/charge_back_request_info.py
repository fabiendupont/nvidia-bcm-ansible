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
module: charge_back_request_info
description: Query cmdaemon for entity of type ChargeBackRequest
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
charge_back_request:
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
    groupByUser:
      type: bool
      description: Group by user
      returned: success
    groupByGroup:
      type: bool
      description: Group by group
      returned: success
    groupByAccount:
      type: bool
      description: Group by account
      returned: success
    groupByJobName:
      type: bool
      description: Group by job name
      returned: success
    groupByJobId:
      type: bool
      description: Group by job ID
      returned: success
    groupByAccountingInfo:
      type: str
      description: Group by accounting info
      returned: success
    users:
      type: str
      description: Users
      returned: success
    groups:
      type: str
      description: Users
      returned: success
    accounts:
      type: str
      description: Accounts
      returned: success
    jobNames:
      type: str
      description: Job names
      returned: success
    jobIds:
      type: str
      description: Job IDs
      returned: success
    accountingInfo:
      type: json
      description: Accounting info
      returned: success
    wlmClusters:
      type: list
      description: List of wlm clusters which to include, empty for all
      returned: success
    pricePerCPUSecond:
      type: float
      description: Price per CPU second
      returned: success
    pricePerCPUCoreSecond:
      type: float
      description: Price per CPU core second
      returned: success
    pricePerGPUSecond:
      type: float
      description: Price per GPU second
      returned: success
    pricePerMemoryByteSecond:
      type: float
      description: Price per memory byte-second
      returned: success
    pricePerSlotSecond:
      type: float
      description: Price per slot second
      returned: success
    pricePerWattSecond:
      type: float
      description: Price per Watt second
      returned: success
    currency:
      type: str
      description: Currency
      returned: success
    startTime:
      type: str
      description: Start time
      returned: success
    endTime:
      type: str
      description: End time
      returned: success
    utc:
      type: bool
      description: Time in UTC
      returned: success
    includeRunning:
      type: bool
      description: Include running
      returned: success
    calculatePrediction:
      type: bool
      description: Calculate prediction
      returned: success
    preference:
      type: int
      description: The request with the highest preference be shown by default
      returned: success
    notes:
      type: str
      description: Administrator notes
      returned: success

"""
############################
# Imports
############################

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import ChargeBackRequest
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

    results = entity_query.find(ChargeBackRequest)

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

    module.exit_json(charge_back_requests=json_ready_result, changed=False)


if __name__ == '__main__':
    main()