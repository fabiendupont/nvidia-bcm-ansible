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
module: charge_back_request
description: ['Manages charge_back_requests']
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
    groupByUser:
      description:
      - Group by user
      type: bool
      required: false
      default: false
    groupByGroup:
      description:
      - Group by group
      type: bool
      required: false
      default: false
    groupByAccount:
      description:
      - Group by account
      type: bool
      required: false
      default: false
    groupByJobName:
      description:
      - Group by job name
      type: bool
      required: false
      default: false
    groupByJobId:
      description:
      - Group by job ID
      type: bool
      required: false
      default: false
    groupByAccountingInfo:
      description:
      - Group by accounting info
      type: list
      required: false
      default: []
    users:
      description:
      - Users
      type: list
      required: false
      default: []
    groups:
      description:
      - Users
      type: list
      required: false
      default: []
    accounts:
      description:
      - Accounts
      type: list
      required: false
      default: []
    jobNames:
      description:
      - Job names
      type: list
      required: false
      default: []
    jobIds:
      description:
      - Job IDs
      type: list
      required: false
      default: []
    accountingInfo:
      description:
      - Accounting info
      type: json
      required: false
    wlmClusters:
      description:
      - List of wlm clusters which to include, empty for all
      type: list
      required: false
      default: []
    pricePerCPUSecond:
      description:
      - Price per CPU second
      type: float
      required: false
      default: 0.0
    pricePerCPUCoreSecond:
      description:
      - Price per CPU core second
      type: float
      required: false
      default: 0.0
    pricePerGPUSecond:
      description:
      - Price per GPU second
      type: float
      required: false
      default: 0.0
    pricePerMemoryByteSecond:
      description:
      - Price per memory byte-second
      type: float
      required: false
      default: 0.0
    pricePerSlotSecond:
      description:
      - Price per slot second
      type: float
      required: false
      default: 0.0
    pricePerWattSecond:
      description:
      - Price per Watt second
      type: float
      required: false
      default: 0.0
    currency:
      description:
      - Currency
      type: str
      required: false
      default: $
    startTime:
      description:
      - Start time
      type: str
      required: false
      default: now/M
    endTime:
      description:
      - End time
      type: str
      required: false
      default: now/M
    utc:
      description:
      - Time in UTC
      type: bool
      required: false
      default: false
    includeRunning:
      description:
      - Include running
      type: bool
      required: false
      default: false
    calculatePrediction:
      description:
      - Calculate prediction
      type: bool
      required: false
      default: false
    preference:
      description:
      - The request with the highest preference be shown by default
      type: int
      required: false
      default: 0
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
- name: create example charge_back_request
  brightcomputing.bcm110.charge_back_request:
    name: example
    groupByUser: true
    startTime: now/y
    endTime: now/y

"""

RETURN = r"""
---
charge_back_request:
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

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import ChargeBackRequest
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.charge_back_request import ChargeBackRequest_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=ChargeBackRequest_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, ChargeBackRequest)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(ChargeBackRequest, params, commit=not module.check_mode)
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