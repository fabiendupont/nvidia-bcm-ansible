#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) NVIDIA Corporation
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bcm_node
short_description: Manage nodes in NVIDIA Base Command Manager
description:
    - Query and modify nodes in NVIDIA Base Command Manager
    - Manage node properties such as hostname, MAC address, rack location, etc.
    - Note: Node creation is not yet supported - nodes must be created via cmsh or BCM GUI
version_added: "1.0.0"
options:
    name:
        description:
            - Name of the node to manage
        required: true
        type: str
    state:
        description:
            - Desired state of the node
            - C(present) ensures the node exists with specified properties
            - C(absent) ensures the node is removed
            - C(query) retrieves information about the node
        choices: [ present, absent, query ]
        default: present
        type: str
    hostname:
        description:
            - Hostname for the node
        type: str
    ip:
        description:
            - IP address for the node
        type: str
    mac:
        description:
            - MAC address for the node
        type: str
    category:
        description:
            - Category to assign to the node
        type: str
    osimage:
        description:
            - OS image to assign to the node
        type: str
    rack:
        description:
            - Rack location for the node
        type: str
    rackposition:
        description:
            - Position in rack for the node
        type: int
    kernelparameters:
        description:
            - Kernel parameters for PXE boot
            - Overrides category-level kernel parameters
            - Used for per-node customization (e.g., Ignition URLs)
        type: str
    node_type:
        description:
            - Type of node to create
            - C(physicalnode) for traditional BCM managed nodes with PXE boot support
            - C(litenode) for Kubernetes/OpenShift nodes managed by BCM Lite Daemon
            - C(genericdevice) for basic devices
        type: str
        choices: [ physicalnode, litenode, genericdevice ]
        default: physicalnode
    pythoncm_path:
        description:
            - Path to pythoncm library
        type: str
        default: /cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages
author:
    - NVIDIA Corporation
'''

EXAMPLES = r'''
- name: Query node information
  nvidia.bcm.bcm_node:
    name: bcm11-headnode
    state: query
  register: node_info

- name: Display node information
  debug:
    var: node_info.node

- name: Update node rack location
  nvidia.bcm.bcm_node:
    name: node001
    state: present
    rack: "A1"
    rackposition: 10

- name: Update node hostname and MAC
  nvidia.bcm.bcm_node:
    name: node001
    state: present
    hostname: node001.cluster.local
    mac: "00:11:22:33:44:55"

- name: Set node-specific kernel parameters (OpenShift Ignition URL)
  nvidia.bcm.bcm_node:
    name: worker-0
    state: present
    category: openshift-416-prod-worker
    kernelparameters: "coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/openshift-4.16/prod/worker/52-54-00-aa-bb-10.ign"

- name: Create a new node
  nvidia.bcm.bcm_node:
    name: compute-10
    state: present
    mac: "52:54:00:12:34:56"
    ip: "10.141.100.10"
    category: slurm-hpc01-compute

- name: Remove a node (use with caution)
  nvidia.bcm.bcm_node:
    name: old-node
    state: absent
'''

RETURN = r'''
node:
    description: Information about the node
    returned: when state=query or state=present
    type: dict
    sample:
        uuid: "c7575ac1-2076-4833-b811-551e4f255381"
        hostname: bcm11-headnode
        mac: "52:54:00:65:74:3F"
        ip: "10.141.255.254"
        type: HeadNode
        partition: "44259690-7f51-4956-a3f5-2d2ef471f627"
        rack: null
        rack_position: 0
        notes: ""
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


