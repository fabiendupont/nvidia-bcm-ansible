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

import os
import threading
import typing

from OpenSSL import crypto

from pythoncm.entity.entity import Entity
from pythoncm.util import is_valid_ipv4_address
from pythoncm.util import is_valid_ipv6_address

if typing.TYPE_CHECKING:
    from pythoncm.cluster import Cluster
    from pythoncm.entity_converter import EntityConverter


class Certificate(Entity):
    CLIENT_TYPE_CMSH = 2
    CLIENT_TYPE_NODE = 3
    CLIENT_TYPE_CMGUI = 4
    CLIENT_TYPE_INSTALLER = 5
    CLIENT_TYPE_PYTHON = 6
    CLIENT_TYPE_LITENODE = 7
    CLIENT_TYPE_LITE_INSTALLER = 8
    CLIENT_TYPE_MINIMAL_NODE = 9

    CLIENT_TYPE_LOCAL = 1024
    CLIENT_TYPE_LDAP = CLIENT_TYPE_LOCAL + 1
    CLIENT_TYPE_JUPYTERHUB = CLIENT_TYPE_LOCAL + 2
    CLIENT_TYPE_PRS = CLIENT_TYPE_LOCAL + 3

    CLIENT_TYPE_DYNAMIC = 1 << 31
    CLIENT_TYPE_RANGE_BITS_PER_BLOCK = 16
    CLIENT_TYPE_RANGE_BLOCK_SIZE = 1 << CLIENT_TYPE_RANGE_BITS_PER_BLOCK

    CLIENT_TYPE_KUBERNETES = CLIENT_TYPE_DYNAMIC + (0 * CLIENT_TYPE_RANGE_BLOCK_SIZE)
    CLIENT_TYPE_ETCD = CLIENT_TYPE_DYNAMIC + (1 * CLIENT_TYPE_RANGE_BLOCK_SIZE)
    CLIENT_TYPE_KUBERNETES_USERS = CLIENT_TYPE_DYNAMIC + (2 * CLIENT_TYPE_RANGE_BLOCK_SIZE)
    CLIENT_TYPE_KUBE_SERVICEACCOUNTS = CLIENT_TYPE_DYNAMIC + (3 * CLIENT_TYPE_RANGE_BLOCK_SIZE)

    def __init__(
        self,
        cluster: Cluster | None = None,
        data: dict[str, typing.Any] | None = None,
        service=None,
        converter: EntityConverter | None = None,
        parent: Entity | None = None,
        add_to_cluster: bool = False,
        create_sub_entities: bool = True,
        **kwargs,
    ) -> None:
        # meta is not allowed
        if "meta" in kwargs:
            raise TypeError(f"'meta' is an invalid keyword argument for {self.__class__.__name__}")

        self.PEM: str | bytes | None

        super().__init__(
            cluster=cluster,
            data=data,
            service=service,
            converter=converter,
            parent=parent,
            add_to_cluster=add_to_cluster,
            create_sub_entities=create_sub_entities,
            **kwargs,
        )
        self.private_key = None
        if self.PEM:
            self.certificate: crypto.X509 | None = crypto.load_certificate(crypto.FILETYPE_PEM, self.PEM)
        else:
            self.certificate = None
        self.condition: threading.Condition | None = None

    def valid(self) -> bool:
        """
        Check if the certificate is valid
        """
        return self.certificate is not None

    def info(self) -> None:
        """
        Print some information about the certificate.
        """
        if self.certificate is None:
            print("No certificate")
        else:
            print(f"Subject:   {self.certificate.get_subject().get_components()}")
            print(f"Issuer:    {self.certificate.get_issuer().get_components()}")
            print(f"Serial:    {self.certificate.get_serial_number():d}")
            print(f"Expire:    {self.certificate.get_notAfter()}")
            print(f"Profile:   {self.profile}")
            for extension in self.extensions():
                print(f"Extension: {extension.get_short_name()} {extension.get_data()} {extension.get_critical():d}")

    def save(
        self,
        filename: str,
        uid: int | None = None,
        gid: int | None = None,
        mode: int = 0o600,
        private_key_file: str | None = None,
    ) -> bool:
        """
        Save to file.
        """
        if self.certificate is not None:
            with open(filename, "w", encoding="utf-8") as fd:
                if uid is not None and gid is not None:
                    os.chown(filename, uid, gid)
                os.chmod(filename, mode)
                fd.write(self.PEM)
            if self.private_key is not None and private_key_file is not None:
                with open(private_key_file, "w", encoding="utf-8") as fd:
                    if uid is not None and gid is not None:
                        os.chown(private_key_file, uid, gid)
                    os.chmod(private_key_file, mode)
                    fd.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, self.private_key).decode("utf-8"))
            return True
        return False

    @property
    def key(self) -> bytes | None:
        if self.private_key is not None:
            return crypto.dump_privatekey(crypto.FILETYPE_PEM, self.private_key)
        return None

    def load(self, filename: str) -> bool:
        """
        Load from file.
        """
        with open(filename, encoding="utf-8") as fd:
            self.PEM = fd.read()
            self.certificate = crypto.load_certificate(crypto.FILETYPE_PEM, self.PEM.encode('utf-8'))
            self.profile = self.extract_profile()
            return True

    def extract_profile(self) -> str | None:
        """
        Extract the profile information.
        """
        if self.certificate is None:
            return None
        # KDR: unclear what the first two chars are \x16\x05
        return next(it.get_data()[2:].decode() for it in self.extensions() if not it.get_critical() and it.get_data())

    def extensions(self) -> list[crypto.X509Extension] | None:
        """
        Get all extensions contained in the certificate.
        """
        if self.certificate is None:
            return None
        extensions = []
        for index in range(self.certificate.get_extension_count()):
            extensions.append(self.certificate.get_extension(index))
        return extensions

    def remove(self):
        """
        Remove the certificate.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmcert',
            call='removeCertificate',
            args=[[self.get_serial_number()]],
        )
        if code:
            raise OSError(out)
        return out[0]

    def revoke(self):
        """
        Revoke the certificate.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmcert',
            call='revokeCertificate',
            args=[[self.get_serial_number()]],
        )
        if code:
            raise OSError(out)
        return out[0]

    def unrevoke(self):
        """
        Unrevoke the certificate.
        """
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmcert',
            call='unrevokeCertificate',
            args=[[self.get_serial_number()]],
        )
        if code:
            raise OSError(out)
        return out[0]

    def create(
        self,
        name: str,
        profile,
        system_login_name: str | None = None,
        country: str | None = None,
        state: str | None = None,
        locality: str | None = None,
        organization: str | None = None,
        organizational_unit: str | None = None,
        client_type: int = CLIENT_TYPE_PYTHON,
        valid_for_days: int = 36500,
        private_key_bits: int = 2048,
        component=None,
        alternative_names: str | list[str] | None = None,
        timeout: float | None = None,
    ) -> bool:
        """
        Create a new certificate.
        """

        # CM-18430: load order issue
        from pythoncm.entity import CertificateSubjectName

        # create private key
        self.private_key = crypto.PKey()
        self.private_key.generate_key(crypto.TYPE_RSA, private_key_bits)
        # create certificate signing request
        csr = crypto.X509Req()
        if country:
            csr.get_subject().countryName = country
        if state:
            csr.get_subject().stateOrProvinceName = state
        if locality:
            csr.get_subject().localityName = locality
        if organization:
            csr.get_subject().organizationName = organization
        if organizational_unit:
            csr.get_subject().organizationalUnitName = organizational_unit
        extensions = []
        if alternative_names:
            if not isinstance(alternative_names, list):
                alternative_names = alternative_names.split(',')
            names = []
            for it in alternative_names:
                if it.startswith('IP:') or it.startswith('DNS:'):
                    names.append(it)
                    continue
                if is_valid_ipv4_address(it) or is_valid_ipv6_address(it):
                    names.append(f'IP:{it}')
                names.append(f'DNS:{it}')
            alternative_names = ','.join(names)
            extensions.append(crypto.X509Extension(b'subjectAltName', True, alternative_names.encode('utf-8')))
        if extensions:
            csr.add_extensions(extensions)
        csr.get_subject().CN = name
        csr.set_pubkey(self.private_key)
        # sign with private key
        csr.sign(self.private_key, 'sha1')
        # request to sign it
        rpc = self._cluster.get_rpc()
        (code, out) = rpc.call(
            service='cmcert',
            call='requestCertificate',
            args=[
                crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr).decode("utf-8"),
                self._cluster.session_uuid,
                client_type,
            ],
        )
        if code:
            raise OSError(out)
        self.PEM = None
        self.request_uuid = out
        # register callback
        self.condition = threading.Condition()
        self._cluster._event_handler.certificate_issue_callback = self._issue_callback
        # issue it yourself
        certificate_subject_name = CertificateSubjectName(self._cluster)
        if profile:
            certificate_subject_name.profile = profile
        if system_login_name:
            certificate_subject_name.syslogin = system_login_name
        if component:
            certificate_subject_name.component = component
        certificate_subject_name.days = valid_for_days
        certificate_subject_name.ca = False
        (_code, _out) = rpc.call(
            service='cmcert',
            call='issueCertificateRequest',
            args=[self.request_uuid, certificate_subject_name],
        )
        # wait for the event
        with self.condition:
            if self.PEM is None:
                self.condition.wait(timeout)
            if self.PEM is not None:
                self.certificate = crypto.load_certificate(crypto.FILETYPE_PEM, self.PEM)
                self.certificate.set_pubkey(self.private_key)
                return True
        return False

    def _issue_callback(self, pem: str | bytes | None) -> None:
        with self.condition:
            self.PEM = pem
            self.condition.notify()
