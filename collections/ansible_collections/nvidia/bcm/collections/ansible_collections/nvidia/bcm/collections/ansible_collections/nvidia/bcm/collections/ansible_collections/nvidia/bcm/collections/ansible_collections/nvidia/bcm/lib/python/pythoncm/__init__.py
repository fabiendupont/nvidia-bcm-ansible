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

import logging
from sys import version_info

assert (version_info.major, version_info.minor) >= (3, 9)


# Configure Null logger to avoid prints with "No handler"
if not any(isinstance(handler, logging.NullHandler) for handler in logging.getLogger().handlers):
    logging.getLogger().addHandler(logging.NullHandler())
