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

import typing

from pythoncm.entity.node import Node

if typing.TYPE_CHECKING:
    from collections.abc import Collection
    from uuid import UUID

    from pythoncm.cluster import Cluster


class ComponentCertificate:
    """
    Recreate component certificates
    """

    LDAP = 'ldap'

    # KubeCluster and EtcdCluster have a certificate per instance
    KUBE = 'kube-%s'
    KUBE_SA = 'kube-%s-sa'
    KUBE_USERS = 'kube-%s-users'
    ETCD = 'etcd-%s'

    CREATE_NOT_SAVED = -2
    CREATE_ERROR = -1
    CREATE_FAILED = 0
    CREATE_OK = 1
    CREATE_NODE_DOWN = -100
    CREATE_NO_SUCH_NODE_DOWN = -101
    CREATE_NO_REMOTE_CM = -102
    CREATE_NO_RPC_ERROR = -103

    def __init__(self, cluster: Cluster):
        self.cluster = cluster

    def recreate_CA(self, component=LDAP):
        """
        Recreate a components CA.
        Only needed when the CA private key has been leaked or lost.
        """
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmcert',
            call='recreateComponentCA',
            args=[component],
        )
        if code:
            raise OSError(out)
        return out

    def __get_nodes_uuids(self, nodes: Collection[Node] | None) -> list[UUID]:
        if not nodes:
            return [node.uuid for node in self.cluster.get_by_type(Node)]

        return self.cluster._entities_to_uuids(nodes)

    def recreate(self, nodes: Collection[Node] | None = None, component=LDAP):
        """
        Recreate the component certificate on one or more nodes.
        """
        node_uuids = self.__get_nodes_uuids(nodes)
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmcert',
            call='precreateComponentCertificate',
            args=[component, node_uuids],
        )
        if code:
            raise OSError(out)
        return list(zip(node_uuids, out))

    def invalidate(self, nodes: Collection[Node] | None = None, component=LDAP):
        """
        Invalidate the component certificate on one or more nodes.
        Nodes will no longer be able to connect to the component using their existing certificates.
        """
        node_uuids = self.__get_nodes_uuids(nodes)
        rpc = self.cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmcert',
            call='pinvalidateComponent',
            args=[component, node_uuids],
        )
        if code:
            raise OSError(out)
        return list(zip(node_uuids, out))
