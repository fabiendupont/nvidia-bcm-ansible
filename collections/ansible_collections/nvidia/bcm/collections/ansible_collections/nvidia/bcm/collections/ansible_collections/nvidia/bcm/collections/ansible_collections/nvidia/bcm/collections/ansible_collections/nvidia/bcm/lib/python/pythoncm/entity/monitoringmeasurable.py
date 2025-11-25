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


class MonitoringMeasurable(Entity):
    NO_DATA = 'no data'

    @property
    def resolve_name(self) -> str:
        """
        Special case for the name if a parameter is defined
        """
        if not self.parameter:
            return self.name

        return self.name + ':' + self.parameter

    @classmethod
    def __translate_prometheus_name(cls, name):
        name = name.lower()
        for illegal in ('::', '.', '-', ' ', '~', '@'):
            name = name.replace(illegal, '_')
        return name

    @property
    def prometheus_name(self) -> str:
        """
        Translate Bright name to Prometheus
        """
        name = self.__translate_prometheus_name(self.name)
        if self.parameter:
            name += '_' + self.__translate_prometheus_name(self.parameter)
        return name

    def value_to_string(self, value: str) -> str:
        return value

    def is_metric(self) -> bool:
        return False

    def is_healthcheck(self) -> bool:
        return False

    def is_enum_metric(self) -> bool:
        return False
