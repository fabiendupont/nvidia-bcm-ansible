#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) NVIDIA Corporation
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bcm_network
short_description: Manage networks in NVIDIA Base Command Manager
description:
    - Query and modify networks in NVIDIA Base Command Manager
    - Networks define IP ranges and settings for cluster communication
    - Common network types include internal, external, and global networks
version_added: "1.0.0"
options:
    name:
        description:
            - Name of the network to manage
        required: true
        type: str
    state:
        description:
            - Desired state of the network
            - C(present) ensures the network exists with specified properties
            - C(absent) ensures the network is removed
            - C(query) retrieves information about the network
        choices: [ present, absent, query ]
        default: present
        type: str
    mtu:
        description:
            - Maximum Transmission Unit for the network
        type: int
    domain_name:
        description:
            - Domain name for the network
        type: str
    pythoncm_path:
        description:
            - Path to pythoncm library
        type: str
        default: /cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages
author:
    - NVIDIA Corporation
'''

EXAMPLES = r'''
- name: Query network information
  nvidia.bcm.bcm_network:
    name: internalnet
    state: query
  register: network_info

- name: Display network information
  debug:
    var: network_info.network

- name: Create a new network
  nvidia.bcm.bcm_network:
    name: storage-network
    state: present
    mtu: 9000
    domain_name: storage.local

- name: Update network MTU
  nvidia.bcm.bcm_network:
    name: internalnet
    state: present
    mtu: 9000

- name: Update domain name
  nvidia.bcm.bcm_network:
    name: internalnet
    state: present
    domain_name: cluster.local

- name: Remove a network (use with caution)
  nvidia.bcm.bcm_network:
    name: old-network
    state: absent
'''

RETURN = r'''
network:
    description: Information about the network
    returned: when state=query or state=present
    type: dict
    sample:
        uuid: "bdd9c6c5-4277-4e45-ac79-32a9292f6de1"
        name: "internalnet"
        type: "INTERNAL"
        mtu: 1500
        domain_name: "cm.cluster"
        gateway: "192.168.122.1"
changed:
    description: Whether any changes were made
    returned: always
    type: bool
msg:
    description: Human-readable message about the action taken
    returned: always
    type: str
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.nvidia.bcm.plugins.module_utils.bcm_common import (
    BCMModule,
    bcm_argument_spec
)


def network_to_dict(network):
    """Convert network Entity to dict for Ansible output"""
    net_dict = network.to_dict()

    return {
        'uuid': str(network.uuid) if hasattr(network, 'uuid') else None,
        'name': network.name if hasattr(network, 'name') else None,
        'type': str(network.type) if hasattr(network, 'type') else None,
        'mtu': network.mtu if hasattr(network, 'mtu') else None,
        'domain_name': network.domainName if hasattr(network, 'domainName') else None,
        'gateway': net_dict.get('gateway') if net_dict.get('gateway') != '0.0.0.0' else None,
        'network': net_dict.get('network') if net_dict.get('network') != '0.0.0.0' else None,
        'netmask': net_dict.get('netmask') if net_dict.get('netmask') != '0.0.0.0' else None,
        'vlan_id': net_dict.get('vlanid') if net_dict.get('vlanid') else None,
    }


def get_network(bcm, name):
    """Get network by name"""
    try:
        # get_by_name doesn't work reliably for networks, need to search
        networks = bcm.cluster.get_by_type('Network')
        for network in networks:
            if hasattr(network, 'name') and network.name == name:
                return network
        return None
    except Exception as e:
        bcm.module.fail_json(msg=f"Failed to query network '{name}': {str(e)}")


