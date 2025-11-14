#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Copyright: (c) NVIDIA Corporation
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

import sys
from ansible.module_utils.basic import AnsibleModule, missing_required_lib


class BCMModule:
    """Base class for BCM Ansible modules with common functionality"""

    def __init__(self, module):
        """
        Initialize BCM module

        Args:
            module: AnsibleModule instance
        """
        self.module = module
        self.pythoncm_path = module.params.get('pythoncm_path',
                                                '/cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages')
        self.cluster = None
        self._ensure_pythoncm()

    def _ensure_pythoncm(self):
        """Ensure pythoncm is available and import it"""
        if self.pythoncm_path and self.pythoncm_path not in sys.path:
            sys.path.insert(0, self.pythoncm_path)

        try:
            import pythoncm
            from pythoncm.cluster import Cluster
            self.pythoncm = pythoncm
            self.Cluster = Cluster
        except ImportError:
            self.module.fail_json(
                msg=missing_required_lib('pythoncm'),
                exception="Please install cmdaemon-pythoncm package"
            )

    def connect(self):
        """Connect to BCM cluster"""
        try:
            self.cluster = self.Cluster()
            return True
        except Exception as e:
            self.module.fail_json(msg=f"Failed to connect to BCM cluster: {str(e)}")
            return False

    def get_device(self, name):
        """
        Get device by name or hostname

        Args:
            name: Device hostname to search for

        Returns:
            Device Entity object or None
        """
        if not self.cluster:
            self.connect()

        try:
            # Try get_by_name first (faster if it works)
            device = self.cluster.get_by_name('Device', name)
            if device:
                return device

            # Fall back to searching all devices by hostname
            devices = self.cluster.get_by_type('Device')
            for device in devices:
                if hasattr(device, 'hostname') and device.hostname == name:
                    return device
            return None
        except Exception as e:
            self.module.fail_json(msg=f"Failed to query device '{name}': {str(e)}")

    def get_all_devices(self, filters=None):
        """
        Get all devices, optionally filtered

        Args:
            filters: Dictionary of attribute filters to apply

        Returns:
            List of Device Entity objects
        """
        if not self.cluster:
            self.connect()

        try:
            devices = self.cluster.get_by_type('Device')

            if filters:
                filtered_devices = []
                for device in devices:
                    match = True
                    for key, value in filters.items():
                        device_value = getattr(device, key, None)
                        if device_value != value:
                            match = False
                            break
                    if match:
                        filtered_devices.append(device)
                return filtered_devices

            return devices
        except Exception as e:
            self.module.fail_json(msg=f"Failed to query devices: {str(e)}")

    def get_category(self, name):
        """
        Get category by name

        Args:
            name: Category name

        Returns:
            Category Entity object or None
        """
        if not self.cluster:
            self.connect()

        try:
            # get_by_name doesn't work for categories, need to search
            categories = self.cluster.get_by_type('Category')
            for category in categories:
                if hasattr(category, 'name') and category.name == name:
                    return category
            return None
        except Exception as e:
            self.module.fail_json(msg=f"Failed to query category '{name}': {str(e)}")

    def get_user(self, name):
        """
        Get user by name

        Args:
            name: User name

        Returns:
            User Entity object or None
        """
        if not self.cluster:
            self.connect()

        try:
            # get_by_name doesn't work for users, need to search
            users = self.cluster.get_by_type('User')
            for user in users:
                if hasattr(user, 'name') and user.name == name:
                    return user
            return None
        except Exception as e:
            self.module.fail_json(msg=f"Failed to query user '{name}': {str(e)}")

    def get_group(self, name):
        """
        Get group by name

        Args:
            name: Group name

        Returns:
            Group Entity object or None
        """
        if not self.cluster:
            self.connect()

        try:
            # get_by_name doesn't work for groups, need to search
            groups = self.cluster.get_by_type('Group')
            for group in groups:
                if hasattr(group, 'name') and group.name == name:
                    return group
            return None
        except Exception as e:
            self.module.fail_json(msg=f"Failed to query group '{name}': {str(e)}")

    def commit(self):
        """
        Commit changes to BCM (legacy method for compatibility)

        Note: For entity creation/updates, use commit_entity() instead
        """
        if not self.cluster:
            return False

        try:
            # Commit all pending changes (empty list = commit all)
            result = self.cluster.commit([])
            # Result is a tuple (success_result, failure_result)
            # If both are None, commit succeeded
            return True
        except Exception as e:
            self.module.fail_json(msg=f"Failed to commit changes: {str(e)}")
            return False

    def commit_entity(self, entity, entity_name=None):
        """
        Commit a specific entity using entity.commit()

        Args:
            entity: The entity object to commit
            entity_name: Optional descriptive name for error messages

        Returns:
            True on success, fails module on error
        """
        if not entity:
            self.module.fail_json(msg="No entity provided to commit")

        try:
            # Call commit() on the entity itself
            result = entity.commit()

            # Check if commit was successful
            # result is a CommitResult object with a success attribute
            if hasattr(result, 'success') and not result.success:
                error_name = entity_name if entity_name else "entity"
                error_msg = str(result) if result else "Unknown error"
                self.module.fail_json(msg=f"Failed to commit {error_name}: {error_msg}")

            return True
        except Exception as e:
            error_name = entity_name if entity_name else "entity"
            self.module.fail_json(msg=f"Failed to commit {error_name}: {str(e)}")
            return False

    def device_to_dict(self, device):
        """
        Convert device Entity object to dictionary for Ansible output

        Args:
            device: Device Entity object

        Returns:
            Dictionary representation of device
        """
        # Get IP from first available interface
        ip_address = None
        if hasattr(device, 'interfaces') and device.interfaces:
            for iface in device.interfaces:
                if hasattr(iface, 'ip') and iface.ip and iface.ip != '0.0.0.0':
                    ip_address = iface.ip
                    break

        return {
            'uuid': str(device.uuid) if hasattr(device, 'uuid') else None,
            'hostname': device.hostname if hasattr(device, 'hostname') else None,
            'mac': device.mac if hasattr(device, 'mac') else None,
            'ip': ip_address,
            'type': device.childType if hasattr(device, 'childType') else None,
            'partition': str(device.partition) if hasattr(device, 'partition') else None,
            'rack': device.rack if hasattr(device, 'rack') else None,
            'rack_position': device.rackPosition if hasattr(device, 'rackPosition') else None,
            'notes': device.notes if hasattr(device, 'notes') else None,
        }


def bcm_argument_spec():
    """Return common argument spec for BCM modules"""
    return dict(
        pythoncm_path=dict(
            type='str',
            required=False,
            default='/cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages'
        ),
    )
