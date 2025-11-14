#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) NVIDIA Corporation
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bcm_info
short_description: Gather facts from NVIDIA Base Command Manager
description:
    - Gather comprehensive facts and information from NVIDIA Base Command Manager
    - Retrieve entity counts, cluster configuration, and overall cluster state
    - Useful for inventory, reporting, and monitoring purposes
version_added: "1.1.0"
options:
    gather_subset:
        description:
            - List of fact subsets to gather
            - C(all) gathers all available facts
            - C(counts) gathers entity counts only
            - C(devices) gathers device summary information
            - C(users) gathers user summary information
            - C(networks) gathers network summary information
        type: list
        elements: str
        default: ['all']
        choices: ['all', 'counts', 'devices', 'users', 'networks']
    pythoncm_path:
        description:
            - Path to pythoncm library
        type: str
        default: /cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages
author:
    - NVIDIA Corporation
'''

EXAMPLES = r'''
- name: Gather all BCM facts
  nvidia.bcm.bcm_info:
  register: bcm_facts

- name: Display BCM facts
  debug:
    var: bcm_facts.bcm

- name: Gather only entity counts
  nvidia.bcm.bcm_info:
    gather_subset:
      - counts
  register: bcm_counts

- name: Display device count
  debug:
    msg: "Total devices: {{ bcm_counts.bcm.counts.devices }}"

- name: Gather device and network information
  nvidia.bcm.bcm_info:
    gather_subset:
      - devices
      - networks
  register: bcm_info
'''

RETURN = r'''
bcm:
    description: BCM cluster facts
    returned: always
    type: dict
    contains:
        counts:
            description: Entity counts
            type: dict
            returned: when counts or all in gather_subset
            sample:
                devices: 6
                users: 1
                groups: 1
                categories: 1
                software_images: 1
                networks: 3
                overlays: 0
                partitions: 1
                racks: 1
        devices:
            description: Device summary information
            type: list
            returned: when devices or all in gather_subset
            sample:
                - name: bcm11-headnode
                  type: HeadNode
                  uuid: abc123...
        users:
            description: User summary information
            type: list
            returned: when users or all in gather_subset
        networks:
            description: Network summary information
            type: list
            returned: when networks or all in gather_subset
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.nvidia.bcm.plugins.module_utils.bcm_common import BCMModule, bcm_argument_spec


def main():
    argument_spec = bcm_argument_spec()
    argument_spec.update(
        gather_subset=dict(
            type='list',
            elements='str',
            default=['all'],
            choices=['all', 'counts', 'devices', 'users', 'networks']
        ),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True,
    )

    gather_subset = module.params['gather_subset']

    # If 'all' is specified, gather everything
    if 'all' in gather_subset:
        gather_subset = ['counts', 'devices', 'users', 'networks']

    bcm = BCMModule(module)
    bcm.connect()

    facts = {}

    # Gather entity counts
    if 'counts' in gather_subset:
        try:
            counts = {}
            entity_types = {
                'Device': 'devices',
                'User': 'users',
                'Group': 'groups',
                'Category': 'categories',
                'SoftwareImage': 'software_images',
                'Network': 'networks',
                'Overlay': 'overlays',
                'Partition': 'partitions',
                'Rack': 'racks',
            }

            for entity_type, key in entity_types.items():
                try:
                    entities = bcm.cluster.get_by_type(entity_type)
                    counts[key] = len(entities)
                except:
                    counts[key] = 0

            facts['counts'] = counts
        except Exception as e:
            module.fail_json(msg=f"Failed to gather counts: {str(e)}")

    # Gather device summary
    if 'devices' in gather_subset:
        try:
            devices = bcm.cluster.get_by_type('Device')
            device_list = []

            for device in devices:
                device_info = {
                    'name': device.hostname if hasattr(device, 'hostname') else None,
                    'uuid': str(device.uuid) if hasattr(device, 'uuid') else None,
                    'type': device.childType if hasattr(device, 'childType') else None,
                    'mac': device.mac if hasattr(device, 'mac') else None,
                }
                device_list.append(device_info)

            facts['devices'] = device_list
        except Exception as e:
            module.fail_json(msg=f"Failed to gather device info: {str(e)}")

    # Gather user summary
    if 'users' in gather_subset:
        try:
            users = bcm.cluster.get_by_type('User')
            user_list = []

            for user in users:
                user_info = {
                    'name': user.name if hasattr(user, 'name') else None,
                    'uuid': str(user.uuid) if hasattr(user, 'uuid') else None,
                    'uid': user.ID if hasattr(user, 'ID') else None,
                    'home': user.homeDirectory if hasattr(user, 'homeDirectory') else None,
                }
                user_list.append(user_info)

            facts['users'] = user_list
        except Exception as e:
            module.fail_json(msg=f"Failed to gather user info: {str(e)}")

    # Gather network summary
    if 'networks' in gather_subset:
        try:
            networks = bcm.cluster.get_by_type('Network')
            network_list = []

            for network in networks:
                network_info = {
                    'name': network.name if hasattr(network, 'name') else None,
                    'uuid': str(network.uuid) if hasattr(network, 'uuid') else None,
                    'mtu': network.mtu if hasattr(network, 'mtu') else None,
                    'domain': network.domainName if hasattr(network, 'domainName') else None,
                }
                network_list.append(network_info)

            facts['networks'] = network_list
        except Exception as e:
            module.fail_json(msg=f"Failed to gather network info: {str(e)}")

    module.exit_json(
        changed=False,
        bcm=facts
    )


if __name__ == '__main__':
    main()
