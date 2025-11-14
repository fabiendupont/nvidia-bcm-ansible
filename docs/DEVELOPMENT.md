# Development Guide

This guide provides information for developers who want to contribute to or extend the NVIDIA BCM Ansible collection.

## Prerequisites

- NVIDIA Base Command Manager installed and configured
- Python 3.6+
- Ansible 2.9+
- `cmdaemon-pythoncm` package installed
- Development tools: `ansible-test`, `ansible-lint`

## Development Setup

### 1. Clone and Setup

```bash
cd /root/bcm
cd ansible_collections/nvidia/bcm
```

### 2. Configure PYTHONPATH

Add pythoncm to your Python path:

```bash
export PYTHONPATH=/cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages:$PYTHONPATH
```

### 3. Install Development Dependencies

```bash
pip install ansible-test ansible-lint yamllint
```

## Collection Structure

```
ansible_collections/nvidia/bcm/
├── galaxy.yml                 # Collection metadata
├── README.md                  # User documentation
├── plugins/
│   ├── inventory/
│   │   └── bcm_inventory.py  # Dynamic inventory plugin
│   ├── modules/
│   │   └── bcm_node.py       # Node management module
│   └── module_utils/
│       └── bcm_common.py     # Shared utilities
├── playbooks/
│   ├── example_inventory.yml # Example inventory config
│   └── example_playbook.yml  # Example playbook
└── docs/
    └── DEVELOPMENT.md        # This file
```

## Creating New Modules

### Module Template

All BCM modules should follow this pattern:

1. **Import BCMModule base class**
```python
from ansible_collections.nvidia.bcm.plugins.module_utils.bcm_common import (
    BCMModule,
    bcm_argument_spec
)
```

2. **Define module arguments**
```python
argument_spec = bcm_argument_spec()
argument_spec.update(
    # Add your module-specific arguments here
)
```

3. **Use BCMModule helper methods**
- `bcm.connect()` - Connect to cluster
- `bcm.get_device(name)` - Get device by name
- `bcm.get_all_devices(filters)` - Get all devices
- `bcm.commit()` - Commit changes
- `bcm.device_to_dict(device)` - Convert device to dict

### Example: Creating a bcm_category Module

```python
#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.nvidia.bcm.plugins.module_utils.bcm_common import (
    BCMModule,
    bcm_argument_spec
)

def main():
    argument_spec = bcm_argument_spec()
    argument_spec.update(
        name=dict(type='str', required=True),
        state=dict(type='str', default='present', choices=['present', 'absent']),
    )

    module = AnsibleModule(argument_spec=argument_spec)
    bcm = BCMModule(module)
    bcm.connect()

    # Your module logic here

    module.exit_json(changed=False)

if __name__ == '__main__':
    main()
```

## Working with pythoncm

### Common pythoncm Operations

```python
# Get all devices
devices = cluster.get_by_type('Device')

# Create a device
device = cluster.create('Device', 'node001')
device.set('hostname', 'node001.cluster.local')
device.set('ip', '10.0.1.1')

# Modify a device
device = cluster.get('Device', 'node001')
device.set('category', 'compute')

# Remove a device
cluster.remove('Device', 'node001')

# Commit changes
result = cluster.commit()

# Get categories
categories = cluster.get_by_type('Category')

# Get software images
images = cluster.get_by_type('SoftwareImage')
```

### Error Handling

Always wrap pythoncm calls in try/except:

```python
try:
    device = cluster.get('Device', name)
except Exception as e:
    module.fail_json(msg=f"Failed to get device: {str(e)}")
```

## Testing

### Manual Testing

Test your module manually:

```bash
ansible localhost -m nvidia.bcm.bcm_node -a "name=test001 state=query"
```

### Integration Testing

Create test playbooks in `tests/integration/`:

```yaml
- name: Test bcm_node module
  hosts: localhost
  tasks:
    - name: Create test node
      nvidia.bcm.bcm_node:
        name: test_node
        state: present
      register: result

    - name: Verify node was created
      assert:
        that:
          - result.changed
          - result.node.name == 'test_node'
```

### Sanity Testing

Run sanity tests:

```bash
ansible-test sanity --docker default
```

## Building the Collection

### Build the tarball

```bash
ansible-galaxy collection build
```

This creates: `nvidia-bcm-1.0.0.tar.gz`

### Install locally

```bash
ansible-galaxy collection install nvidia-bcm-1.0.0.tar.gz
```

## Contributing

### Module Ideas

Future modules to implement:

- `bcm_category` - Manage categories
- `bcm_software_image` - Manage software images
- `bcm_overlay` - Manage configuration overlays
- `bcm_network` - Manage network configurations
- `bcm_job` - Submit and manage cluster jobs
- `bcm_user` - Manage cluster users
- `bcm_role` - Manage node roles

### Inventory Plugin Enhancements

- Add caching support
- Support for multiple clusters
- Filtering options
- Custom grouping strategies

## Documentation

### Module Documentation

All modules must include:

- `DOCUMENTATION` - Module description and parameters
- `EXAMPLES` - Usage examples
- `RETURN` - Return value documentation

### ansible-doc

Test documentation rendering:

```bash
ansible-doc nvidia.bcm.bcm_node
ansible-doc -t inventory nvidia.bcm.bcm_inventory
```

## Debugging

### Enable Ansible Debug Mode

```bash
ANSIBLE_DEBUG=1 ansible-playbook playbook.yml
```

### Python Debugging

Add to your module:

```python
import pdb; pdb.set_trace()
```

### Check pythoncm Connection

```python
export PYTHONPATH=/cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages
python3 -c "from pythoncm.cluster import Cluster; c = Cluster(); print('Connected')"
```

## Resources

- [Ansible Module Development](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html)
- [Ansible Collection Structure](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections_structure.html)
- [NVIDIA Base Command Manager Documentation](https://docs.nvidia.com/base-command-manager/)
- pythoncm API: See `/cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages/pythoncm/`
