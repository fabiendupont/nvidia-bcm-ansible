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
module: ec2_provider
description: ['Manages ec2_providers']
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
    APIRegionName:
      description:
      - AWS region to be used for listing available regions
      type: str
      required: false
    accessKeyId:
      description:
      - AWS access key ID
      type: str
      required: false
    accessKeySecret:
      description:
      - AWS secret access key
      type: str
      required: false
    iamRoleName:
      description:
      - IAM role to get AWS credentials from. The role must be assigned to the COD-AWS
        head node.
      type: str
      required: false
    VPCs:
      description:
      - List of VPCs
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - User-defined name of the VPC
          type: str
          required: true
        vpcID:
          description:
          - AWS VPC identifier
          type: str
          required: false
        defaultImageId:
          description:
          - ID of the default AMI to start instances with ('latest' means using the latest
            AMI)
          type: str
          required: false
        publicACL:
          description:
          - Public Network ACL ID of the public subnet (cloud director)
          type: str
          required: false
        privateACL:
          description:
          - Private Network ACL ID of the private subnet (cloud node)
          type: str
          required: false
        internetGatewayID:
          description:
          - The AWS ID of the internet gateway assigned to this VPC
          type: str
          required: false
        region:
          description:
          - AWS region of the VPC
          type: str
          required: false
        subnets:
          description:
          - Subnets (networks) associated with the VPC
          type: list
          required: false
          default: []
        baseAddress:
          description:
          - Base IP address of the VPC
          type: str
          required: false
          default: 10.0.0.0
        netmaskBits:
          description:
          - Number of netmask bits
          type: int
          required: false
          default: 16
        securityGroupNode:
          description:
          - Security group ID of the cloud nodes
          type: str
          required: false
        securityGroupDirector:
          description:
          - Security group ID of the cloud director
          type: str
          required: false
        routeTableIdPublic:
          description:
          - Routing table ID for the public subnet
          type: str
          required: false
        routeTableIdPrivate:
          description:
          - Routing table ID for private subnets
          type: str
          required: false
        setDirectorAsDefaultGateway:
          description:
          - If specified, a default route via the director will be created in the private
            subnet. This is not necessary if the private subnet was already configured
            and the nodes have access to the head node (e.g Direct Connect)
          type: bool
          required: false
          default: true
        useInternalIPForDirectorIP:
          description:
          - If specified, CMDaemon will use cloud director's internal IP, instead of a
            public/external IP. Useful when you have existing IP connectivity to your
            VPC.
          type: bool
          required: false
          default: false
        enforceDirectorIP:
          description:
          - If specified, CMDaemon will assume this is the cloud director's IP address.
          type: str
          required: false
          default: 0.0.0.0
        extra_values:
          description: []
          type: json
          required: false
    regions:
      description: []
      type: list
      required: false
      default: []
    defaultRegion:
      description:
      - Default region to start instances in
      type: str
      required: false
    defaultType:
      description:
      - Default type for instances
      type: str
      required: false
    defaultDirectorType:
      description:
      - Default type for cloud director instances
      type: str
      required: false
    imageOwners:
      description:
      - AWS Account IDs to be used to search for images
      type: list
      required: false
      default:
      - '137677339600'
      - '197943594779'
    addJobBasedTag:
      description:
      - Enable automatic tagging of cloud resources with information of running cloud
        jobs to allow cost monitoring
      type: bool
      required: false
      default: false
    JobIdTagName:
      description:
      - The name of the tag that contains the job ID when using job based tagging
      type: str
      required: false
      default: BCM_JOB_ID
    JobAccountTagName:
      description:
      - The name of the tag that contains the job account when using job based tagging
      type: str
      required: false
      default: BCM_JOB_ACCOUNT
    JobUserTagName:
      description:
      - The name of the tag that contains the user name when using job based tagging
      type: str
      required: false
      default: BCM_JOB_USER
    JobNameTagName:
      description:
      - The name of the tag that contains the job name when using job based tagging
      type: str
      required: false
      default: BCM_JOB_NAME
    marketplaceUsePolicy:
      description:
      - Preference towards using marketplace AMIs
      type: str
      required: false
      default: NEVER
      choices:
      - ALWAYS
      - NEVER
      - AS_NEEDED

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
ec2_provider:
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

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import EC2Provider
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.ec2_provider import EC2Provider_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=EC2Provider_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, EC2Provider)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(EC2Provider, params, commit=not module.check_mode)
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