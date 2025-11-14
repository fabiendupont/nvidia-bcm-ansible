#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) NVIDIA Corporation
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bcm_user
short_description: Manage users in NVIDIA Base Command Manager
description:
    - Query and modify users in NVIDIA Base Command Manager
    - Manage user properties such as home directory, shell, email, etc.
    - Note: User creation is not yet supported - users must be created via cmsh or BCM GUI
version_added: "1.1.0"
options:
    name:
        description:
            - Name of the user to manage
        required: true
        type: str
    state:
        description:
            - Desired state of the user
            - C(present) ensures the user exists with specified properties
            - C(absent) ensures the user is removed
            - C(query) retrieves information about the user
        choices: [ present, absent, query ]
        default: query
        type: str
    uid:
        description:
            - User ID (UID) for the user
            - Required when creating a new user
        type: str
    gid:
        description:
            - Primary group ID (GID) for the user
            - Defaults to same as UID if not specified during creation
        type: str
    home:
        description:
            - Home directory for the user
            - Defaults to /home/<username> if not specified during creation
        type: str
    shell:
        description:
            - Login shell for the user
            - Defaults to /bin/bash if not specified during creation
        type: str
    email:
        description:
            - Email address for the user
        type: str
    notes:
        description:
            - Notes or description for the user
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
- name: Query user information
  nvidia.bcm.bcm_user:
    name: cmsupport
    state: query
  register: user_info

- name: Display user information
  debug:
    var: user_info.user

- name: Create a new user
  nvidia.bcm.bcm_user:
    name: newuser
    state: present
    uid: "2001"
    gid: "2001"
    home: /home/newuser
    shell: /bin/bash
    email: newuser@example.com

- name: Create a user with minimal parameters (defaults apply)
  nvidia.bcm.bcm_user:
    name: simpleuser
    state: present
    uid: "2002"
    # gid defaults to uid (2002)
    # home defaults to /home/simpleuser
    # shell defaults to /bin/bash

- name: Update user email
  nvidia.bcm.bcm_user:
    name: testuser
    state: present
    email: testuser@example.com

- name: Update user shell and home directory
  nvidia.bcm.bcm_user:
    name: testuser
    state: present
    shell: /bin/zsh
    home: /home/testuser

- name: Remove a user (use with caution)
  nvidia.bcm.bcm_user:
    name: olduser
    state: absent
'''

RETURN = r'''
user:
    description: User information
    returned: always
    type: dict
    sample:
        name: cmsupport
        uuid: c792c8d3-3a5a-5003-bf6e-5bed0e59706f
        home: /home/cmsupport
        shell: /bin/bash
        email: support@example.com
        groups: []
        notes: Support user account
changed:
    description: Whether the user was modified
    returned: always
    type: bool
    sample: true
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.nvidia.bcm.plugins.module_utils.bcm_common import BCMModule, bcm_argument_spec


def user_to_dict(user):
    """Convert user Entity to dictionary"""
    return {
        'uuid': str(user.uuid) if hasattr(user, 'uuid') else None,
        'name': user.name if hasattr(user, 'name') else None,
        'uid': user.ID if hasattr(user, 'ID') else None,
        'gid': user.groupID if hasattr(user, 'groupID') else None,
        'home': user.homeDirectory if hasattr(user, 'homeDirectory') else None,
        'shell': user.loginShell if hasattr(user, 'loginShell') else None,
        'email': user.email if hasattr(user, 'email') else None,
        'groups': user.groups if hasattr(user, 'groups') else [],
        'notes': user.information if hasattr(user, 'information') else None,
    }


def main():
    argument_spec = bcm_argument_spec()
    argument_spec.update(
        name=dict(type='str', required=True),
        state=dict(type='str', default='query', choices=['present', 'absent', 'query']),
        uid=dict(type='str', required=False),
        gid=dict(type='str', required=False),
        home=dict(type='str', required=False),
        shell=dict(type='str', required=False),
        email=dict(type='str', required=False),
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

    user = bcm.get_user(name)

    # Query state
    if state == 'query':
        if not user:
            module.fail_json(msg=f"User '{name}' not found")

        module.exit_json(
            changed=False,
            user=user_to_dict(user)
        )

    # Absent state
    elif state == 'absent':
        if not user:
            module.exit_json(changed=False, msg=f"User '{name}' does not exist")

        if module.check_mode:
            module.exit_json(changed=True, msg=f"Would remove user '{name}'")

        try:
            # remove() handles deletion immediately, no commit needed
            user.remove()

            module.exit_json(
                changed=True,
                msg=f"User '{name}' removed successfully"
            )
        except Exception as e:
            module.fail_json(msg=f"Failed to remove user '{name}': {str(e)}")

    # Present state
    elif state == 'present':
        # CREATE USER if it doesn't exist
        if not user:
            # Validate required parameters for creation
            if not module.params.get('uid'):
                module.fail_json(msg=f"UID is required when creating a new user")

            # Import the User entity class
            try:
                from pythoncm.entity.user import User
            except ImportError:
                module.fail_json(msg="Failed to import User entity class")

            if module.check_mode:
                module.exit_json(changed=True, msg=f"Would create user '{name}'")

            try:
                # Create new user entity
                user = User()
                user.name = name
                user.ID = module.params['uid']
                user.groupID = module.params['gid'] if module.params['gid'] else module.params['uid']  # Default GID = UID
                user.homeDirectory = module.params['home'] if module.params['home'] else f"/home/{name}"
                user.loginShell = module.params['shell'] if module.params['shell'] else '/bin/bash'

                if module.params.get('email'):
                    user.email = module.params['email']
                if module.params.get('notes'):
                    user.information = module.params['notes']

                # Add to cluster
                bcm.cluster.add(user)

                # Commit the entity
                bcm.commit_entity(user, f"user '{name}'")

                module.exit_json(
                    changed=True,
                    user=user_to_dict(user),
                    msg=f"User '{name}' created successfully"
                )
            except Exception as e:
                module.fail_json(msg=f"Failed to create user '{name}': {str(e)}")

        # UPDATE EXISTING USER
        # Check what needs to be updated
        updates = {}

        if module.params.get('home'):
            current_home = user.homeDirectory if hasattr(user, 'homeDirectory') else None
            if current_home != module.params['home']:
                updates['homeDirectory'] = module.params['home']

        if module.params.get('shell'):
            current_shell = user.loginShell if hasattr(user, 'loginShell') else None
            if current_shell != module.params['shell']:
                updates['loginShell'] = module.params['shell']

        if module.params.get('email'):
            current_email = user.email if hasattr(user, 'email') else None
            if current_email != module.params['email']:
                updates['email'] = module.params['email']

        if module.params.get('notes'):
            current_notes = user.information if hasattr(user, 'information') else None
            if current_notes != module.params['notes']:
                updates['information'] = module.params['notes']

        if not updates:
            module.exit_json(
                changed=False,
                user=user_to_dict(user),
                msg=f"User '{name}' already in desired state"
            )

        if module.check_mode:
            module.exit_json(
                changed=True,
                msg=f"Would update user '{name}' with: {updates}"
            )

        # Apply updates
        try:
            for key, value in updates.items():
                setattr(user, key, value)

            # Commit the entity
            bcm.commit_entity(user, f"user '{name}'")

            module.exit_json(
                changed=True,
                user=user_to_dict(user),
                msg=f"User '{name}' updated successfully",
                updates=updates
            )
        except Exception as e:
            module.fail_json(msg=f"Failed to update user '{name}': {str(e)}")


if __name__ == '__main__':
    main()
