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
            # Node creation is complex in BCM and typically requires additional setup
            # For now, fail with a helpful message
            module.fail_json(
                msg=f"Node '{name}' does not exist. "
                    "Node creation via Ansible is not yet supported. "
                    "Please create nodes using cmsh or the BCM GUI first, "
                    "then use this module to query or modify them."
            )
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
