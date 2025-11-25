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

import re
import string
from enum import IntEnum
from enum import auto
from uuid import UUID

from pythoncm.util import etc_file
from pythoncm.util import is_valid_ipv4_address
from pythoncm.util import is_valid_ipv6_address
from pythoncm.validate_json import ValidateJSON
from pythoncm.validate_xml import ValidateXML


class MetaData:
    re_domain = re.compile(
        r"((([a-z]{1,2})|([0-9]{1,2})|([a-z0-9]{1,2})|([a-z0-9][a-z0-9-]{1,61}[a-z0-9]))\.)+[a-z]{2,6}"
    )
    re_hostname = re.compile(
        r"([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])(\.([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9\-]{0,61}[a-zA-Z0-9]))*"
    )

    class Type(IntEnum):
        BOOL = auto()
        INT = auto()
        UINT = auto()
        FLOAT = auto()
        STRING = auto()
        RESOLVE = auto()
        ENTITY = auto()
        TIMESTAMP = auto()
        ENUM = auto()
        ELEMENT_OF = auto()
        JSON = auto()
        UUID = auto()

    def __init__(self):
        self.fields = []

    def add(self, field):
        self.fields.append(field)

    def remove(self, name):
        self.fields = [field for field in self.fields if field.name != name]

    def get_all_names(self):
        return {field.name for field in self.fields}

    def get_by_name(self, name):
        try:
            return next(field for field in self.fields if field.name == name)
        except Exception:
            return None

    def get_by_type(self, kind, vector=None):
        return [
            field for field in self.fields if (field.kind == kind) and ((vector is None) or (field.vector == vector))
        ]

    @classmethod
    def check_kind(cls, field, value, __recursive=True):
        # KDR: do not move to the top, import loop
        from pythoncm.entity.entity import Entity

        if __recursive and field.vector:
            if isinstance(value, list):
                return all(cls.check_kind(field, it, False) for it in value)
            return False
        expected_kind = field.kind
        if expected_kind == cls.Type.BOOL:
            return isinstance(value, bool)
        if expected_kind == cls.Type.INT:
            return isinstance(value, int)
        if expected_kind in {cls.Type.UINT, cls.Type.TIMESTAMP}:
            return (isinstance(value, int)) and (value >= 0)
        if expected_kind == cls.Type.ELEMENT_OF:
            if isinstance(value, UUID):
                return field.entity_allow_null or value != UUID(int=0)
            if field.instance is None:
                return isinstance(value, Entity)
            if value is None:
                return field.entity_allow_null
            if isinstance(value, Entity):
                return value.check_type(field.instance)
            raise TypeError(f"{value=!r} is not Entity")
        if expected_kind == cls.Type.FLOAT:
            return isinstance(value, int | float)
        if expected_kind == cls.Type.STRING:
            if not isinstance(value, str):
                return False
            if field.regex_check is not None:
                return re.match(field.regex_check, value) is not None
            if field.function_check is not None:
                return field.function_check(value)
            return True
        if expected_kind == cls.Type.ENUM:
            return isinstance(value, field.enum_type)
        if expected_kind == cls.Type.ENTITY:
            if value is None:
                return field.entity_allow_null
            if field.instance is None:
                return isinstance(value, Entity)
            return value.check_type(field.instance)
        if expected_kind == cls.Type.RESOLVE:
            if isinstance(value, UUID):
                return field.entity_allow_null or value != UUID(int=0)
            if value is not None and field.instance is not None:
                return value.check_type(field.instance)
            if value is None and field.entity_allow_null:
                return True
        elif expected_kind == cls.Type.JSON:
            return value is None or isinstance(value, dict | list | str | int | float | bool)
        elif expected_kind == cls.Type.UUID:
            return isinstance(value, UUID)
        return False

    @classmethod
    def check_isDomain(cls, value):
        return cls.re_domain.match(value)

    @classmethod
    def check_isDomainWithIndex(cls, value):
        idx = value.find(":")
        if idx < 0:
            return cls.check_isDomain(value)
        if idx + 1 == len(value):
            return False
        return cls.check_isDomain(value[0:idx]) and value[idx:1:].isdigit()

    @classmethod
    def check_isIPv4or6orHostname(cls, value):
        return cls.check_isIPv4or6(value) or cls.re_hostname.match(value)

    @classmethod
    def check_isIPv4or6(cls, value):
        return cls.check_isIPv4(value) or cls.check_isIPv6(value)

    @classmethod
    def check_isIPv4(cls, value):
        return is_valid_ipv4_address(value)

    @classmethod
    def check_isIPv6(cls, value, allow_ip_v4=True):
        return is_valid_ipv6_address(value) or (allow_ip_v4 and is_valid_ipv4_address(value))

    @classmethod
    def check_isIP(cls, value):
        return cls.check_isIPv4or6(value)

    @classmethod
    def check_isCIDR(cls, value, allow_ip_v4=True, allow_ip_v6=True):
        if not isinstance(value, str):
            return False
        words = value.split('/')
        if len(words) != 2:
            return False
        if not all(it.isdigit() for it in words[1]):
            return False
        mask = int(words[1])
        return (allow_ip_v4 and is_valid_ipv4_address(words[0]) and 0 <= mask <= 32) or (
            allow_ip_v6 and is_valid_ipv6_address(words[0]) and 0 <= mask <= 128
        )

    @classmethod
    def check_isMAC(cls, value):
        if not isinstance(value, str):
            return False
        if not bool(value) or not all(c in set(string.hexdigits + ':') for c in value):
            return False
        return all(len(it) == 2 for it in value.split(':'))

    @classmethod
    def check_isEmail(cls, value):
        if not isinstance(value, str):
            return False
        if len(value) == 0:
            return True
        if "@" not in value:
            return False
        name, domain = value.split("@", 1)
        if len(name) == 0 or len(domain) == 0 or not cls.check_isDomain(domain):
            return False
        return "\t" not in name and "\r" not in name and "\n" not in name

    @classmethod
    def check_is_raid_configuration(cls, value: str | bytes) -> bool:
        filename = etc_file('raid.xsd')
        return (not value) or ValidateXML.check(value, filename)

    @classmethod
    def check_is_disk_setup(cls, value: str | bytes) -> bool:
        filename = etc_file('disks.xsd')
        return (not value) or ValidateXML.check(value, filename)

    @classmethod
    def check_is_bios_setup(cls, value: str | bytes) -> bool:
        return (not value) or ValidateJSON.check(value)
