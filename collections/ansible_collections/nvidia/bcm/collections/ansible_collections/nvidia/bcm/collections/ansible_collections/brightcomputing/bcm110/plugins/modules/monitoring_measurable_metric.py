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
module: monitoring_measurable_metric
description: ['Manages monitoring_measurable_metrics']
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
    producer:
      description:
      - Monitoring data producer
      type: str
      required: false
    name:
      description:
      - Name
      type: str
      required: true
    parameter:
      description:
      - Parameter
      type: str
      required: false
    maxAge:
      description:
      - Maximal age of historic data, 0 for infinite
      type: float
      required: false
      default: 0.0
    maxSamples:
      description:
      - Maximal samples of historic data, 0 for infinite
      type: int
      required: false
      default: 0
    disabled:
      description:
      - 'Disable: do not process or save to disk'
      type: bool
      required: false
      default: false
    disableTriggers:
      description:
      - Disable triggers from being evaluated
      type: bool
      required: false
      default: false
    gap:
      description:
      - Number of missed samples before we add a NaN
      type: int
      required: false
      default: 0
    introduceNaN:
      description:
      - Introduce NaN if device goes up/down/up
      type: bool
      required: false
      default: false
    description:
      description:
      - Description
      type: str
      required: false
    typeClass:
      description:
      - Type class, slash(/) separated for levels
      type: str
      required: false
    sourceType:
      description:
      - Source of the measurable
      type: str
      required: false
      default: BRIGHT
      choices:
      - ANY
      - BRIGHT
      - PROMETHEUS
      - BOTH
    consolidator:
      description:
      - Consolidator configuration
      type: str
      required: false
    suppressedByGoingDown:
      description:
      - Suppress running action if device is going down
      type: bool
      required: false
      default: false
    access:
      description:
      - User access control
      type: str
      required: false
      default: INHERIT
      choices:
      - PUBLIC
      - PRIVATE
      - INDIVIDUAL
      - INHERIT
    associatedUser:
      description:
      - User associated with this measurable
      type: str
      required: false
    minimum:
      description:
      - Minimum
      type: float
      required: false
      default: 0.0
    maximum:
      description:
      - Maximum
      type: float
      required: false
      default: 0.0
    cumulative:
      description:
      - Cumulative
      type: bool
      required: false
      default: false
    integer:
      description:
      - Only integers values will be reporter, interpolate accordingly
      type: bool
      required: false
      default: false
    unit:
      description:
      - Unit
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
monitoring_measurable_metric:
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
    producer:
      type: complex
      description: Monitoring data producer
      returned: success
    name:
      type: str
      description: Name
      returned: success
    parameter:
      type: str
      description: Parameter
      returned: success
    maxAge:
      type: float
      description: Maximal age of historic data, 0 for infinite
      returned: success
    maxSamples:
      type: int
      description: Maximal samples of historic data, 0 for infinite
      returned: success
    disabled:
      type: bool
      description: 'Disable: do not process or save to disk'
      returned: success
    disableTriggers:
      type: bool
      description: Disable triggers from being evaluated
      returned: success
    gap:
      type: int
      description: Number of missed samples before we add a NaN
      returned: success
    introduceNaN:
      type: bool
      description: Introduce NaN if device goes up/down/up
      returned: success
    description:
      type: str
      description: Description
      returned: success
    typeClass:
      type: str
      description: Type class, slash(/) separated for levels
      returned: success
    sourceType:
      type: str
      description: Source of the measurable
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
    minimum:
      type: float
      description: Minimum
      returned: success
    maximum:
      type: float
      description: Maximum
      returned: success
    cumulative:
      type: bool
      description: Cumulative
      returned: success
    integer:
      type: bool
      description: Only integers values will be reporter, interpolate accordingly
      returned: success
    unit:
      type: str
      description: Unit
      returned: success

"""
############################
# Imports
############################

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import MonitoringMeasurableMetric
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.monitoring_measurable_metric import MonitoringMeasurableMetric_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=MonitoringMeasurableMetric_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, MonitoringMeasurableMetric)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(MonitoringMeasurableMetric, params, commit=not module.check_mode)
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