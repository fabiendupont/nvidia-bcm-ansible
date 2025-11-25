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
module: kube_cluster
description: ['Manages kube_clusters']
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
      - Name of the Kubernetes cluster
      type: str
      required: true
    etcdCluster:
      description:
      - The Etcd cluster instance
      type: str
      required: false
    serviceNetwork:
      description:
      - Network where service cluster IPs will be assigned from (must not overlap with
        any IP ranges assigned to nodes for pods)
      type: str
      required: false
    podNetwork:
      description:
      - Network where POD IPs will be assigned from
      type: str
      required: false
    podNetworkNodeMask:
      description:
      - Pod Network mask size for node cidr in cluster.
      type: str
      required: false
    internalNetwork:
      description:
      - Network to use to back the internal communications
      type: str
      required: false
    kubeDnsIp:
      description:
      - KubeDNS IP address
      type: str
      required: false
      default: 0.0.0.0
    kubernetesApiServer:
      description:
      - 'Kubernetes API server address (format: https://host:port)'
      type: str
      required: false
    kubernetesApiServerProxyPort:
      description:
      - Kubernetes API server proxy port
      type: int
      required: false
      default: 6444
    appGroups:
      description:
      - Kubernetes applications managed by cmdaemon
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Object name
          type: str
          required: true
        applications:
          description:
          - Kubernetes applications managed by cmdaemon
          type: list
          required: false
          default: []
          elements: dict
          options:
            name:
              description:
              - Object name
              type: str
              required: true
            format:
              description:
              - Configuration format
              type: str
              required: false
              default: Yaml
              choices:
              - Yaml
              - Json
              - Other
            enabled:
              description:
              - Enable this application
              type: bool
              required: false
              default: true
            config:
              description:
              - Yaml or json configuration for the object
              type: str
              required: false
            extraEnvironment:
              description:
              - Additional variables for kubernetes apps or kubernetes nodes environment
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
                value:
                  description:
                  - Value
                  type: str
                  required: false
                nodesEnvironment:
                  description:
                  - Add variable to the nodes environment
                  type: bool
                  required: false
                  default: false
            excludeListSnippets:
              description: []
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
                excludeList:
                  description:
                  - Excluded paths in the node image update
                  type: list
                  required: false
                  default: []
                disabled:
                  description:
                  - Disabled
                  type: bool
                  required: false
                  default: false
                noNewFiles:
                  description:
                  - No new files
                  type: bool
                  required: false
                  default: false
                modeSync:
                  description:
                  - Include this snippet when mode is sync
                  type: bool
                  required: false
                  default: true
                modeFull:
                  description:
                  - Include this snippet when mode is full
                  type: bool
                  required: false
                  default: false
                modeUpdate:
                  description:
                  - Include this snippet when mode is update
                  type: bool
                  required: false
                  default: true
                modeGrab:
                  description:
                  - Include this snippet when mode is grab
                  type: bool
                  required: false
                  default: false
                modeGrabNew:
                  description:
                  - Include this snippet when mode is grab new
                  type: bool
                  required: false
                  default: false
            state:
              description: []
              type: int
              required: false
              default: 0
        enabled:
          description:
          - Enable this application group
          type: bool
          required: false
          default: true
    labelSets:
      description:
      - Labels managed by cmdaemon
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Object name
          type: str
          required: true
        labels:
          description:
          - Node labels
          type: list
          required: false
          default: []
        nodes:
          description:
          - List of nodes belonging to this label set
          type: list
          required: false
          default: []
        categories:
          description:
          - List of categories belonging to this label set
          type: list
          required: false
          default: []
        overlays:
          description:
          - List of overlays belonging to this label set
          type: list
          required: false
          default: []
    notes:
      description:
      - Notes
      type: str
      required: false
    version:
      description:
      - Kubernetes Cluster Version
      type: str
      required: false
    trustedDomains:
      description:
      - Trusted domains to be included in Kubernetes related certificates as Alt Subjects.
      type: list
      required: false
      default:
      - kubernetes
      - kubernetes.default
      - kubernetes.default.svc
      - master
      - localhost
    moduleFileTemplate:
      description:
      - Template for system module file
      type: str
      required: false
    kubeadm_init_file:
      description:
      - Kubeadm init file YAML
      type: str
      required: false
    kubeadm_init_cert_key:
      description:
      - Kubeadm CERT Key
      type: str
      required: false
    kubeadm_ca_cert:
      description:
      - Kube CA Cert
      type: str
      required: false
    kubeadm_ca_key:
      description:
      - Kube CA Key
      type: str
      required: false
    users:
      description:
      - Kubernetes users
      type: list
      required: false
      default: []
      elements: dict
      options:
        userName:
          description:
          - User name (not user ID)
          type: str
          required: true
        manageKubeConfig:
          description:
          - Write a kubeconfig file for this user
          type: bool
          required: false
          default: true
        initialDefaultNamespace:
          description:
          - namespace to make default when creating kubeconfig
          type: str
          required: false
    external:
      description:
      - External kubernetes cluster
      type: bool
      required: false
      default: false
    externalIngressServer:
      description:
      - 'Kubernetes Ingress server address (format: https://host:port)'
      type: str
      required: false
    externalPort:
      description:
      - External port, set to 0 to disable
      type: int
      required: false
      default: 0
    capiTemplate:
      description:
      - CAPI template kubernetes cluster
      type: bool
      required: false
      default: false
    capiNamespace:
      description:
      - Kubernetes CAPI namespace
      type: str
      required: false
      default: default
    kubeCluster:
      description:
      - The Kubernetes cluster instance managing this CAPI-deployed Kubernetes Cluster
      type: str
      required: false
    options:
      description:
      - Options to configure flags for Kube components
      type: json
      required: false
    ingressProxyEnable:
      description:
      - Ingress Proxy Enable Flag
      type: bool
      required: false
      default: false
    ingressProxyListenPort:
      description:
      - Ingress Proxy Listen Port
      type: int
      required: false
      default: 443
    ingressProxyBackendPort:
      description:
      - Ingress Proxy Backend Port, set to 0 to disable
      type: int
      required: false
      default: 0

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
kube_cluster:
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

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import KubeCluster
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.kube_cluster import KubeCluster_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=KubeCluster_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, KubeCluster)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(KubeCluster, params, commit=not module.check_mode)
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