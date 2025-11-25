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
module: oci_provider
description: ['Manages oci_providers']
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
    defaultNodeInstallerImageId:
      description:
      - Default node-installer image, can be overridden in cloudsettings
      type: str
      required: false
    defaultCompartmentId:
      description:
      - Default compartment ID used, others are listed in https://cloud.oracle.com/identity/compartments.
      type: str
      required: false
    defaultRegion:
      description:
      - Default region to start virtual machine in.
      type: str
      required: false
    defaultShape:
      description:
      - Default cloud node VM shape.
      type: str
      required: false
    APIRegionName:
      description:
      - OCI region name to be used for listing available regions
      type: str
      required: false
    regions:
      description: []
      type: list
      required: false
      default: []
    securityGroupNode:
      description:
      - Security group ID of the cloud nodes
      type: str
      required: false
    computeClusterID:
      description:
      - Compute Cluster ID for nodes that use GPU Memory Cluster
      type: str
      required: false
    defaultAvailabilityDomain:
      description:
      - Default availablity domain for cloud nodes
      type: str
      required: false
    authUser:
      description:
      - User ocid. Format is ocid1.user.oc1..<unique ID>, can be found in Profile->User
        Settings
      type: str
      required: false
    authKeyContent:
      description:
      - API private key file's content (PEM format) to connect to OCI
      type: str
      required: false
    authFingerprint:
      description:
      - Fingerprint of API Keys. Format is 12:34:56:78:90:ab:cd:ef:12:34:56:78:90:ab:cd:ef,
        can be found in Identity->Users->User Details->API Keys
      type: str
      required: false
    authTenancy:
      description:
      - Usually one company will have a single tenancy. Format is ocid1.tenancy.oc1..<unique
        ID>, can be found in https://cloud.oracle.com/tenancy
      type: str
      required: false
    imagesCompartmentId:
      description:
      - Compartment OCID to search for custom images
      type: str
      required: false
    imagesManifestBaseURL:
      description:
      - Base URL to download images manifests
      type: str
      required: false
    definedTags:
      description:
      - List of OCI defined tags that will be assigned to cloud nodes. Defined tags are
        case-insensitive and require the format 'namespace.key.value'
      type: list
      required: false
      default: []

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
oci_provider:
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
    defaultNodeInstallerImageId:
      type: str
      description: Default node-installer image, can be overridden in cloudsettings
      returned: success
    defaultCompartmentId:
      type: str
      description: Default compartment ID used, others are listed in https://cloud.oracle.com/identity/compartments.
      returned: success
    defaultRegion:
      type: complex
      description: Default region to start virtual machine in.
      returned: success
    defaultShape:
      type: complex
      description: Default cloud node VM shape.
      returned: success
    APIRegionName:
      type: str
      description: OCI region name to be used for listing available regions
      returned: success
    regions:
      type: list
      description: ''
      returned: success
    securityGroupNode:
      type: str
      description: Security group ID of the cloud nodes
      returned: success
    computeClusterID:
      type: str
      description: Compute Cluster ID for nodes that use GPU Memory Cluster
      returned: success
    defaultAvailabilityDomain:
      type: str
      description: Default availablity domain for cloud nodes
      returned: success
    authUser:
      type: str
      description: User ocid. Format is ocid1.user.oc1..<unique ID>, can be found
        in Profile->User Settings
      returned: success
    authKeyContent:
      type: str
      description: API private key file's content (PEM format) to connect to OCI
      returned: success
    authFingerprint:
      type: str
      description: Fingerprint of API Keys. Format is 12:34:56:78:90:ab:cd:ef:12:34:56:78:90:ab:cd:ef,
        can be found in Identity->Users->User Details->API Keys
      returned: success
    authTenancy:
      type: str
      description: Usually one company will have a single tenancy. Format is ocid1.tenancy.oc1..<unique
        ID>, can be found in https://cloud.oracle.com/tenancy
      returned: success
    imagesCompartmentId:
      type: str
      description: Compartment OCID to search for custom images
      returned: success
    imagesManifestBaseURL:
      type: str
      description: Base URL to download images manifests
      returned: success
    definedTags:
      type: str
      description: List of OCI defined tags that will be assigned to cloud nodes.
        Defined tags are case-insensitive and require the format 'namespace.key.value'
      returned: success

"""
############################
# Imports
############################

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import OCIProvider
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.oci_provider import OCIProvider_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=OCIProvider_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, OCIProvider)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(OCIProvider, params, commit=not module.check_mode)
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