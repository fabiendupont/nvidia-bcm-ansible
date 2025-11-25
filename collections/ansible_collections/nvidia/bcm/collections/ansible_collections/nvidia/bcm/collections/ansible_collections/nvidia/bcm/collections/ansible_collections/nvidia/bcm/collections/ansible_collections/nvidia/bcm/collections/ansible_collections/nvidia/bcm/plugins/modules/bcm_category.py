#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) NVIDIA Corporation
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bcm_category
short_description: Manage node categories in NVIDIA Base Command Manager
description:
    - Query and modify node categories in NVIDIA Base Command Manager
    - Categories are used to organize nodes and assign configurations
    - Nodes in a category inherit settings like software images, networks, and mount points
version_added: "1.0.0"
options:
    name:
        description:
            - Name of the category to manage
        required: true
        type: str
    state:
        description:
            - Desired state of the category
            - C(present) ensures the category exists with specified properties
            - C(absent) ensures the category is removed
            - C(query) retrieves information about the category
        choices: [ present, absent, query ]
        default: present
        type: str
    notes:
        description:
            - Notes or description for the category
        type: str
    softwareimage:
        description:
            - Name of the software image to use for this category
        type: str
    bootloader:
        description:
            - Bootloader type (e.g., 'syslinux')
        type: str
    bootloaderprotocol:
        description:
            - Bootloader protocol (e.g., 'http')
        type: str
    kernelparameters:
        description:
            - Kernel parameters for booting nodes in this category
        type: str
    kerneloutputconsole:
        description:
            - Console device for kernel output (e.g., 'ttyS0,115200')
        type: str
    installmode:
        description:
            - Installation mode for nodes
        type: str
        choices: ['AUTO', 'FULL', 'MAIN', 'NOSYNC', 'SKIP']
    newnodeinstallmode:
        description:
            - Installation mode for new nodes
        type: str
        choices: ['AUTO', 'FULL', 'MAIN', 'NOSYNC']
    pythoncm_path:
        description:
            - Path to pythoncm library
        type: str
        default: /cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages
author:
    - NVIDIA Corporation
'''

EXAMPLES = r'''
- name: Query category information
  nvidia.bcm.bcm_category:
    name: default
    state: query
  register: category_info

- name: Display category information
  debug:
    var: category_info.category

- name: Create a new GPU category
  nvidia.bcm.bcm_category:
    name: gpu_compute
    state: present
    notes: "GPU compute nodes with CUDA support"

- name: Update category notes
  nvidia.bcm.bcm_category:
    name: gpu_compute
    state: present
    notes: "Updated description for GPU nodes"

- name: Remove a category (use with caution)
  nvidia.bcm.bcm_category:
    name: old-category
    state: absent
'''

RETURN = r'''
category:
    description: Information about the category
    returned: when state=query or state=present
    type: dict
    sample:
        uuid: "d05e44cd-eb62-4c3c-a1f0-bca9913c743d"
        name: default
        notes: ""
        roles: []
        software_image: "f4632f43-b445-4bee-bf3b-177ec7243ce4"
        management_network: "c48ff6fe-ee03-43ec-9dd5-9b5554a5d5f7"
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


def category_to_dict(category):
    """Convert category Entity to dict for Ansible output"""
    # Get software image UUID if present
    software_image = None
    if hasattr(category, 'softwareImageProxy') and category.softwareImageProxy:
        if isinstance(category.softwareImageProxy, dict):
            software_image = str(category.softwareImageProxy.get('parentSoftwareImage'))
        elif hasattr(category.softwareImageProxy, 'parentSoftwareImage'):
            software_image = str(category.softwareImageProxy.parentSoftwareImage)

    return {
        'uuid': str(category.uuid) if hasattr(category, 'uuid') else None,
        'name': category.name if hasattr(category, 'name') else None,
        'notes': category.notes if hasattr(category, 'notes') else None,
        'roles': category.roles if hasattr(category, 'roles') else [],
        'software_image': software_image,
        'management_network': str(category.managementNetwork) if hasattr(category, 'managementNetwork') else None,
    }


