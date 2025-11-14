# Installation Guide

## Prerequisites

- NVIDIA Base Command Manager (BCM) head node
- Python 3.6 or later
- Ansible 2.14 or later
- Access to BCM admin certificates

## Step 1: Install System Dependencies

On Red Hat Enterprise Linux 9:

```bash
# Install Ansible
dnf install -y ansible-core

# Install Python dependencies
dnf install -y python3-lxml python3-passlib python3-tabulate python3-pyOpenSSL

# Install BCM pythoncm package (from BCM repository)
dnf install -y cmdaemon-pythoncm
```

## Step 2: Verify BCM Certificates

The collection uses certificate-based authentication. Verify the admin certificates exist:

```bash
ls -la ~/.cm/admin.pem ~/.cm/admin.key
```

These certificates are typically created automatically when BCM is installed.

## Step 3: Install the Collection

### From Source

```bash
cd /path/to/ansible_collections/nvidia/bcm
ansible-galaxy collection build
ansible-galaxy collection install nvidia-bcm-*.tar.gz
```

### From Galaxy (when published)

```bash
ansible-galaxy collection install nvidia.bcm
```

## Step 4: Test the Installation

### Test the Dynamic Inventory

Create a test inventory file `test_inventory.yml`:

```yaml
plugin: nvidia.bcm.bcm_inventory
host: localhost
pythoncm_path: /cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages
```

List all hosts:

```bash
ansible-inventory -i test_inventory.yml --list
ansible-inventory -i test_inventory.yml --graph
```

Expected output:
```
@all:
  |--@ungrouped:
  |--@type_GenericDevice:
  |  |--node001
  |  |--node002
  |  |--...
  |--@type_HeadNode:
  |  |--bcm-headnode
```

### Test with Ansible Commands

```bash
# List all hosts
ansible -i test_inventory.yml all --list-hosts

# List only compute nodes
ansible -i test_inventory.yml type_GenericDevice --list-hosts

# Ping all nodes (if they're accessible)
ansible -i test_inventory.yml all -m ping
```

## Step 5: Using in Playbooks

Create a playbook `test_playbook.yml`:

```yaml
---
- name: Test BCM Integration
  hosts: all
  gather_facts: false

  tasks:
    - name: Display BCM host information
      debug:
        msg: |
          Hostname: {{ bcm_hostname }}
          Type: {{ bcm_type }}
          MAC: {{ bcm_mac }}
          IP: {{ bcm_ip }}
```

Run it:

```bash
ansible-playbook -i test_inventory.yml test_playbook.yml
```

## Troubleshooting

### Import Error: No module named 'pythoncm'

**Solution**: Ensure pythoncm path is correctly set in your inventory configuration:

```yaml
pythoncm_path: /cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages
```

### Import Error: No module named 'lxml' (or other dependencies)

**Solution**: Install missing Python dependencies:

```bash
dnf install -y python3-lxml python3-passlib python3-tabulate python3-pyOpenSSL
```

### Connection Failed: Certificate errors

**Solution**: Verify admin certificates exist and have correct permissions:

```bash
ls -la ~/.cm/admin.{pem,key}
# Should be owned by your user and have 600 permissions
chmod 600 ~/.cm/admin.pem ~/.cm/admin.key
```

### No devices found

**Solution**: Verify BCM is running and you can connect with cmsh:

```bash
cmsh -c "device; list"
```

## Configuration Options

### Inventory Plugin Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `plugin` | string | required | Must be `nvidia.bcm.bcm_inventory` |
| `host` | string | `localhost` | BCM head node hostname or IP |
| `pythoncm_path` | string | `/cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages` | Path to pythoncm library |
| `strict` | bool | `false` | If true, skip hosts with missing variables |
| `compose` | dict | `{}` | Create computed variables |
| `keyed_groups` | list | `[]` | Create groups based on host variables |

### Advanced Inventory Configuration

```yaml
plugin: nvidia.bcm.bcm_inventory
host: localhost
pythoncm_path: /cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages

# Create custom groups
keyed_groups:
  - key: bcm_type
    prefix: type

# Add computed variables
compose:
  ansible_host: bcm_ip
  fqdn: bcm_hostname + '.cluster.local'
```

## Next Steps

- Read the [DEVELOPMENT.md](docs/DEVELOPMENT.md) guide to create custom modules
- Check the [example playbooks](playbooks/) for usage examples
- Review module documentation: `ansible-doc nvidia.bcm.bcm_node`
