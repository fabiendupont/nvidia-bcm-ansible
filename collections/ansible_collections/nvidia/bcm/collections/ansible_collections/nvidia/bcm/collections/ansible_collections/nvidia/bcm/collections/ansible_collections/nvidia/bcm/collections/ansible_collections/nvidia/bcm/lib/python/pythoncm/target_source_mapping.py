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

import itertools
import operator

from tabulate import tabulate

from pythoncm.entity.entity import Entity


class TargetSourceMapping:
    """
    Helper class to display source, target node relationships.
    """

    TARGET = 0
    SOURCE = 1

    def __init__(self, cluster, target, source):
        self.cluster = cluster
        self.target_source = list(zip(target, source))

    def get_sources(self, target):
        """
        Get all possible sources for a specific target
        """
        if isinstance(target, Entity):
            target = target.uuid
        return [it[1] for it in self.target_source if it[0] == target]

    def get_targets(self, source):
        """
        Get all possible targets for a specific source
        """
        if isinstance(source, Entity):
            source = source.uuid
        return [it[0] for it in self.target_source if it[1] == source]

    def group(self, grouping=TARGET):
        """
        Create a dictionary grouped by source or target
        """
        target_source = sorted(self.target_source, key=operator.itemgetter(grouping, 1 - grouping))
        return {
            key: [v[1 - grouping] for v in values]
            for (key, values) in itertools.groupby(target_source, operator.itemgetter(grouping))
        }

    def to_string(self, grouping=TARGET, table_format='rst', showindex='default', header=None):
        """
        Create a nice easy to print table.
        """
        if header is None:
            if grouping == self.SOURCE:
                headers = ['Source', 'Target']
            else:
                headers = ['Target', 'Source']
        else:
            headers = []
        grouped = self.group(grouping)
        data = [
            [self.cluster.resolve_name_by_uuid(key), [self.cluster.resolve_name_by_uuid(v) for v in values]]
            for (key, values) in grouped.items()
        ]
        return tabulate(data, tablefmt=table_format, showindex=showindex, headers=headers)
