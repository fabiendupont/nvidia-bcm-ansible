#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) NVIDIA Corporation
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bcm_group
short_description: Manage groups in NVIDIA Base Command Manager
description:
    - Query and modify groups in NVIDIA Base Command Manager
    - Manage group properties and membership
    - Note: Group creation is not yet supported - groups must be created via cmsh or BCM GUI
version_added: "1.1.0"
options:
    name:
        description:
            - Name of the group to manage
        required: true
        type: str
    state:
        description:
            - Desired state of the group
            - C(present) ensures the group exists with specified properties
            - C(absent) ensures the group is removed
            - C(query) retrieves information about the group
        choices: [ present, absent, query ]
        default: query
        type: str
    notes:
        description:
            - Notes or description for the group
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
- name: Query group information
  nvidia.bcm.bcm_group:
    name: cmsupport
    state: query
  register: group_info

- name: Display group information
  debug:
    var: group_info.group

- name: Update group notes
  nvidia.bcm.bcm_group:
    name: mygroup
    state: present
    notes: Development team group

- name: Remove a group (use with caution)
  nvidia.bcm.bcm_group:
    name: oldgroup
    state: absent
'''

RETURN = r'''
group:
    description: Group information
    returned: always
    type: dict
    sample:
        name: cmsupport
        uuid: a1b2c3d4-1234-5678-90ab-cdef12345678
        members: []
        notes: Support group
changed:
    description: Whether the group was modified
    returned: always
    type: bool
    sample: true
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.nvidia.bcm.plugins.module_utils.bcm_common import BCMModule, bcm_argument_spec


def group_to_dict(group):
    """Convert group Entity to dictionary"""
    return {
        'uuid': str(group.uuid) if hasattr(group, 'uuid') else None,
        'name': group.name if hasattr(group, 'name') else None,
        'members': group.members if hasattr(group, 'members') else [],
        'notes': group.notes if hasattr(group, 'notes') else None,
    }


def main():
    argument_spec = bcm_argument_spec()
    argument_spec.update(
        name=dict(type='str', required=True),
        state=dict(type='str', default='query', choices=['present', 'absent', 'query']),
        notes=dict(type='str', required=False),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    name = module.params['name']
    state = module.params['state']

    bcm = BCMModule(module)
    bcm.connect()

    group = bcm.get_group(name)

    # Query state
    if state == 'query':
        if not group:
            module.fail_json(msg=f"Group '{name}' not found")

        module.exit_json(
            changed=False,
            group=group_to_dict(group)
        )

    # Absent state
    elif state == 'absent':
        if not group:
            module.exit_json(changed=False, msg=f"Group '{name}' does not exist")

        if module.check_mode:
            module.exit_json(changed=True, msg=f"Would remove group '{name}'")

        try:
            # remove() handles deletion immediately, no commit needed
            group.remove()
            module.exit_json(
                changed=True,
                msg=f"Group '{name}' removed successfully"
            )
        except Exception as e:
            module.fail_json(msg=f"Failed to remove group '{name}': {str(e)}")

    # Present state
    elif state == 'present':
        if not group:
            module.fail_json(
                msg=f"Group '{name}' does not exist. Group creation not yet supported. "
                    f"Please create the group via cmsh or BCM GUI first."
            )

        # Check what needs to be updated
        updates = {}

        if module.params.get('notes'):
            current_notes = group.notes if hasattr(group, 'notes') else None
            if current_notes != module.params['notes']:
                updates['notes'] = module.params['notes']

        if not updates:
            module.exit_json(
                changed=False,
                group=group_to_dict(group),
                msg=f"Group '{name}' already in desired state"
            )

        if module.check_mode:
            module.exit_json(
                changed=True,
                msg=f"Would update group '{name}' with: {updates}"
            )

        # Apply updates
        try:
            for key, value in updates.items():
                setattr(group, key, value)

            bcm.commit_entity(group, f"group '{name}'")

            module.exit_json(
                changed=True,
                group=group_to_dict(group),
                msg=f"Group '{name}' updated successfully",
                updates=updates
            )
        except Exception as e:
            module.fail_json(msg=f"Failed to update group '{name}': {str(e)}")


if __name__ == '__main__':
    main()
