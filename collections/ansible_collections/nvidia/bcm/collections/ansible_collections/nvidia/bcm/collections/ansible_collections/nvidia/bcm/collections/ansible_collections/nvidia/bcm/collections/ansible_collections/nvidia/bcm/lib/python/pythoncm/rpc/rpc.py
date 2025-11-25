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

import gzip
import json
import typing
import urllib.error
import urllib.request

from pythoncm.entity_to_json_encoder import EntityToJSONEncoder
from pythoncm.rpc.https_client import HTTPSClientAuthHandler
from pythoncm.rpc.rpc_timeouts import RPCTimeouts


class RPC:
    """
    Wrapper class to make cmdaemon RPC
    """

    OK = 0
    LOGIN_ERROR = -97
    JSON_ERROR = -98
    URL_ERROR = -99
    GENERIC_ERROR = -100
    HTTP_SERVICE_RESTRICTED = 635
    HTTP_RPC_RESTRICTED = 640

    def __init__(self, settings):
        self.settings = settings
        if self.settings.use_proxy:
            self.opener = urllib.request.build_opener(HTTPSClientAuthHandler(self.settings))
        else:
            self.opener = urllib.request.build_opener(
                HTTPSClientAuthHandler(self.settings),
                urllib.request.ProxyHandler({}),
            )

    def call(
        self,
        service: str,
        call: str,
        args: list[str] | None = None,
        minify: bool = True,
        timeout: float | None = None,
        **kwargs,
    ) -> tuple[int, typing.Any]:
        """
        Make a remote procedure call to the specified proxy service.
        """
        if args is None:
            args = []
        data = {
            'service': service,
            'call': call,
            'minify': minify,
            'args': args,
        }
        data.update(kwargs)
        if timeout is None:
            timeout = RPCTimeouts.get(service, call)
        return self._call(data, timeout)

    def __url(self, path: str = 'json') -> str:
        proto = "https" if self.settings.is_ssl() else "http"
        return f'{proto}://{self.settings.host}:{self.settings.port:d}/{path}'

    def get(
        self,
        path: str,
        timeout: float | None = None,
    ) -> tuple[int, str]:
        return self._call(path, timeout)

    def get_cookie(
        self,
        data: dict[str, typing.Any],
        timeout: float | None = None,
    ) -> tuple[int, str]:
        return self._call(data, timeout, 'Set-cookie')

    def _call(
        self,
        data: str | dict[str, typing.Any],
        timeout: float | None = None,
        getheader: str | None = None,
    ) -> tuple[int, str | dict[str, typing.Any] | typing.Any]:
        try:
            compressed = False
            if isinstance(data, dict):
                jsondata = json.dumps(
                    data,
                    cls=EntityToJSONEncoder,
                    ensure_ascii=True,
                ).encode('ascii')
                if self.settings.compression and len(jsondata) >= self.settings.min_compression_size:
                    jsondata = gzip.compress(jsondata)
                    compressed = True
                request = urllib.request.Request(self.__url(), jsondata)
            else:
                request = urllib.request.Request(self.__url(data))
            request.add_header('Content-Type', 'application/json')
            if compressed:
                request.add_header('Content-Encoding', 'gzip')
            if self.settings.compression:
                request.add_header('Accept-Encoding', 'gzip, deflate')
            if self.settings.cookie is not None:
                request.add_header('Cookie', self.settings.cookie)
            response = self.opener.open(request, timeout=timeout)
            response_data = response.read()
            if response.info().get('Content-Encoding') == 'gzip':
                response_data = gzip.decompress(response_data)
            response_data = response_data.decode('utf-8')
            if isinstance(data, str):
                return self.OK, response_data
            if getheader is None:
                return self.OK, json.loads(response_data)
            cookie = response.getheader(getheader, None)
            if cookie is None:
                return self.LOGIN_ERROR, json.loads(response_data)
            return self.OK, response.getheader(getheader, None)
        except ValueError as e:
            return self.JSON_ERROR, str(e)
        except urllib.error.HTTPError as e:
            return e.code, e.reason
        except urllib.error.URLError as e:
            return self.URL_ERROR, e.reason
        except Exception as e:
            return self.GENERIC_ERROR, str(e)
