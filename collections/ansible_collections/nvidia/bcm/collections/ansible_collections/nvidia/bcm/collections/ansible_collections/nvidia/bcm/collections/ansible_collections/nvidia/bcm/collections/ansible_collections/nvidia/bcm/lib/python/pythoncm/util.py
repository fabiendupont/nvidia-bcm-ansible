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
import socket
import typing
from datetime import datetime
from uuid import UUID

if typing.TYPE_CHECKING:
    from collections.abc import Hashable
    from collections.abc import Iterable


def contains(vector, element, case_insensitive=True):
    if not case_insensitive or (not isinstance(element, str) and not isinstance(element, bytes)):
        return element in vector

    return element.lower() in tuple(it.lower() for it in vector)


def name_compare(a: str, b: str) -> int | None:
    """
    Compare the names of two entities.
    Exact, case insensitive and without spaces.
    """
    if a == b:
        return 0
    a = a.lower()
    b = b.lower()
    if a == b:
        return 1
    a = a.replace(' ', '')
    b = b.replace(' ', '')
    if a == b:
        return 2
    return None


def lower_no_space(value: str) -> str:
    return value.lower().replace(" ", "")


def format_time_stamp(value, now=None, time_format=None, latest=False, relative=False):
    """
    Print date or timespan
    """
    if latest:
        value = now - value
        try:
            import humanfriendly

            return humanfriendly.format_timespan(value)
        except ImportError:
            return f"{value:8.5f}s"
    elif relative:
        try:
            import humanfriendly

            return humanfriendly.format_timespan(value)
        except ImportError:
            return f"{value:8.5f}s"
    else:
        return datetime.fromtimestamp(int(value)).strftime(time_format)


def format_milli_seconds_time_stamp(value, now=None, time_format=None, latest=False, relative=False):
    """
    Print date or timespan, supplied in milliseconds
    """
    return format_time_stamp(
        value / 1000.0,
        now=now,
        time_format=time_format,
        latest=latest,
        relative=relative,
    )


def etc_file(filename=''):
    path = os.path.realpath(__file__)
    while path != '/':
        path = os.path.dirname(path)
        etc_file = os.path.join(path, 'etc', filename)
        if os.path.exists(etc_file):
            return etc_file
    return None


def is_valid_ipv4_address(address: str | None) -> bool:
    if address is None:
        return False
    try:
        socket.inet_pton(socket.AF_INET, address)
    except TypeError:  # address not a str
        return False
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except OSError:
            return False
        return address.count('.') == 3
    except OSError:  # not a valid address
        return False
    return True


def is_valid_ipv6_address(address: str | None) -> bool:
    if address is None:
        return False
    try:
        socket.inet_pton(socket.AF_INET6, address)
    except TypeError:  # address not a str
        return False
    except AttributeError:  # no inet_pton here, sorry
        try:
            socket.inet_aton(address)
        except OSError:
            return False
        return address.count(':') == 7
    except OSError:  # not a valid address
        return False
    return True


def unique(series: Iterable[Hashable | list[Hashable]]) -> list:
    return list({tuple(it) if isinstance(it, list) else it for it in series})


def uuid_compare(lhs: UUID | str, rhs: UUID | str) -> bool:
    if type(lhs) is type(rhs):
        return lhs == rhs
    if isinstance(lhs, str):
        return UUID(lhs) == rhs
    return UUID(rhs) == lhs


def uuid_list_compare(lhs: list[UUID | str], rhs: list[UUID | str]) -> bool:
    if len(lhs) == len(rhs):
        return all(map(uuid_compare, lhs, rhs))
    return False


def convert_to_uuid(value):
    from pythoncm.entity.entity import Entity

    if isinstance(value, Entity):
        return value.uuid
    if isinstance(value, UUID):
        return value
    if isinstance(value, int):
        return UUID(int=value)
    if isinstance(value, str):
        try:
            return UUID(value)
        except ValueError:
            pass
    if isinstance(value, list):
        return [convert_to_uuid(it) for it in value]
    return UUID(int=0)
