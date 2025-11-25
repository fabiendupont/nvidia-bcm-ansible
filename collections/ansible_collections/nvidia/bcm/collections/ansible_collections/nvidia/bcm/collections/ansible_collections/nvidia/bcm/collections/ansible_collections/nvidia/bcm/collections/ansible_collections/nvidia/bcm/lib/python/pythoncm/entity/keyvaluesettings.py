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

from pythoncm.entity.entity import Entity


class KeyValueSettings(Entity):
    def _check_key(self, key: str) -> None:
        if len(key) == 0 or key[0] == ' ' or key[-1] == ' ':
            raise ValueError

    def _index(self, key: str) -> int:
        """
        Get the index in the array of key-value pairs with the desired key
        """
        self._check_key(key)
        indexes = [idx for idx, value in enumerate(self.keyValues) if value.split('=')[0] == key]
        if len(indexes) == 1:
            return indexes[0]
        raise KeyError

    def set(self, key: str, value: str, update: bool = True) -> bool:
        """
        Set our update a key=value pair
        """
        try:
            index = self._index(key)
            if not update:
                return False
            self.keyValues[index] = f'{key}={value}'
        except KeyError:
            self.keyValues.append(f'{key}={value}')
        return True

    def get(self, key: str) -> str:
        """
        Get the value of the desired key
        If not found an error is raises
        """
        return self.keyValues[self._index(key)].split('=', 1)[1]

    def clear(self, key: str) -> None:
        """
        Clear the entry that matches he desired key
        If not found an error is raises
        """
        del self.keyValues[self._index(key)]

    def from_dict(self, key_values: dict):
        """
        Copy all key: value from a dictionary into the key=value pars
        """
        map(self._check_key, key_values.keys())
        self.keyValues = [f'{key}={value}' for key, value in key_values.items()]

    def as_dict(self) -> dict:
        """
        Return all key-value pairs as dict
        """
        return dict(it.split('=', 1) for it in self.keyValues)
