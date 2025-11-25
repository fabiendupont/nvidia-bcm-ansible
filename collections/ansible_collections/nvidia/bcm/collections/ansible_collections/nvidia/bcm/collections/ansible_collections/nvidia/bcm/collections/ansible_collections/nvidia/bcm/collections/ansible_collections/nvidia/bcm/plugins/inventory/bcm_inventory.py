#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright: (c) NVIDIA Corporation
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
    name: bcm_inventory
    plugin_type: inventory
    short_description: NVIDIA Base Command Manager (BCM) dynamic inventory plugin
    description:
        - Queries NVIDIA Base Command Manager for cluster nodes
        - Automatically groups nodes by categories and custom attributes
        - Provides node facts as host variables
    options:
        plugin:
            description: Name of the plugin
            required: true
            choices: ['nvidia.bcm.bcm_inventory', 'bcm_inventory']
        host:
            description: BCM head node hostname or IP
            required: false
            default: localhost
        pythoncm_path:
            description: Path to pythoncm library if not in default location
            required: false
            default: /cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages
        group_by_category:
            description: Create groups based on node categories
            type: bool
            required: false
            default: true
        group_by_role:
            description: Create groups based on node roles
            type: bool
            required: false
            default: true
        compose:
            description: Create additional host variables using Jinja2 expressions
            type: dict
            required: false
            default: {}
        keyed_groups:
            description: Create groups based on host variables
            type: list
            required: false
            default: []
        strict:
            description: If true, skip hosts with missing variables
            type: bool
            required: false
            default: false
'''

EXAMPLES = r'''
# Minimal example
plugin: nvidia.bcm.bcm_inventory

# Full example with grouping options
plugin: nvidia.bcm.bcm_inventory
host: localhost
pythoncm_path: /cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages
group_by_category: true
group_by_role: true

# Example with custom grouping
plugin: nvidia.bcm.bcm_inventory
keyed_groups:
  - key: bcm_category
    prefix: category
  - key: bcm_status
    prefix: status
compose:
  ansible_host: bcm_hostname
'''

import sys
from ansible.plugins.inventory import BaseInventoryPlugin, Constructable
from ansible.errors import AnsibleError


class InventoryModule(BaseInventoryPlugin, Constructable):
    NAME = 'nvidia.bcm.bcm_inventory'

    def verify_file(self, path):
        """Verify that the source file is valid for this plugin"""
        if super(InventoryModule, self).verify_file(path):
            if path.endswith(('bcm.yml', 'bcm.yaml', 'bcm_inventory.yml', 'bcm_inventory.yaml')):
                return True
        return False

    def parse(self, inventory, loader, path, cache=True):
        """Parse the inventory file and populate inventory"""
        super(InventoryModule, self).parse(inventory, loader, path, cache)

        # Read the config
        self._read_config_data(path)

        # Get configuration options
        pythoncm_path = self.get_option('pythoncm_path')
        group_by_category = self.get_option('group_by_category')
        group_by_role = self.get_option('group_by_role')

        # Add pythoncm to path if needed
        if pythoncm_path and pythoncm_path not in sys.path:
            sys.path.insert(0, pythoncm_path)

        try:
            import pythoncm
            from pythoncm.cluster import Cluster
        except ImportError as e:
            raise AnsibleError(
                f"Failed to import pythoncm. Please ensure cmdaemon-pythoncm is installed.\n"
                f"Error: {e}\n"
                f"Tried path: {pythoncm_path}"
            )

        try:
            # Connect to BCM
            cluster = Cluster()

            # Get all devices (nodes)
            devices = cluster.get_by_type('Device')

            # Process each device
            for device in devices:
                # Get device attributes using Entity API
                hostname = device.hostname if hasattr(device, 'hostname') else 'unknown'

                # Add host to inventory
                self.inventory.add_host(hostname)

                # Add host variables
                self.inventory.set_variable(hostname, 'bcm_uuid', str(device.uuid) if hasattr(device, 'uuid') else None)
                self.inventory.set_variable(hostname, 'bcm_hostname', device.hostname if hasattr(device, 'hostname') else None)
                self.inventory.set_variable(hostname, 'bcm_mac', device.mac if hasattr(device, 'mac') else None)
                self.inventory.set_variable(hostname, 'bcm_type', device.childType if hasattr(device, 'childType') else None)
                self.inventory.set_variable(hostname, 'bcm_partition', str(device.partition) if hasattr(device, 'partition') else None)

                # Get IP from first interface if available
                ip_address = None
                if hasattr(device, 'interfaces') and device.interfaces:
                    for iface in device.interfaces:
                        if hasattr(iface, 'ip') and iface.ip and iface.ip != '0.0.0.0':
                            ip_address = iface.ip
                            break
                self.inventory.set_variable(hostname, 'bcm_ip', ip_address)

                # Group by device type
                if hasattr(device, 'childType') and device.childType:
                    group_name = f"type_{device.childType}"
                    self.inventory.add_group(group_name)
                    self.inventory.add_child(group_name, hostname)

                # Set ansible_host if we have an IP
                if ip_address:
                    self.inventory.set_variable(hostname, 'ansible_host', ip_address)

                # Use constructable methods for additional grouping
                strict = self.get_option('strict')
                self._set_composite_vars(
                    self.get_option('compose'),
                    self.inventory.get_host(hostname).get_vars(),
                    hostname,
                    strict=strict
                )

                self._add_host_to_keyed_groups(
                    self.get_option('keyed_groups'),
                    self.inventory.get_host(hostname).get_vars(),
                    hostname,
                    strict=strict
                )

        except Exception as e:
            raise AnsibleError(f"Failed to query BCM cluster: {e}")
