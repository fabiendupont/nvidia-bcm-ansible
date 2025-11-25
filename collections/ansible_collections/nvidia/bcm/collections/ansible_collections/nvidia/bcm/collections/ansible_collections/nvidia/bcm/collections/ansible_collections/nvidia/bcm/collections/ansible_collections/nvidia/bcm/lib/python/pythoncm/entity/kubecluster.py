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

from pythoncm.entity import GuiKubeClusterOverview
from pythoncm.entity.entity import Entity


class KubeCluster(Entity):
    def overview(self):
        """
        Get the Kubernetes cluster overiew.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmgui',
            call='getKubeClusterOverview',
            args=[self.uuid],
        )
        if code:
            raise OSError(out)
        if out is None:
            return out
        return GuiKubeClusterOverview(self._cluster, out, self)

    def _component_certificate_name(self) -> str:
        return self._cluster.component_certificate.KUBE % self.name

    def recreate_certificate_CA(self):
        """
        Recreate the CA for the KubeCluster instance.
        """
        return self._cluster.component_certificate.recreate_CA(self._component_certificate_name())

    def recreate_certificates(self, nodes=None):
        """
        Recreate the certificates on one or more nodes for this KubeCluster instance.
        """
        return self._cluster.component_certificate.recreate(self._component_certificate_name(), nodes=nodes)

    def invalidate_certificates(self, nodes=None):
        """
        Invalidate the certificate on one or more nodes for this KubeCluster instance.
        Nodes will no longer be able to connect to the using their existing certificates.
        """
        return self._cluster.component_certificate.invalidate(self._component_certificate_name(), nodes=nodes)

    def _component_service_account_certificate_name(self):
        return self._cluster.component_certificate.KUBE_SA % self.name

    def recreate_service_account_certificate_CA(self):
        """
        Recreate the CA for the KubeCluster instance.
        """
        return self._cluster.component_certificate.recreate_CA(self._component_service_account_certificate_name())

    def recreate_service_account_certificates(self, nodes=None):
        """
        Recreate the certificates on one or more nodes for this KubeCluster instance.
        """
        return self._cluster.component_certificate.recreate(
            self._component_service_account_certificate_name(), nodes=nodes
        )

    def invalidate_service_account_certificates(self, nodes=None):
        """
        Invalidate the certificate on one or more nodes for this KubeCluster instance.
        Nodes will no longer be able to connect to the using their existing certificates.
        """
        return self._cluster.component_certificate.invalidate(
            self._component_service_account_certificate_name(), nodes=nodes
        )

    def _component_users_certificate_name(self) -> str:
        return self._cluster.component_certificate.KUBE_USERS % self.name

    def recreate_user_certificates(self, nodes=None):
        """
        Recreate all users certificate for this KubeCluster instance.
        """
        return self._cluster.component_certificate.recreate(
            self._component_users_certificate_name(),
            nodes=[self._cluster.active_head_node()],
        )
