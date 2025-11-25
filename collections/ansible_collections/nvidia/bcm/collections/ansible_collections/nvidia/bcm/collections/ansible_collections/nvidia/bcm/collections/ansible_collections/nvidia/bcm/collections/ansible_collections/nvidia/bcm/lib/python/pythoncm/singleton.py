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

"""
Module offering the Singleton class.


This class can be used as the C{__metaclass__} class field to ensure only a
single instance of the class gets used in the run of an application or
script.

>>> class A(object):
...     __metaclass__ = Singleton

@author: Andy Georges (Ghent University)
"""


class Singleton(type):
    """Serves as  metaclass for classes that should implement the Singleton pattern.

    See https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python
    """

    _instances: typing.ClassVar[dict[type, object]] = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
