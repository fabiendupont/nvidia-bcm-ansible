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


class Service:
    """
    Wrapper class to manage entities supplied by cmdaemon
    """

    def __init__(self, proxy, name, plural=None, by_uuids=False, owner=False, multi=False, get_one_extra_args=None):
        self.proxy = proxy
        self.name = name
        self.by_uuids = by_uuids
        self.owner = owner
        self.multi = multi
        if plural is None:
            self.plural = name + 's'
        else:
            self.plural = plural
        if get_one_extra_args is None:
            self.get_one_extra_args = []
        else:
            self.get_one_extra_args = get_one_extra_args

    def get_one(self):
        return f'get{self.name}'

    def get_all(self):
        return f'get{self.plural}'

    def add_one(self):
        return f'add{self.name}'

    def update_one(self):
        return f'update{self.name}'

    def remove_one(self):
        return f'remove{self.name}'

    def used_by_one(self):
        return f'queryRemove{self.name}'

    def validate_one(self):
        return f'validate{self.name}'

    def get_by_uuids(self):
        if self.by_uuids:
            return f'get{self.plural}ByUuids'
        return None

    def add_multi(self):
        if not self.multi:
            raise TypeError(f'Entity {self.name} does not support multi add/remove')
        return f'add{self.plural}'

    def update_multi(self):
        if not self.multi:
            raise TypeError(f'Entity {self.name} does not support multi add/remove')
        return f'update{self.plural}'

    def remove_multi(self):
        if not self.multi:
            raise TypeError(f'Entity {self.name} does not support multi add/remove')
        return f'remove{self.plural}'

    def used_by_multi(self):
        if not self.multi:
            raise TypeError(f'Entity {self.name} does not support multi add/remove')
        return f'queryRemove{self.plural}'
