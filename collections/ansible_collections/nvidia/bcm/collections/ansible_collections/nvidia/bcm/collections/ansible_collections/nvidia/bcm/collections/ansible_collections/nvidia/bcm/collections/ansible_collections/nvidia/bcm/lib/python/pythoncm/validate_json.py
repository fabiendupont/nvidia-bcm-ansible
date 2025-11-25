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
import logging

LOGGER = logging.getLogger(__name__)


class ValidateJSON:
    """
    Validate an JSON string (no schema for now)
    """

    @classmethod
    def check(cls, data: str, validate: str | None = None) -> bool:
        try:
            json.loads(data)
            return True
        except Exception as e:
            LOGGER.error(f"JSON validation failed:\n {data}\n{e}")
            return False