def main():
    # Define module arguments
    argument_spec = bcm_argument_spec()
    argument_spec.update(
        name=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent', 'query']),
        notes=dict(type='str'),
        softwareimage=dict(type='str'),
        bootloader=dict(type='str'),
        bootloaderprotocol=dict(type='str'),
        kernelparameters=dict(type='str'),
        kerneloutputconsole=dict(type='str'),
        installmode=dict(type='str', choices=['AUTO', 'FULL', 'MAIN', 'NOSYNC', 'SKIP']),
        newnodeinstallmode=dict(type='str', choices=['AUTO', 'FULL', 'MAIN', 'NOSYNC']),
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

    # Get existing category
    category = bcm.get_category(name)

    # Handle query state
    if state == 'query':
        if category:
            result['category'] = category_to_dict(category)
            result['msg'] = f"Category '{name}' found"
        else:
            result['msg'] = f"Category '{name}' not found"
            result['category'] = None
        module.exit_json(**result)

    # Handle absent state
    elif state == 'absent':
        if category:
            # Check if this is the default category
            if name == 'default':
                module.fail_json(msg="Cannot remove the 'default' category")

            if not module.check_mode:
                try:
                    # remove() handles deletion immediately, no commit needed
                    category.remove()
                except Exception as e:
                    module.fail_json(msg=f"Failed to remove category '{name}': {str(e)}")
            result['changed'] = True
            result['msg'] = f"Category '{name}' removed"
        else:
            result['msg'] = f"Category '{name}' already absent"
        module.exit_json(**result)

    # Handle present state
    elif state == 'present':
        changes_needed = False

        if not category:
            # CREATE NEW CATEGORY
            # Import the Category entity class
            try:
                from pythoncm.entity.category import Category
            except ImportError:
                module.fail_json(msg="Failed to import Category entity class")

            if module.check_mode:
                module.exit_json(changed=True, msg=f"Would create category '{name}'")

            try:
                # Create new category entity
                category = Category()
                category.name = name

                # Set optional notes
                if module.params.get('notes'):
                    category.notes = module.params['notes']

                # Set boot parameters if provided
                if module.params.get('bootloader'):
                    category.bootloader = module.params['bootloader']
                if module.params.get('bootloaderprotocol'):
                    category.bootloaderProtocol = module.params['bootloaderprotocol']
                if module.params.get('kernelparameters'):
                    category.kernelParameters = module.params['kernelparameters']
                if module.params.get('kerneloutputconsole'):
                    category.kernelOutputConsole = module.params['kerneloutputconsole']
                if module.params.get('installmode'):
                    category.installMode = module.params['installmode']
                if module.params.get('newnodeinstallmode'):
                    category.newNodeInstallMode = module.params['newnodeinstallmode']

                # Configure the auto-created softwareImageProxy
                # Categories must have a parent software image configured
                try:
                    from pythoncm.entity.softwareimage import SoftwareImage

                    # If a software image name is provided, use it; otherwise use default-image
                    image_name = module.params.get('softwareimage', 'default-image')
                    software_image = bcm.cluster.get_by_name(image_name, 'SoftwareImage')
                    if not software_image:
                        module.fail_json(msg=f"Cannot find software image '{image_name}' required for category creation")

                    # Set the proxy's parent image and revision
                    category.softwareImageProxy.parentSoftwareImage = software_image
                    category.softwareImageProxy.revisionID = -1  # NO_REVISION constant
                except Exception as e:
                    module.fail_json(msg=f"Failed to configure software image for category: {str(e)}")

                # Add to cluster
                bcm.cluster.add(category)

                # Commit the entity
                bcm.commit_entity(category, f"category '{name}'")

                module.exit_json(
                    changed=True,
                    category=category_to_dict(category),
                    msg=f"Category '{name}' created successfully"
                )
            except Exception as e:
                module.fail_json(msg=f"Failed to create category '{name}': {str(e)}")

        else:
            # Category exists, check if updates are needed
            updates = {}

            # Check notes
            if module.params.get('notes') is not None:
                current_notes = category.notes if hasattr(category, 'notes') else ''
                if current_notes != module.params['notes']:
                    updates['notes'] = module.params['notes']
                    changes_needed = True

            # Check boot parameters
            param_mapping = {
                'bootloader': 'bootloader',
                'bootloaderprotocol': 'bootloaderProtocol',
                'kernelparameters': 'kernelParameters',
                'kerneloutputconsole': 'kernelOutputConsole',
                'installmode': 'installMode',
                'newnodeinstallmode': 'newNodeInstallMode',
            }

            for param_name, attr_name in param_mapping.items():
                if module.params.get(param_name) is not None:
                    current_value = getattr(category, attr_name, '') if hasattr(category, attr_name) else ''
                    if current_value != module.params[param_name]:
                        updates[attr_name] = module.params[param_name]
                        changes_needed = True

            # Check software image
            if module.params.get('softwareimage') is not None:
                try:
                    from pythoncm.entity.softwareimage import SoftwareImage
                    desired_image = bcm.cluster.get_by_name(module.params['softwareimage'], 'SoftwareImage')
                    if not desired_image:
                        module.fail_json(msg=f"Cannot find software image '{module.params['softwareimage']}'")

                    current_image_uuid = None
                    if hasattr(category, 'softwareImageProxy') and category.softwareImageProxy:
                        if hasattr(category.softwareImageProxy, 'parentSoftwareImage'):
                            current_image = category.softwareImageProxy.parentSoftwareImage
                            if hasattr(current_image, 'uuid'):
                                current_image_uuid = str(current_image.uuid)

                    if str(desired_image.uuid) != current_image_uuid:
                        updates['softwareImageProxy'] = desired_image
                        changes_needed = True
                except Exception as e:
                    module.fail_json(msg=f"Failed to check software image: {str(e)}")

            if changes_needed:
                if not module.check_mode:
                    try:
                        for key, value in updates.items():
                            if key == 'softwareImageProxy':
                                # Special handling for software image
                                category.softwareImageProxy.parentSoftwareImage = value
                                category.softwareImageProxy.revisionID = -1
                            else:
                                setattr(category, key, value)

                        # Commit the entity
                        bcm.commit_entity(category, f"category '{name}'")

                        # Refresh category object
                        category = bcm.get_category(name)

                    except Exception as e:
                        module.fail_json(msg=f"Failed to update category '{name}': {str(e)}")

                result['changed'] = True
                result['msg'] = f"Category '{name}' updated with: {', '.join(updates.keys())}"
            else:
                result['msg'] = f"Category '{name}' already configured"

        # Add category info to result
        if category:
            result['category'] = category_to_dict(category)

        module.exit_json(**result)


if __name__ == '__main__':
    main()
