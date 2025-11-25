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
module: monitoring_trigger
description: ['Manages monitoring_triggers']
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
    disabled:
      description:
      - Disable
      type: bool
      required: false
      default: false
    severity:
      description:
      - Severity
      type: int
      required: false
      default: 10
    markEntityAsFailed:
      description:
      - Mark entity as failed
      type: bool
      required: false
      default: true
    markEntityAsUnknown:
      description:
      - Mark entity as unknown
      type: bool
      required: false
      default: false
    stateFlappingPeriod:
      description:
      - Time period to check for state flapping
      type: float
      required: false
      default: 300.0
    stateFlappingCount:
      description:
      - Number of times states need to change in the specified period before it is considered
        stateflapping
      type: int
      required: false
      default: 5
    enterActions:
      description:
      - Actions to execute when the expression enters 'true' state
      type: list
      required: false
      default: []
    duringActions:
      description:
      - Actions to execute when the expression is and has been 'true'
      type: list
      required: false
      default: []
    leaveActions:
      description:
      - Actions to execute when the expression is was 'true' and no longer is
      type: list
      required: false
      default: []
    stateFlappingActions:
      description:
      - Actions to execute when the expression is state flapping
      type: list
      required: false
      default: []
    expression_MonitoringGroupedExpression:
      description:
      - Expression
      type: dict
      required: false
      options:
        name:
          description:
          - Name
          type: str
          required: true
        op:
          description:
          - Operator
          type: str
          required: false
          default: OR
          choices:
          - OR
          - AND
        allowMissing:
          description:
          - Allow missing sub expressions
          type: bool
          required: false
          default: false
        expressions:
          description:
          - Expressions
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Name
              type: str
              required: true
            entities:
              description:
              - Entities matching the regex, leave empty for all
              type: str
              required: false
            measurables:
              description:
              - Measurables matching the regex, leave empty for all
              type: str
              required: false
            parameters:
              description:
              - Parameters matching the regex, leave empty for all
              type: str
              required: false
            op:
              description:
              - Operator
              type: str
              required: false
              default: EQ
              choices:
              - EQ
              - NE
              - LT
              - GT
            grouping:
              description:
              - Method to group all matching entity measurable parameter
              type: str
              required: false
              default: ANY
              choices:
              - ANY
              - ALL
              - SUM
              - MIN
              - MAX
              - AVG
            value:
              description:
              - Value
              type: str
              required: false
              default: FAIL
            useRaw:
              description:
              - Use raw data instead of rate for cumulative metrics
              type: bool
              required: false
              default: false
            code:
              description:
              - Lua code
              type: str
              required: false
    expression_MonitoringCompareExpression:
      description:
      - Expression
      type: dict
      required: false
      options:
        name:
          description:
          - Name
          type: str
          required: true
        entities:
          description:
          - Entities matching the regex, leave empty for all
          type: str
          required: false
        measurables:
          description:
          - Measurables matching the regex, leave empty for all
          type: str
          required: false
        parameters:
          description:
          - Parameters matching the regex, leave empty for all
          type: str
          required: false
        op:
          description:
          - Operator
          type: str
          required: false
          default: EQ
          choices:
          - EQ
          - NE
          - LT
          - GT
        grouping:
          description:
          - Method to group all matching entity measurable parameter
          type: str
          required: false
          default: ANY
          choices:
          - ANY
          - ALL
          - SUM
          - MIN
          - MAX
          - AVG
        value:
          description:
          - Value
          type: str
          required: false
          default: FAIL
        useRaw:
          description:
          - Use raw data instead of rate for cumulative metrics
          type: bool
          required: false
          default: false
        code:
          description:
          - Lua code
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
monitoring_trigger:
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
    disabled:
      type: bool
      description: Disable
      returned: success
    severity:
      type: int
      description: Severity
      returned: success
    markEntityAsFailed:
      type: bool
      description: Mark entity as failed
      returned: success
    markEntityAsUnknown:
      type: bool
      description: Mark entity as unknown
      returned: success
    stateFlappingPeriod:
      type: float
      description: Time period to check for state flapping
      returned: success
    stateFlappingCount:
      type: int
      description: Number of times states need to change in the specified period before
        it is considered stateflapping
      returned: success
    expression:
      type: complex
      description: Expression
      returned: success
    enterActions:
      type: list
      description: Actions to execute when the expression enters 'true' state
      returned: success
    duringActions:
      type: list
      description: Actions to execute when the expression is and has been 'true'
      returned: success
    leaveActions:
      type: list
      description: Actions to execute when the expression is was 'true' and no longer
        is
      returned: success
    stateFlappingActions:
      type: list
      description: Actions to execute when the expression is state flapping
      returned: success

"""
############################
# Imports
############################

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import MonitoringTrigger
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.monitoring_trigger import MonitoringTrigger_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=MonitoringTrigger_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, MonitoringTrigger)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(MonitoringTrigger, params, commit=not module.check_mode)
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