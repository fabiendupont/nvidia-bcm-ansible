# NVIDIA Base Command Manager (BCM) Ansible Collection

An Ansible collection for managing NVIDIA Base Command Manager clusters.

## Description

This collection provides modules and plugins to manage NVIDIA Base Command Manager (BCM) infrastructure through Ansible automation. It includes dynamic inventory capabilities and modules for common cluster management tasks.

## Requirements

- Ansible 2.9 or later
- Python 3.6 or later
- Access to an NVIDIA Base Command Manager head node
- `pythoncm` package installed (provided by BCM)

## Installation

### Installing pythoncm

The `pythoncm` package is required and can be installed from the BCM repository:

```bash
dnf install cmdaemon-pythoncm
```

You may need to configure your PYTHONPATH to include the pythoncm library:

```bash
export PYTHONPATH=/cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages:$PYTHONPATH
```

### Installing the Collection

Install directly from Ansible Galaxy:

```bash
ansible-galaxy collection install nvidia.bcm
```

Or install from source:

```bash
cd ansible_collections/nvidia/bcm
ansible-galaxy collection build
ansible-galaxy collection install nvidia-bcm-*.tar.gz
```

## Features

### Dynamic Inventory Plugin

Automatically discover and group nodes from your BCM cluster:

- Automatic node discovery
- Grouping by categories, roles, and custom attributes
- Real-time inventory synchronization with BCM state

### Modules

**Device Management:**
- `bcm_node` - Manage cluster nodes (query, update properties, remove)
- `bcm_category` - Manage node categories
- `bcm_software_image` - Manage software images and kernel parameters

**Network Management:**
- `bcm_network` - Manage cluster networks (MTU, domain names)
- `bcm_overlay` - Query configuration overlays

**User Management:**
- `bcm_user` - Manage BCM users (query, update properties)
- `bcm_group` - Manage BCM groups

**Operations:**
- `bcm_power` - Manage node power states (on, off, reset, status)
- `bcm_info` - Gather cluster facts and information

## Quick Start

### Using the Dynamic Inventory

Create an inventory configuration file `bcm.yml`:

```yaml
plugin: nvidia.bcm.bcm_inventory
host: localhost
```

Use it with ansible commands:

```bash
ansible-inventory -i bcm.yml --list
ansible -i bcm.yml all -m ping
```

### Using Modules in Playbooks

```yaml
---
- name: Manage BCM Cluster
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Get node information
      nvidia.bcm.bcm_node:
        name: node001
        state: query
      register: node_info

    - name: Display node info
      debug:
        var: node_info
```

## Documentation

For detailed documentation on each module and plugin, use:

```bash
ansible-doc nvidia.bcm.bcm_inventory
ansible-doc nvidia.bcm.bcm_node
```

## Support

For issues and feature requests, please visit:
https://github.com/nvidia/ansible-bcm/issues

## License

GPL-3.0-or-later

## Author

NVIDIA Corporation
