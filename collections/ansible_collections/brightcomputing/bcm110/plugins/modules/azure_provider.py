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
module: azure_provider
description: ['Manages azure_providers']
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
    subscriptionId:
      description:
      - Azure Subscription ID.
      type: str
      required: false
    clientId:
      description:
      - Azure Client ID.
      type: str
      required: false
    clientSecret:
      description:
      - Azure Client Secret.
      type: str
      required: false
    tenantId:
      description:
      - Tenant ID.
      type: str
      required: false
    cloudName:
      description:
      - Azure Cloud Name. Used to access non-public regions.
      type: str
      required: false
      default: AzureCloud
    defaultLocation:
      description:
      - Default location to start virtual machine in.
      type: str
      required: false
    defaultVMSize:
      description:
      - Default cloud node VM size.
      type: str
      required: false
    defaultDirectorVMSize:
      description:
      - Default cloud director VM size.
      type: str
      required: false
    defaultHyperVGeneration:
      description:
      - Hyper-V generation to use by default (V1 or V2), see https://docs.microsoft.com/en-us/azure/virtual-machines/generation-2
      type: str
      required: false
      default: V1
      choices:
      - V1
      - V2
    extensions:
      description:
      - List of extensions
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - User-defined name of the private cloud
          type: str
          required: true
        location:
          description:
          - Region of the cluster extension
          type: str
          required: false
        resourceGroup:
          description:
          - Azure resource group name for all resources in the extension
          type: str
          required: false
        network:
          description:
          - Network associated with the extension
          type: str
          required: false
        extraField:
          description:
          - Reserved
          type: list
          required: false
          default: []
    regions:
      description: []
      type: list
      required: false
      default: []
    defaultNodeInstallerImage:
      description:
      - Default node-installer image, can be overridden in the OS disk.
      type: str
      required: false
    marketplaceUsePolicy:
      description:
      - Preference towards using marketplace images
      type: str
      required: false
      default: NEVER
      choices:
      - ALWAYS
      - NEVER
      - AS_NEEDED
    freeImageType:
      description:
      - What kind of image to use for cloud nodes within the license
      type: str
      required: false
      default: MARKETPLACE
      choices:
      - VHD
      - MARKETPLACE

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
azure_provider:
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
    subscriptionId:
      type: str
      description: Azure Subscription ID.
      returned: success
    clientId:
      type: str
      description: Azure Client ID.
      returned: success
    clientSecret:
      type: str
      description: Azure Client Secret.
      returned: success
    tenantId:
      type: str
      description: Tenant ID.
      returned: success
    cloudName:
      type: str
      description: Azure Cloud Name. Used to access non-public regions.
      returned: success
    defaultLocation:
      type: complex
      description: Default location to start virtual machine in.
      returned: success
    defaultVMSize:
      type: complex
      description: Default cloud node VM size.
      returned: success
    defaultDirectorVMSize:
      type: complex
      description: Default cloud director VM size.
      returned: success
    defaultHyperVGeneration:
      type: str
      description: Hyper-V generation to use by default (V1 or V2), see https://docs.microsoft.com/en-us/azure/virtual-machines/generation-2
      returned: success
    extensions:
      type: list
      description: List of extensions
      returned: success
    regions:
      type: list
      description: ''
      returned: success
    defaultNodeInstallerImage:
      type: str
      description: Default node-installer image, can be overridden in the OS disk.
      returned: success
    marketplaceUsePolicy:
      type: str
      description: Preference towards using marketplace images
      returned: success
    freeImageType:
      type: str
      description: What kind of image to use for cloud nodes within the license
      returned: success

"""
############################
# Imports
############################

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import AzureProvider
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.azure_provider import AzureProvider_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=AzureProvider_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, AzureProvider)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(AzureProvider, params, commit=not module.check_mode)
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