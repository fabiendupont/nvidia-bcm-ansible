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

import json
import os
import ssl
from urllib import parse as urllib_parse

from pythoncm.rpc.rpc import RPC
from pythoncm.util import is_valid_ipv4_address


class Settings:
    """
    Defines the settings for connectivity to the cluster.
    """

    def __init__(
        self,
        host: str | None = None,
        port: int = 8081,
        cert_file: str | None = None,
        key_file: str | None = None,
        ca_file: str | None = None,
        check_hostname: bool = False,
        use_proxy: bool = False,
        force_ssl: bool = False,
        compression: bool = False,
        min_compression_size: int = 512,
    ):
        self.host = host
        self.port = port
        self.cert_file = cert_file
        self.key_file = key_file
        self.ca_file = ca_file
        self.check_hostname = check_hostname
        self.use_proxy = use_proxy
        self.cookie = None
        self.force_ssl = force_ssl
        self.compression = compression
        self.min_compression_size = min_compression_size
        if (self.ca_file is None) or not os.path.exists(self.ca_file):
            self.context = ssl.create_default_context()
        else:
            self.context = ssl.create_default_context(cafile=self.ca_file)
        self.context.check_hostname = self.check_hostname and not is_valid_ipv4_address(self.host)
        if self.check_certificate_files():
            self.context.verify_mode = ssl.CERT_REQUIRED
            self.context.load_cert_chain(self.cert_file, self.key_file)
        else:
            self.context.verify_mode = ssl.CERT_NONE
        if self.host is None:
            self.read_url()

    def read_url(self, filename: str = '/var/spool/cmd/my.master.cmd.url') -> bool:
        """
        Parse a file containing a URL to be used to connect to the cluster
        """
        with open(filename, encoding="utf-8") as f:
            url = f.readline()
        parsed_url = urllib_parse.urlparse(url)
        if parsed_url.hostname is None:
            return False
        self.host = parsed_url.hostname
        if parsed_url.port is not None:
            self.port = parsed_url.port
        return True

    def reload_certificate(self) -> None:
        """
        Force reload of certificates.
        Should not be needed except when files were changed on disk.
        """
        context = ssl.create_default_context(cafile=self.ca_file)
        context.check_hostname = self.check_hostname and not is_valid_ipv4_address(self.host)
        context.verify_mode = self.context.verify_mode
        if self.check_certificate_files():
            context.load_cert_chain(self.cert_file, self.key_file)
        self.context = context

    def is_ssl(self) -> bool:
        """
        Check if SSL certificates are set
        """
        return self.force_ssl or (self.ca_file is not None) or (self.cert_file is not None)

    def check_ca_certificate_file(self) -> bool:
        """
        Check if the CA certificate is defined and exists
        """
        return (self.ca_file is not None) and os.path.exists(self.ca_file)

    def check_certificate_files(self) -> bool:
        """
        Check if the certificate and private key are defined and exist
        """
        return (
            (self.cert_file is not None)
            and (self.key_file is not None)
            and os.path.exists(self.cert_file)
            and os.path.exists(self.key_file)
        )

    def save(self, filename: str, mode: int = 0o600) -> bool:
        """
        Save all settings in a small JSON file.
        """
        data = {}
        for field in (
            'host',
            'port',
            'ca_file',
            'check_hostname',
            'cert_file',
            'key_file',
        ):
            data[field] = getattr(self, field)
        try:
            with open(filename, 'w', encoding="utf-8") as f:
                os.chmod(filename, mode)
                f.write(json.dumps(data, ensure_ascii=True))
                return True
        except OSError:
            pass
        return False

    def load(self, filename: str) -> bool:
        """
        Load all settings from a small JSON file.
        """
        try:
            with open(filename, encoding="utf-8") as f:
                data = json.loads(f.read())
                for k, v in data.items():
                    setattr(self, k, v)
            return True
        except ValueError:
            return False
        except OSError:
            return False

    def update_host(self, host: str | None) -> bool:
        """
        Update the host we are connected to, handy in case of IP changes
        """
        if not host:
            return False
        if self.host == host:
            return True
        self.context.check_hostname = self.check_hostname and not is_valid_ipv4_address(self.host)
        self.host = host
        return True

    def get_cookie(self, username: str, password: str) -> bool:
        rpc = RPC(self)
        data = {"service": "login", "username": username, "password": password}
        code, self.cookie = rpc.get_cookie(data)
        return code == rpc.OK and self.cookie is not None

    def get_version(self) -> str:
        rpc = RPC(self)
        _, version = rpc.get('info/version')
        return version