def main():
    # Define module arguments
    argument_spec = bcm_argument_spec()
    argument_spec.update(
        name=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent', 'query']),
        mtu=dict(type='int'),
        domain_name=dict(type='str'),
    )

    # Create module
    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    # Initialize BCM connection
    bcm = BCMModule(module)
    bcm.connect()

    # Get parameters
    name = module.params['name']
    state = module.params['state']

    # Initialize result
    result = {
        'changed': False,
        'msg': ''
    }

    # Get existing network
    network = get_network(bcm, name)

    # Handle query state
    if state == 'query':
        if network:
            result['network'] = network_to_dict(network)
            result['msg'] = f"Network '{name}' found"
        else:
            result['msg'] = f"Network '{name}' not found"
            result['network'] = None
        module.exit_json(**result)

    # Handle absent state
    elif state == 'absent':
        if network:
            # Check if this is a system network
            if name in ['globalnet', 'internalnet', 'externalnet']:
                module.fail_json(msg=f"Cannot remove system network '{name}'")

            # Check if any devices are using this network
            try:
                devices = bcm.cluster.get_by_type('Device')
                using_devices = []
                for dev in devices:
                    if hasattr(dev, 'interfaces') and dev.interfaces:
                        for iface in dev.interfaces:
                            if hasattr(iface, 'network') and str(iface.network) == str(network.uuid):
                                using_devices.append(dev.hostname if hasattr(dev, 'hostname') else str(dev.uuid))
                                break

                if using_devices:
                    module.fail_json(
                        msg=f"Cannot remove network '{name}' - it is used by devices: {', '.join(using_devices[:5])}"
                    )
            except Exception as e:
                module.fail_json(msg=f"Failed to check network usage: {str(e)}")

            if not module.check_mode:
                try:
                    # remove() handles deletion immediately, no commit needed
                    network.remove()
                except Exception as e:
                    module.fail_json(msg=f"Failed to remove network '{name}': {str(e)}")
            result['changed'] = True
            result['msg'] = f"Network '{name}' removed"
        else:
            result['msg'] = f"Network '{name}' already absent"
        module.exit_json(**result)

    # Handle present state
    elif state == 'present':
        changes_needed = False

        if not network:
            # CREATE NEW NETWORK
            # Validate required parameters
            if module.params.get('mtu') is None:
                module.fail_json(msg=f"MTU is required when creating a new network")

            # Import the Network entity class
            try:
                from pythoncm.entity.network import Network
            except ImportError:
                module.fail_json(msg="Failed to import Network entity class")

            if module.check_mode:
                module.exit_json(changed=True, msg=f"Would create network '{name}'")

            try:
                # Create new network entity
                network = Network()
                network.name = name
                network.mtu = module.params['mtu']

                # Set optional parameters
                if module.params.get('domain_name'):
                    network.domainName = module.params['domain_name']

                # Add to cluster
                bcm.cluster.add(network)

                # Commit the entity
                bcm.commit_entity(network, f"network '{name}'")

                module.exit_json(
                    changed=True,
                    network=network_to_dict(network),
                    msg=f"Network '{name}' created successfully"
                )
            except Exception as e:
                module.fail_json(msg=f"Failed to create network '{name}': {str(e)}")

        else:
            # Network exists, check if updates are needed
            updates = {}

            # Check MTU
            if module.params.get('mtu') is not None:
                current_mtu = network.mtu if hasattr(network, 'mtu') else None
                if current_mtu != module.params['mtu']:
                    updates['mtu'] = module.params['mtu']
                    changes_needed = True

            # Check domain name
            if module.params.get('domain_name') is not None:
                current_domain = network.domainName if hasattr(network, 'domainName') else None
                if current_domain != module.params['domain_name']:
                    updates['domainName'] = module.params['domain_name']
                    changes_needed = True

            if changes_needed:
                if not module.check_mode:
                    try:
                        for key, value in updates.items():
                            setattr(network, key, value)

                        # Commit the entity
                        bcm.commit_entity(network, f"network '{name}'")

                        # Refresh network object
                        network = get_network(bcm, name)

                    except Exception as e:
                        module.fail_json(msg=f"Failed to update network '{name}': {str(e)}")

                result['changed'] = True
                result['msg'] = f"Network '{name}' updated with: {', '.join(updates.keys())}"
            else:
                result['msg'] = f"Network '{name}' already configured"

        # Add network info to result
        if network:
            result['network'] = network_to_dict(network)

        module.exit_json(**result)


if __name__ == '__main__':
    main()
