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

import http.client
from urllib import request


class HTTPSClientAuthHandler(request.HTTPSHandler):
    def __init__(self, settings):
        super().__init__()
        self.settings = settings

    def https_open(self, req: request.Request) -> http.client.HTTPResponse:
        return self.do_open(self.getConnection, req)

    def getConnection(self, host: str, timeout=120) -> http.client.HTTPSConnection:
        return http.client.HTTPSConnection(
            host,
            context=self.settings.context,
            timeout=timeout,
        )
