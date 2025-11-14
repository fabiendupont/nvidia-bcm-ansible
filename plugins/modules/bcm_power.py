#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) NVIDIA Corporation
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bcm_power
short_description: Manage power state of nodes in NVIDIA Base Command Manager
description:
    - Query and control power state of compute nodes
    - Perform power operations (on, off, reset, status)
    - Supports IPMI, Redfish, and custom power scripts
version_added: "1.1.0"
options:
    name:
        description:
            - Name of the node to manage
        required: true
        type: str
    state:
        description:
            - Desired power state
            - C(on) powers on the node
            - C(off) powers off the node
            - C(reset) performs a hard reset (power cycle)
            - C(status) queries current power state
        choices: [ on, off, reset, status ]
        default: status
        type: str
    pythoncm_path:
        description:
            - Path to pythoncm library
        type: str
        default: /cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages
author:
    - NVIDIA Corporation
notes:
    - Requires BMC/IPMI access configured in BCM
    - Power operations may take several seconds to complete
    - Use with caution - improper power operations can interrupt workloads
'''

EXAMPLES = r'''
- name: Query node power status
  nvidia.bcm.bcm_power:
    name: node001
    state: status
  register: power_status

- name: Display power status
  debug:
    var: power_status

- name: Power on a node
  nvidia.bcm.bcm_power:
    name: node001
    state: on

- name: Power off a node (graceful)
  nvidia.bcm.bcm_power:
    name: node001
    state: off

- name: Hard reset a node
  nvidia.bcm.bcm_power:
    name: node001
    state: reset

- name: Power on multiple nodes
  nvidia.bcm.bcm_power:
    name: "{{ item }}"
    state: on
  loop:
    - node001
    - node002
    - node003
'''

RETURN = r'''
power_state:
    description: Current power state of the node
    returned: always
    type: str
    sample: on
power_status_detail:
    description: Detailed power status information
    returned: when state is status
    type: dict
    sample:
        state: UNKNOWN
        msg: ""
        method: custom
changed:
    description: Whether power state was changed
    returned: always
    type: bool
    sample: true
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.nvidia.bcm.plugins.module_utils.bcm_common import BCMModule, bcm_argument_spec


def get_power_state_string(state_info):
    """Convert power state info to simple string"""
    if isinstance(state_info, dict):
        state_name = state_info.get('name', 'UNKNOWN')
    else:
        state_name = str(state_info)

    # Normalize state names
    state_name = state_name.upper()
    if state_name in ['ON', 'POWERED_ON', 'POWEREDON']:
        return 'on'
    elif state_name in ['OFF', 'POWERED_OFF', 'POWEREDOFF']:
        return 'off'
    else:
        return 'unknown'


def main():
    argument_spec = bcm_argument_spec()
    argument_spec.update(
        name=dict(type='str', required=True),
        state=dict(type='str', default='status', choices=['on', 'off', 'reset', 'status']),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    name = module.params['name']
    desired_state = module.params['state']

    bcm = BCMModule(module)
    bcm.connect()

    device = bcm.get_device(name)
    if not device:
        module.fail_json(msg=f"Node '{name}' not found")

    # Get current power status
    try:
        success, status_list = device.power_status()

        if not success or not status_list:
            module.fail_json(msg=f"Failed to query power status for '{name}'")

        status_info = status_list[0] if status_list else {}
        current_state_info = status_info.get('state', {}) if isinstance(status_info, dict) else {}
        current_state = get_power_state_string(current_state_info)

    except Exception as e:
        module.fail_json(msg=f"Failed to query power status for '{name}': {str(e)}")

    # Status query only
    if desired_state == 'status':
        result = {
            'changed': False,
            'power_state': current_state,
            'power_status_detail': {
                'state': current_state_info.get('name', 'UNKNOWN') if isinstance(current_state_info, dict) else str(current_state_info),
                'msg': status_info.get('msg', '') if isinstance(status_info, dict) else '',
                'method': status_info.get('name', 'unknown') if isinstance(status_info, dict) else 'unknown',
            }
        }
        module.exit_json(**result)

    # Determine if action is needed
    action_needed = True
    if desired_state == 'on' and current_state == 'on':
        action_needed = False
    elif desired_state == 'off' and current_state == 'off':
        action_needed = False

    if not action_needed:
        module.exit_json(
            changed=False,
            power_state=current_state,
            msg=f"Node '{name}' already in desired state '{desired_state}'"
        )

    if module.check_mode:
        module.exit_json(
            changed=True,
            msg=f"Would change power state of '{name}' to '{desired_state}'"
        )

    # Perform power operation
    try:
        if desired_state == 'on':
            success, result_list = device.power_on()
            action = 'powered on'
        elif desired_state == 'off':
            success, result_list = device.power_off()
            action = 'powered off'
        elif desired_state == 'reset':
            success, result_list = device.power_reset()
            action = 'reset'

        if not success:
            module.fail_json(
                msg=f"Power operation failed for '{name}'",
                result=result_list
            )

        module.exit_json(
            changed=True,
            power_state=desired_state if desired_state != 'reset' else current_state,
            msg=f"Node '{name}' {action} successfully"
        )

    except Exception as e:
        module.fail_json(msg=f"Failed to perform power operation on '{name}': {str(e)}")


if __name__ == '__main__':
    main()
