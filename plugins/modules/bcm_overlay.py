#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) NVIDIA Corporation
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bcm_overlay
short_description: Manage configuration overlays in NVIDIA Base Command Manager
description:
    - Query configuration overlays in NVIDIA Base Command Manager
    - Configuration overlays customize node configurations with files, scripts, and roles
    - Overlays can be applied to specific categories, nodes, or all head nodes
version_added: "1.0.0"
options:
    name:
        description:
            - Name of the configuration overlay to manage
        required: true
        type: str
    state:
        description:
            - Desired state of the overlay
            - C(query) retrieves information about the overlay
            - C(present) and C(absent) states are not yet implemented
        choices: [ query ]
        default: query
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
- name: Query configuration overlay information
  nvidia.bcm.bcm_overlay:
    name: slurm-submit
    state: query
  register: overlay_info

- name: Display overlay information
  debug:
    var: overlay_info.overlay

- name: List all overlays
  nvidia.bcm.bcm_overlay:
    name: "{{ item }}"
    state: query
  loop:
    - slurm-submit
    - slurm-client
  register: all_overlays
'''

RETURN = r'''
overlay:
    description: Information about the configuration overlay
    returned: when state=query
    type: dict
    sample:
        uuid: "1ef91086-49cc-40e2-90cf-0dceeaa3d918"
        name: "slurm-submit"
        priority: 0
        all_head_nodes: false
        num_categories: 1
        num_roles: 1
        num_files: 0
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


def overlay_to_dict(overlay):
    """Convert overlay Entity to dict for Ansible output"""
    overlay_dict = overlay.to_dict()

    # Count various elements
    num_categories = len(overlay_dict.get('categories', []))
    num_roles = len(overlay_dict.get('roles', []))
    num_files = len(overlay_dict.get('customizationFiles', []))

    return {
        'uuid': str(overlay.uuid) if hasattr(overlay, 'uuid') else None,
        'name': overlay.name if hasattr(overlay, 'name') else None,
        'priority': overlay.priority if hasattr(overlay, 'priority') else None,
        'all_head_nodes': overlay.allHeadNodes if hasattr(overlay, 'allHeadNodes') else False,
        'num_categories': num_categories,
        'num_roles': num_roles,
        'num_files': num_files,
    }


def get_overlay(bcm, name):
    """Get configuration overlay by name"""
    try:
        # get_by_name doesn't work for overlays, need to search
        overlays = bcm.cluster.get_by_type('ConfigurationOverlay')
        for overlay in overlays:
            if hasattr(overlay, 'name') and overlay.name == name:
                return overlay
        return None
    except Exception as e:
        bcm.module.fail_json(msg=f"Failed to query configuration overlay '{name}': {str(e)}")


def main():
    # Define module arguments
    argument_spec = bcm_argument_spec()
    argument_spec.update(
        name=dict(type='str', required=True),
        state=dict(type='str', default='query', choices=['query']),
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

    # Get existing overlay
    overlay = get_overlay(bcm, name)

    # Handle query state
    if state == 'query':
        if overlay:
            result['overlay'] = overlay_to_dict(overlay)
            result['msg'] = f"Configuration overlay '{name}' found"
        else:
            result['msg'] = f"Configuration overlay '{name}' not found"
            result['overlay'] = None
        module.exit_json(**result)

    # Other states not yet implemented
    else:
        module.fail_json(msg=f"State '{state}' is not yet implemented for bcm_overlay module")


if __name__ == '__main__':
    main()
