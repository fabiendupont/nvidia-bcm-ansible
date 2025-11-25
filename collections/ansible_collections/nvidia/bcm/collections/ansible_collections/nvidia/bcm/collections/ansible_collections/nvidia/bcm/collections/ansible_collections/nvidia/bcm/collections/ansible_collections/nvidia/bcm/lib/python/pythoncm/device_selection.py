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
from uuid import UUID

from pythoncm.entity import NodeGroup
from pythoncm.entity.category import Category
from pythoncm.entity.computenode import ComputeNode
from pythoncm.entity.configurationoverlay import ConfigurationOverlay
from pythoncm.entity.device import Device
from pythoncm.entity.node import Node
from pythoncm.namerange.expand import Expand


class DeviceSelection:
    """
    Helper class to create a list of nodes or devices.
    """

    def __init__(self, cluster, only_nodes=False):
        self.cluster = cluster
        self.only_nodes = only_nodes
        self.selected = set()

    def get_sorted_by_name(self):
        """
        Sort by hostname
        """
        return sorted(self.selected, key=lambda it: it.resolve_name, reverse=False)

    def union(self, device_selection):
        """
        Update the current selection by calculating the union with the provided selection.
        """
        if not isinstance(device_selection, DeviceSelection):
            raise TypeError('Union can only be calculated on two device selections')
        result = DeviceSelection(
            self.cluster,
            self.only_nodes or device_selection.only_nodes,
        )
        result.selected = self.selected.union(device_selection.selected)
        return result

    def intersection(self, device_selection):
        """
        Update the current selection by calculating the intersection with the provided selection.
        """
        if not isinstance(device_selection, DeviceSelection):
            raise TypeError('Union can only be calculated on two device selections')
        result = DeviceSelection(
            self.cluster,
            self.only_nodes and device_selection.only_nodes,
        )
        result.selected = self.selected.intersection(device_selection.selected)
        return result

    def _get_devices_from_list(self, devices, ignore_invalid=False):
        result = (
            [it for it in devices if isinstance(it, Device)]
            + self.cluster.get_by_uuid([it for it in devices if isinstance(it, UUID)])
            + ([self.cluster.get_by_name(it, 'Device') for it in devices if isinstance(it, str)])
        )
        result = [it for it in result if it is not None]
        if not ignore_invalid and (len(result) != len(devices)):
            raise ValueError('Invalid devices specified')
        if self.only_nodes:
            result = [it for it in devices if isinstance(it, Node)]
        return result

    def __get_typed_entity(self, entity, instance_type):
        if isinstance(entity, UUID):
            entity = self.cluster.get_by_uuid(entity)
            if entity is None:
                raise ValueError(f'Unable to find {instance_type.__name__} by key')
        elif isinstance(entity, str):
            entity = self.cluster.get_by_name(entity, instance_type.__name__)
            if entity is None:
                raise ValueError(f'Unable to find {instance_type.__name__} by string')
        if not isinstance(entity, instance_type):
            raise TypeError(f'No {instance_type.__name__} specified')
        return entity

    def _get_nodes_in_category(self, category):
        category = self.__get_typed_entity(
            entity=category,
            instance_type=Category,
        )
        compute_nodes = self.cluster.get_by_type(ComputeNode)
        return [it for it in compute_nodes if it.category == category]

    def _get_nodes_in_nodegroup(self, nodegroup):
        nodegroup = self.__get_typed_entity(
            entity=nodegroup,
            instance_type=NodeGroup,
        )
        return nodegroup.nodes

    def _get_nodes_in_configuration_overlay(self, configuration_overlay):
        configuration_overlay = self.__get_typed_entity(
            entity=configuration_overlay,
            instance_type=ConfigurationOverlay,
        )
        category_nodes = [self._get_nodes_in_category(it) for it in configuration_overlay.categories]
        return configuration_overlay.nodes + list(itertools.chain.from_iterable(category_nodes))

    def add_device(self, device, ignore_invalid=False):
        """
        Add a single device to the selection.
        """
        self.add_devices([device], ignore_invalid)

    def remove_device(self, device, ignore_invalid=False):
        """
        Remove a single device to the selection.
        """
        self.remove_devices([device], ignore_invalid)

    def add_devices(self, devices, ignore_invalid=False):
        """
        Add one or more device to the selection.
        """
        devices = self._get_devices_from_list(devices, ignore_invalid)
        if devices is not None:
            self.selected.update(devices)

    def remove_devices(self, devices, ignore_invalid=False):
        """
        Remove one or more device to the selection.
        """
        devices = self._get_devices_from_list(devices, ignore_invalid)
        if devices is not None:
            self.selected.difference_update(devices)

    def add_category(self, category):
        """
        Add all nodes which use the specified category to the selection.
        """
        nodes = self._get_nodes_in_category(category)
        self.selected.update(nodes)

    def remove_category(self, category):
        """
        Remove all nodes which use the specified category to the selection.
        """
        nodes = self._get_nodes_in_category(category)
        self.selected.difference_update(nodes)

    def add_nodegroup(self, nodegroup):
        """
        Add all nodes contained in the specified node group to the selection.
        """
        nodes = self._get_nodes_in_nodegroup(nodegroup)
        self.selected.update(nodes)

    def remove_nodegroup(self, nodegroup):
        """
        Remove all nodes contained in the specified node group to the selection.
        """
        nodes = self._get_nodes_in_nodegroup(nodegroup)
        self.selected.difference_update(nodes)

    def add_configuration_overlay(self, configuration_overlay):
        """
        Add all nodes contained in the specified configuration overlay to the selection.
        """
        nodes = self._get_nodes_in_configuration_overlay(configuration_overlay)
        self.selected.update(nodes)

    def remove_configuration_overlay(self, configuration_overlay):
        """
        Remove all nodes contained in the specified configuration overlay to the selection.
        """
        nodes = self._get_nodes_in_configuration_overlay(configuration_overlay)
        self.selected.difference_update(nodes)

    def add_devices_in_text_range(self, text_range):
        """
        Add all devices by text range to the selection
        """
        devices = self._get_devices_from_list(Expand.expand(text_range))
        self.selected.update(devices)

    def remove_devices_in_text_range(self, text_range):
        """
        Add all devices by text range to the selection
        """
        devices = self._get_devices_from_list(Expand.expand(text_range))
        self.selected.difference_update(devices)
