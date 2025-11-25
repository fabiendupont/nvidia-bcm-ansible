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

from pythoncm.entity.entity import Entity


class CertificateRequest(Entity):
    def issue(self, certificate_subject_name):
        """
        Issue a certificate based on the request.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmcert',
            call='issueCertificateRequest',
            args=[self.request_uuid, certificate_subject_name],
        )
        if code:
            raise OSError(out)
        return out

    def deny(self, reason):
        """
        Deny the request.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmcert',
            call='removeCertificateRequests',
            args=[[self.request_uuid], reason],
        )
        if code:
            raise OSError(out)
        if len(out):
            return out[0]
        return False
