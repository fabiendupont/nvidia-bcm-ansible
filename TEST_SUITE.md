# BCM Ansible Collection - Test Suite

## Overview

This document describes the comprehensive test suite for the NVIDIA BCM Ansible Collection.

## Module Coverage

### Core Modules (11 total)

| Module | Status | Test Playbook | Coverage |
|--------|--------|---------------|----------|
| bcm_info | ✅ | test-all-modules.yml | Query cluster info, version |
| bcm_network | ✅ | test-all-modules.yml | Query, create, modify networks |
| bcm_category | ✅ | test-all-modules.yml, test-kickstart.yml | Full CRUD operations |
| bcm_user | ✅ | test-all-modules.yml, user_management_example.yml | Query, create, modify, delete |
| bcm_group | ✅ | test-all-modules.yml, group_management_example.yml | Query, create, modify, delete |
| bcm_node | ✅ | test-all-modules.yml | List, query, modify nodes |
| bcm_certificate | ✅ | test-certificate.yml, test-all-modules.yml | Query, save, revoke, unrevoke, remove |
| bcm_software_image | ✅ | test-all-modules.yml | Query images |
| bcm_overlay | ✅ | - | Configuration overlay management |
| bcm_power | ✅ | power_management_example.yml | Power on/off, status |
| bcm_inventory | ✅ | - | Dynamic inventory plugin |

## Test Playbooks

### Quick Test Suite

Run all quick tests (tags: quick):
```bash
ansible-playbook playbooks/test-all-modules.yml --tags quick
```

### Individual Module Tests

```bash
# Information module
ansible-playbook playbooks/test-all-modules.yml --tags info

# Network module
ansible-playbook playbooks/test-all-modules.yml --tags network

# Category module
ansible-playbook playbooks/test-all-modules.yml --tags category
ansible-playbook playbooks/test-kickstart.yml

# User module
ansible-playbook playbooks/test-all-modules.yml --tags user
ansible-playbook playbooks/user_management_example.yml

# Group module
ansible-playbook playbooks/test-all-modules.yml --tags group
ansible-playbook playbooks/group_management_example.yml

# Node module
ansible-playbook playbooks/test-all-modules.yml --tags node

# Certificate module
ansible-playbook playbooks/test-all-modules.yml --tags certificate
ansible-playbook playbooks/test-certificate.yml

# Software Image module
ansible-playbook playbooks/test-all-modules.yml --tags image

# Power module
ansible-playbook playbooks/power_management_example.yml
```

### Integration Tests

```bash
# Kickstart deployment workflow
ansible-playbook playbooks/test-kickstart.yml

# BCM agent deployment
ansible-playbook playbooks/deploy-bcm-agent.yml

# RHEL node registration
ansible-playbook playbooks/register-bcm-rhel.yml
```

## Testing on New BCM Instance

### Prerequisites

1. BCM head node accessible at specified IP
2. SSH access configured
3. Python 3 installed
4. BCM cmdaemon running

### Setup

1. Update inventory:
```yaml
# inventory-new-bcm.yml
all:
  children:
    bcm_headnodes:
      hosts:
        bcm-new:
          ansible_host: 192.168.122.204
          ansible_user: root
```

2. Install collection:
```bash
ansible-galaxy collection install nvidia-bcm-1.1.0.tar.gz --force
```

3. Run tests:
```bash
# Test connection
ansible -i inventory-new-bcm.yml bcm-new -m ping

# Run quick tests
ansible-playbook -i inventory-new-bcm.yml playbooks/test-all-modules.yml --tags quick

# Run full test suite
ansible-playbook -i inventory-new-bcm.yml playbooks/test-all-modules.yml
```

## Expected Test Results

### test-all-modules.yml

```
PLAY [Test All BCM Ansible Modules] ************

TASK [Get cluster information] *****************
ok: [localhost]

TASK [Display cluster info] ********************
ok: [localhost] => {
    "msg": "BCM Version: 11.0"
}

TASK [Query networks] **************************
ok: [localhost]

TASK [Query default category] ******************
ok: [localhost]

TASK [Query root user] *************************
ok: [localhost]

TASK [Query root group] ************************
ok: [localhost]

TASK [List all devices] ************************
ok: [localhost]

TASK [Query all certificates] ******************
ok: [localhost]

TASK [Summary] *********************************
ok: [localhost] => {
    "msg": "All core modules functional!"
}

PLAY RECAP *************************************
localhost         : ok=15  changed=0
```

### test-certificate.yml

All certificate operations tested:
- ✅ Query all certificates
- ✅ Filter by profile
- ✅ Query by serial/name
- ✅ Save to file
- ✅ Revoke/unrevoke
- ✅ Idempotency
- ✅ Check mode

### test-kickstart.yml

Category-based PXE boot configuration:
- ✅ Create categories
- ✅ Configure PXE boot
- ✅ Assign nodes
- ✅ Cleanup

## Known Limitations

### Certificate Creation
- Certificate creation via pythoncm fails on OpenSSL 3.x (BCM limitation)
- Workaround: Create via cmsh, manage via Ansible

### Software Image Creation
- Images must be cloned from base images
- Cannot create images from scratch via API

## Continuous Integration

### Pre-commit Checks
```bash
# Syntax check
ansible-playbook --syntax-check playbooks/*.yml

# Lint check
ansible-lint playbooks/*.yml
```

### Module Documentation
```bash
# Generate module docs
ansible-doc nvidia.bcm.bcm_info
ansible-doc nvidia.bcm.bcm_certificate
ansible-doc nvidia.bcm.bcm_node
```

## Test Environment

- **BCM Version**: 11.0
- **Python**: 3.9+
- **Ansible**: 2.14+
- **OS**: Rocky Linux 9 / RHEL 9
- **pythoncm**: 3.12

## Reporting Issues

When reporting test failures, include:
1. BCM version
2. Playbook output (use `-vvv` for verbose)
3. Module being tested
4. Expected vs actual behavior

## Contributing Tests

When adding new modules:
1. Add test cases to `test-all-modules.yml`
2. Create dedicated test playbook if complex
3. Update this document
4. Tag tests appropriately (quick, integration, etc.)
