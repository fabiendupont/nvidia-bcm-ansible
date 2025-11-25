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

import inspect
import json
from uuid import UUID


class EntityToJSONEncoder(json.JSONEncoder):
    """
    Overload of the default JSON encoder.
    """

    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        if hasattr(obj, "to_dict"):
            return self.default(obj.to_dict())
        if hasattr(obj, "__dict__"):
            d = {
                key: value
                for key, value in inspect.getmembers(obj)
                if (
                    key != '_abc_impl'
                    and not key.startswith("__")
                    and not inspect.isabstract(value)
                    and not inspect.isbuiltin(value)
                    and not inspect.isfunction(value)
                    and not inspect.isgenerator(value)
                    and not inspect.isgeneratorfunction(value)
                    and not inspect.ismethod(value)
                    and not inspect.ismethoddescriptor(value)
                    and not inspect.isroutine(value)
                )
            }
            return self.default(d)
        return obj
