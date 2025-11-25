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
module: kube_cluster_info
description: Query cmdaemon for entity of type KubeCluster
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
kube_cluster:
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
      description: Name of the Kubernetes cluster
      returned: success
    etcdCluster:
      type: complex
      description: The Etcd cluster instance
      returned: success
    serviceNetwork:
      type: complex
      description: Network where service cluster IPs will be assigned from (must not
        overlap with any IP ranges assigned to nodes for pods)
      returned: success
    podNetwork:
      type: complex
      description: Network where POD IPs will be assigned from
      returned: success
    podNetworkNodeMask:
      type: str
      description: Pod Network mask size for node cidr in cluster.
      returned: success
    internalNetwork:
      type: complex
      description: Network to use to back the internal communications
      returned: success
    kubeDnsIp:
      type: str
      description: KubeDNS IP address
      returned: success
    kubernetesApiServer:
      type: str
      description: 'Kubernetes API server address (format: https://host:port)'
      returned: success
    kubernetesApiServerProxyPort:
      type: int
      description: Kubernetes API server proxy port
      returned: success
    appGroups:
      type: list
      description: Kubernetes applications managed by cmdaemon
      returned: success
    labelSets:
      type: list
      description: Labels managed by cmdaemon
      returned: success
    notes:
      type: str
      description: Notes
      returned: success
    version:
      type: str
      description: Kubernetes Cluster Version
      returned: success
    trustedDomains:
      type: str
      description: Trusted domains to be included in Kubernetes related certificates
        as Alt Subjects.
      returned: success
    moduleFileTemplate:
      type: str
      description: Template for system module file
      returned: success
    kubeadm_init_file:
      type: str
      description: Kubeadm init file YAML
      returned: success
    kubeadm_init_cert_key:
      type: str
      description: Kubeadm CERT Key
      returned: success
    kubeadm_ca_cert:
      type: str
      description: Kube CA Cert
      returned: success
    kubeadm_ca_key:
      type: str
      description: Kube CA Key
      returned: success
    users:
      type: list
      description: Kubernetes users
      returned: success
    external:
      type: bool
      description: External kubernetes cluster
      returned: success
    externalIngressServer:
      type: str
      description: 'Kubernetes Ingress server address (format: https://host:port)'
      returned: success
    externalPort:
      type: int
      description: External port, set to 0 to disable
      returned: success
    capiTemplate:
      type: bool
      description: CAPI template kubernetes cluster
      returned: success
    capiNamespace:
      type: str
      description: Kubernetes CAPI namespace
      returned: success
    kubeCluster:
      type: complex
      description: The Kubernetes cluster instance managing this CAPI-deployed Kubernetes
        Cluster
      returned: success
    options:
      type: json
      description: Options to configure flags for Kube components
      returned: success
    ingressProxyEnable:
      type: bool
      description: Ingress Proxy Enable Flag
      returned: success
    ingressProxyListenPort:
      type: int
      description: Ingress Proxy Listen Port
      returned: success
    ingressProxyBackendPort:
      type: int
      description: Ingress Proxy Backend Port, set to 0 to disable
      returned: success

"""
############################
# Imports
############################

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import KubeCluster
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

    results = entity_query.find(KubeCluster)

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

    module.exit_json(kube_clusters=json_ready_result, changed=False)


if __name__ == '__main__':
    main()