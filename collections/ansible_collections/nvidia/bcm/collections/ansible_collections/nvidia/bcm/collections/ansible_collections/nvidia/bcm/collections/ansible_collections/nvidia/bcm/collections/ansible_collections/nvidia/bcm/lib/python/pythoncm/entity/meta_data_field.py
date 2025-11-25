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

import abc
import json
import typing
from enum import Enum

import yaml
from lxml import etree
from passlib.hosts import host_context

if typing.TYPE_CHECKING:
    from collections.abc import Callable

    from pythoncm.entity.entity import Entity


class BaseDiff(abc.ABC):
    @abc.abstractmethod
    def diff(self, value1, value2) -> bool:
        pass

    def __call__(self, *args, **kwargs) -> bool:
        return self.diff(*args, **kwargs)


class NoneDiff(BaseDiff):
    def diff(self, value1, value2) -> bool:
        return False


class DefaultDiff(BaseDiff):
    def diff(self, value1, value2) -> bool:
        if type(value1) is not type(value2):
            raise TypeError(f"arguments should of same type found: {type(value1)} and {type(value2)}")
        return value1 != value2


class CryptHashDiff(BaseDiff):
    def diff(self, hashed, plaintext) -> bool:
        if not all(isinstance(val, str) for val in (hashed, plaintext)):
            raise TypeError(f"arguments should str found: {type(hashed)} and {type(plaintext)}")
        hashed = hashed.replace('{CRYPT}', '')
        return not host_context.verify(plaintext, hashed)


class JsonDiff(BaseDiff):
    def diff(self, value1: str, value2: str) -> bool:
        if not all(isinstance(val, str) for val in (value1, value2)):
            raise TypeError(f"arguments should str found: {type(value1)} and {type(value2)}")
        return json.loads(value1) != json.loads(value2)


class YamlDiff(BaseDiff):
    def diff(self, value1: str, value2: str) -> bool:
        if not all(isinstance(val, str) for val in (value1, value2)):
            raise TypeError(f"arguments should str found: {type(value1)} and {type(value2)}")
        return yaml.load(value1, Loader=yaml.SafeLoader) != yaml.load(value2, Loader=yaml.SafeLoader)


class XmlDiff(BaseDiff):
    def diff(self, value1, value2) -> bool:
        if not all(isinstance(val, str) for val in (value1, value2)):
            raise TypeError(f"arguments should str found: {type(value1)} and {type(value2)}")
        xml1 = etree.XML(value1.encode())
        xml2 = etree.XML(value2.encode())
        return etree.tostring(xml1) != etree.tostring(xml2)


class EnumDiff(BaseDiff):
    def diff(self, value1, value2) -> bool:
        if not all(isinstance(val, Enum) for val in (value1, value2)):
            raise TypeError(f"arguments should str found: {type(value1)} and {type(value2)}")
        return value1 != value2


class DisabledDiff(BaseDiff):
    def diff(self, value1, value2) -> bool:
        return False


class _DiffEnum(Enum):
    none = NoneDiff()
    default = DefaultDiff()
    crypt_hash = CryptHashDiff()
    json = JsonDiff()
    yaml = YamlDiff()
    xml = XmlDiff()
    enum = EnumDiff()
    disabled = DisabledDiff()


class MetaDataField(typing.NamedTuple):
    Diff = _DiffEnum

    name: str
    kind: int  # enum ??
    default: typing.Any | None = None
    vector: bool = False
    description: str = ''
    regex_check: str | None = None
    function_check: Callable[[typing.Any], bool] = None
    entity_allow_null: bool = False
    required: bool = False
    options: typing.Any | None = None
    readonly: bool = False
    element_of: typing.Any | None = None
    create_instance: bool = False
    instance: str | None = None
    init_instance: str | None = None
    clone: bool = True
    conditional_clone: Callable[[Entity], bool] | None = None
    internal: bool = False
    diff_type: Diff = Diff.default
    enum_type: Enum | None = None
