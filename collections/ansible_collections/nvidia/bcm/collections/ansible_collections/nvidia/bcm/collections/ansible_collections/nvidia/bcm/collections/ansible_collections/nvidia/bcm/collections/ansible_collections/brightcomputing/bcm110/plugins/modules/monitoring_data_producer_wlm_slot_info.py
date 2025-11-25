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
module: monitoring_data_producer_wlm_slot_info
description: Query cmdaemon for entity of type MonitoringDataProducerWlmSlot
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
monitoring_data_producer_wlm_slot:
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
    description:
      type: str
      description: Description
      returned: success
    notes:
      type: str
      description: Administrator notes
      returned: success
    when:
      type: str
      description: When the producer should run
      returned: success
    preJob:
      type: bool
      description: Run as pre job in prolog
      returned: success
    postJob:
      type: bool
      description: Run as post job in epilog
      returned: success
    maxAge:
      type: float
      description: Maximal age of historic data, 0 for infinite
      returned: success
    maxSamples:
      type: int
      description: Maximal samples of historic data, 0 for infinite
      returned: success
    interval:
      type: float
      description: Sampling interval
      returned: success
    offset:
      type: float
      description: Time offset for sampling interval
      returned: success
    startupDelay:
      type: float
      description: Delay the first sampling the specified time after cmd starts
      returned: success
    intervals:
      type: float
      description: Out of band sampling interval
      returned: success
    gap:
      type: int
      description: Number of missed samples before we add a NaN
      returned: success
    fuzzyOffset:
      type: float
      description: Automatic fuzzy offset factor [0-1]. Multiplied by interval
      returned: success
    introduceNaN:
      type: bool
      description: Introduce NaN if device goes up/down/up
      returned: success
    maxMeasurables:
      type: int
      description: Maximal number of measurables the producer can introduce
      returned: success
    automaticReinitialize:
      type: bool
      description: Automatic run --initialize when a new metric has been detected
      returned: success
    disabled:
      type: bool
      description: Disabled
      returned: success
    disableTriggers:
      type: bool
      description: Disable triggers from being evaluated
      returned: success
    disableOnHighLoad:
      type: bool
      description: Disable when nodes are very busy
      returned: success
    nodeExecutionFilters:
      type: list
      description: 'Filter nodes which should run this data producer. If none are
        specified: execute on each node.'
      returned: success
    executionMultiplexers:
      type: list
      description: 'Execute the producer once for each entity which matches one of
        the criteria. If none are specified: only execute it for the node itself.'
      returned: success
    consolidator:
      type: complex
      description: Consolidator configuration
      returned: success
    suppressedByGoingDown:
      type: bool
      description: Suppress running action if device is going down
      returned: success
    access:
      type: str
      description: User access control
      returned: success
    associatedUser:
      type: str
      description: User associated with this measurable
      returned: success

"""
############################
# Imports
############################

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import MonitoringDataProducerWlmSlot
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

    results = entity_query.find(MonitoringDataProducerWlmSlot)

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

    module.exit_json(monitoring_data_producer_wlm_slots=json_ready_result, changed=False)


if __name__ == '__main__':
    main()