def main():
    # Define module arguments
    argument_spec = bcm_argument_spec()
    argument_spec.update(
        name=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent', 'query']),
        hostname=dict(type='str'),
        ip=dict(type='str'),
        mac=dict(type='str'),
        category=dict(type='str'),
        osimage=dict(type='str'),
        rack=dict(type='str'),
        rackposition=dict(type='int'),
        kernelparameters=dict(type='str'),
        node_type=dict(type='str', default='physicalnode', choices=['physicalnode', 'litenode', 'genericdevice']),
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

    # Get existing device
    device = bcm.get_device(name)

    # Handle query state
    if state == 'query':
        if device:
            result['node'] = bcm.device_to_dict(device)
            result['msg'] = f"Node '{name}' found"
        else:
            result['msg'] = f"Node '{name}' not found"
            result['node'] = None
        module.exit_json(**result)

    # Handle absent state
    elif state == 'absent':
        if device:
            if not module.check_mode:
                try:
                    # remove() handles deletion immediately, no commit needed
                    device.remove()
                except Exception as e:
                    module.fail_json(msg=f"Failed to remove node '{name}': {str(e)}")
            result['changed'] = True
            result['msg'] = f"Node '{name}' removed"
        else:
            result['msg'] = f"Node '{name}' already absent"
        module.exit_json(**result)

    # Handle present state
    elif state == 'present':
        changes_needed = False

        if not device:
            # Create new node
            if not module.params.get('mac'):
                module.fail_json(msg=f"MAC address is required to create node '{name}'")

            if not module.check_mode:
                try:
                    # Import the appropriate node class based on node_type
                    node_type = module.params.get('node_type', 'physicalnode')
                    if node_type == 'physicalnode':
                        from pythoncm.entity.computenode import ComputeNode
                        from pythoncm.entity.networkphysicalinterface import NetworkPhysicalInterface

                        device = ComputeNode()
                        device.hostname = name
                        device.mac = module.params['mac']

                        # PhysicalNode requires interface configuration
                        if module.params.get('ip'):
                            # Create a physical interface
                            interface = NetworkPhysicalInterface()
                            interface.name = 'BOOTIF'
                            interface.ip = module.params['ip']

                            # Get default network (internalnet)
                            network = bcm.cluster.get_by_name('internalnet', 'Network')
                            if network:
                                interface.network = network

                            # Add interface to device
                            device.nics.append(interface)

                            # Set provisioning interface
                            device.provisioningInterface = interface

                    elif node_type == 'litenode':
                        from pythoncm.entity.litenode import LiteNode
                        device = LiteNode()
                        device.hostname = name
                        device.mac = module.params['mac']
                    elif node_type == 'genericdevice':
                        from pythoncm.entity.genericdevice import GenericDevice
                        device = GenericDevice()
                        device.hostname = name
                        device.mac = module.params['mac']
                    else:
                        module.fail_json(msg=f"Unsupported node_type: {node_type}")

                    # Set category for all node types
                    if module.params.get('category'):
                        category = bcm.get_category(module.params['category'])
                        if not category:
                            module.fail_json(msg=f"Category '{module.params['category']}' not found")
                        device.category = category

                    # Add to cluster
                    bcm.cluster.add(device)

                    # Commit the new device
                    bcm.commit_entity(device, f"new node '{name}'")

                    # Refresh device object
                    device = bcm.get_device(name)

                except Exception as e:
                    module.fail_json(msg=f"Failed to create node '{name}': {str(e)}")

            changes_needed = True
            result['msg'] = f"Node '{name}' created"
        else:
            # Node exists, check if updates are needed
            updates = {}

            # Check hostname
            if module.params.get('hostname'):
                current_hostname = device.hostname if hasattr(device, 'hostname') else None
                if current_hostname != module.params['hostname']:
                    updates['hostname'] = module.params['hostname']
                    changes_needed = True

            # Check MAC address
            if module.params.get('mac'):
                current_mac = device.mac if hasattr(device, 'mac') else None
                if current_mac != module.params['mac']:
                    updates['mac'] = module.params['mac']
                    changes_needed = True

            # Check rack
            if module.params.get('rack'):
                current_rack = device.rack if hasattr(device, 'rack') else None
                if current_rack != module.params['rack']:
                    updates['rack'] = module.params['rack']
                    changes_needed = True

            # Check rack position
            if module.params.get('rackposition') is not None:
                current_pos = device.rackPosition if hasattr(device, 'rackPosition') else None
                if current_pos != module.params['rackposition']:
                    updates['rackPosition'] = module.params['rackposition']
                    changes_needed = True

            # Check category
            if module.params.get('category'):
                current_category = device.category.name if (hasattr(device, 'category') and device.category) else None
                if current_category != module.params['category']:
                    category = bcm.get_category(module.params['category'])
                    if not category:
                        module.fail_json(msg=f"Category '{module.params['category']}' not found")
                    updates['category'] = category
                    changes_needed = True

            # Check kernel parameters
            if module.params.get('kernelparameters') is not None:
                current_params = device.kernelparameters if hasattr(device, 'kernelparameters') else None
                if current_params != module.params['kernelparameters']:
                    updates['kernelparameters'] = module.params['kernelparameters']
                    changes_needed = True

            if changes_needed:
                if not module.check_mode:
                    try:
                        for key, value in updates.items():
                            setattr(device, key, value)
                        bcm.commit_entity(device, f"node '{name}'")

                        # Refresh device object
                        device = bcm.get_device(name)

                    except Exception as e:
                        module.fail_json(msg=f"Failed to update node '{name}': {str(e)}")

                result['changed'] = True
                result['msg'] = f"Node '{name}' updated with: {', '.join(updates.keys())}"
            else:
                result['msg'] = f"Node '{name}' already configured"

        # Add node info to result
        if device:
            result['node'] = bcm.device_to_dict(device)

        module.exit_json(**result)


if __name__ == '__main__':
    main()
