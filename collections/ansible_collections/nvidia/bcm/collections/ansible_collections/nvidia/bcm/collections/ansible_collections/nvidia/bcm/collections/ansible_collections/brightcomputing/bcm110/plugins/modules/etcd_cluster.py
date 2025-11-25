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
module: etcd_cluster
description: ['Manages etcd_clusters']
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
      - Name of the Etcd cluster
      type: str
      required: true
    heartBeatInterval:
      description:
      - Time (in milliseconds) of a heartbeat interval
      type: int
      required: false
      default: 100
    electionTimeout:
      description:
      - Time (in milliseconds) for an election to timeout
      type: int
      required: false
      default: 1000
    notes:
      description:
      - Notes
      type: str
      required: false
    ca:
      description:
      - The Certificate Authority (CA) Certificate path for Etcd, used to generate certificates
        for Etcd.
      type: str
      required: false
      default: /etc/kubernetes/pki/default/etcd/ca.crt
    cakey:
      description:
      - The Certificate Authority (CA) Key path for Etcd, used to generate certificates
        for Etcd.
      type: str
      required: false
      default: /etc/kubernetes/pki/default/etcd/ca.key
    memberCertificate:
      description:
      - The Certificate path to use for Etcd cluster members, signed with the Etcd CA.
      type: str
      required: false
      default: /etc/kubernetes/pki/default/etcd-member.crt
    memberCertificateKey:
      description:
      - The Key path to use for Etcd cluster members, signed with the Etcd CA.
      type: str
      required: false
      default: /etc/kubernetes/pki/default/etcd-member.key
    clientCertificate:
      description:
      - The Client Certificate used for Etcdctl for example.
      type: str
      required: false
      default: /etc/kubernetes/pki/default/apiserver-etcd-client.crt
    clientCertificateKey:
      description:
      - The Client Certificate Key used for Etcdctl for example.
      type: str
      required: false
      default: /etc/kubernetes/pki/default/apiserver-etcd-client.key
    clientCA:
      description:
      - The Certificate Authority (CA) used for client certificates. When set it is assumed
        client certificate and key will be generated and signed with this CA by another
        party. Etcd still expects the path to be correct for the Client Certificate and
        Key.
      type: str
      required: false
      default: /etc/kubernetes/pki/default/etcd/ca.crt
    moduleFileTemplate:
      description:
      - Template for system module file
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
etcd_cluster:
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
      description: Name of the Etcd cluster
      returned: success
    heartBeatInterval:
      type: int
      description: Time (in milliseconds) of a heartbeat interval
      returned: success
    electionTimeout:
      type: int
      description: Time (in milliseconds) for an election to timeout
      returned: success
    notes:
      type: str
      description: Notes
      returned: success
    ca:
      type: str
      description: The Certificate Authority (CA) Certificate path for Etcd, used
        to generate certificates for Etcd.
      returned: success
    cakey:
      type: str
      description: The Certificate Authority (CA) Key path for Etcd, used to generate
        certificates for Etcd.
      returned: success
    memberCertificate:
      type: str
      description: The Certificate path to use for Etcd cluster members, signed with
        the Etcd CA.
      returned: success
    memberCertificateKey:
      type: str
      description: The Key path to use for Etcd cluster members, signed with the Etcd
        CA.
      returned: success
    clientCertificate:
      type: str
      description: The Client Certificate used for Etcdctl for example.
      returned: success
    clientCertificateKey:
      type: str
      description: The Client Certificate Key used for Etcdctl for example.
      returned: success
    clientCA:
      type: str
      description: The Certificate Authority (CA) used for client certificates. When
        set it is assumed client certificate and key will be generated and signed
        with this CA by another party. Etcd still expects the path to be correct for
        the Client Certificate and Key.
      returned: success
    clientTypeEtcd:
      type: int
      description: client type in the CLIENT_TYPE_ETCD range
      returned: success
    moduleFileTemplate:
      type: str
      description: Template for system module file
      returned: success

"""
############################
# Imports
############################

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import EtcdCluster
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.etcd_cluster import EtcdCluster_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=EtcdCluster_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, EtcdCluster)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(EtcdCluster, params, commit=not module.check_mode)
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