#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) NVIDIA Corporation
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bcm_software_image
short_description: Manage software images in NVIDIA Base Command Manager
description:
    - Query and modify software images in NVIDIA Base Command Manager
    - Software images are OS images used for node provisioning
    - Images contain the operating system, kernel, and modules for cluster nodes
version_added: "1.0.0"
options:
    name:
        description:
            - Name of the software image to manage
        required: true
        type: str
    state:
        description:
            - Desired state of the software image
            - C(present) ensures the image exists with specified properties
            - C(absent) ensures the image is removed
            - C(query) retrieves information about the image
        choices: [ present, absent, query ]
        default: present
        type: str
    kernel_parameters:
        description:
            - Additional kernel boot parameters
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
- name: Query software image information
  nvidia.bcm.bcm_software_image:
    name: default-image
    state: query
  register: image_info

- name: Display image information
  debug:
    var: image_info.image

- name: Update kernel parameters
  nvidia.bcm.bcm_software_image:
    name: default-image
    state: present
    kernel_parameters: "rd.driver.blacklist=nouveau quiet"

- name: Remove a software image (use with caution)
  nvidia.bcm.bcm_software_image:
    name: old-image
    state: absent
'''

RETURN = r'''
image:
    description: Information about the software image
    returned: when state=query or state=present
    type: dict
    sample:
        uuid: "f4632f43-b445-4bee-bf3b-177ec7243ce4"
        name: "default-image"
        path: "/cm/images/default-image"
        kernel_version: "5.14.0-503.14.1.el9_5.x86_64"
        kernel_parameters: "rd.driver.blacklist=nouveau"
        kernel_output_console: "tty0"
        creation_time: 1761904370
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


def software_image_to_dict(image):
    """Convert software image Entity to dict for Ansible output"""
    return {
        'uuid': str(image.uuid) if hasattr(image, 'uuid') else None,
        'name': image.name if hasattr(image, 'name') else None,
        'path': image.path if hasattr(image, 'path') else None,
        'kernel_version': image.kernelVersion if hasattr(image, 'kernelVersion') else None,
        'kernel_parameters': image.kernelParameters if hasattr(image, 'kernelParameters') else None,
        'kernel_output_console': image.kernelOutputConsole if hasattr(image, 'kernelOutputConsole') else None,
        'creation_time': image.creationTime if hasattr(image, 'creationTime') else None,
    }


def get_software_image(bcm, name):
    """Get software image by name"""
    try:
        # get_by_name doesn't work for software images, need to search
        images = bcm.cluster.get_by_type('SoftwareImage')
        for image in images:
            if hasattr(image, 'name') and image.name == name:
                return image
        return None
    except Exception as e:
        bcm.module.fail_json(msg=f"Failed to query software image '{name}': {str(e)}")


def main():
    # Define module arguments
    argument_spec = bcm_argument_spec()
    argument_spec.update(
        name=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent', 'query']),
        kernel_parameters=dict(type='str'),
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

    # Get existing software image
    image = get_software_image(bcm, name)

    # Handle query state
    if state == 'query':
        if image:
            result['image'] = software_image_to_dict(image)
            result['msg'] = f"Software image '{name}' found"
        else:
            result['msg'] = f"Software image '{name}' not found"
            result['image'] = None
        module.exit_json(**result)

    # Handle absent state
    elif state == 'absent':
        if image:
            # Check if this is the default image
            if name == 'default-image':
                module.fail_json(msg="Cannot remove the 'default-image'")

            # Check if any categories are using this image
            try:
                categories = bcm.cluster.get_by_type('Category')
                using_categories = []
                for cat in categories:
                    if hasattr(cat, 'softwareImageProxy') and cat.softwareImageProxy:
                        if isinstance(cat.softwareImageProxy, dict):
                            img_uuid = cat.softwareImageProxy.get('parentSoftwareImage')
                        elif hasattr(cat.softwareImageProxy, 'parentSoftwareImage'):
                            img_uuid = cat.softwareImageProxy.parentSoftwareImage
                        else:
                            continue

                        if str(img_uuid) == str(image.uuid):
                            using_categories.append(cat.name)

                if using_categories:
                    module.fail_json(
                        msg=f"Cannot remove software image '{name}' - it is used by categories: {', '.join(using_categories)}"
                    )
            except Exception as e:
                module.fail_json(msg=f"Failed to check image usage: {str(e)}")

            if not module.check_mode:
                try:
                    # remove() handles deletion immediately, no commit needed
                    image.remove()
                except Exception as e:
                    module.fail_json(msg=f"Failed to remove software image '{name}': {str(e)}")
            result['changed'] = True
            result['msg'] = f"Software image '{name}' removed"
        else:
            result['msg'] = f"Software image '{name}' already absent"
        module.exit_json(**result)

    # Handle present state
    elif state == 'present':
        changes_needed = False

        if not image:
            # Image creation is not yet supported
            module.fail_json(
                msg=f"Software image '{name}' does not exist. "
                    "Image creation via Ansible is not yet supported. "
                    "Please create images using cmsh or the BCM GUI first, "
                    "then use this module to query or modify them."
            )
        else:
            # Image exists, check if updates are needed
            updates = {}

            # Check kernel parameters
            if module.params.get('kernel_parameters') is not None:
                current_params = image.kernelParameters if hasattr(image, 'kernelParameters') else ''
                if current_params != module.params['kernel_parameters']:
                    updates['kernelParameters'] = module.params['kernel_parameters']
                    changes_needed = True

            if changes_needed:
                if not module.check_mode:
                    try:
                        for key, value in updates.items():
                            setattr(image, key, value)
                        bcm.commit_entity(image, f"software image '{name}'")

                        # Refresh image object
                        image = get_software_image(bcm, name)

                    except Exception as e:
                        module.fail_json(msg=f"Failed to update software image '{name}': {str(e)}")

                result['changed'] = True
                result['msg'] = f"Software image '{name}' updated with: {', '.join(updates.keys())}"
            else:
                result['msg'] = f"Software image '{name}' already configured"

        # Add image info to result
        if image:
            result['image'] = software_image_to_dict(image)

        module.exit_json(**result)


if __name__ == '__main__':
    main()
