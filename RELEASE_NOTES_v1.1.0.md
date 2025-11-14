# NVIDIA BCM Ansible Collection v1.1.0 - Release Notes

**Release Date:** January 16, 2025

## Summary

Version 1.1.0 adds four new medium-priority modules for user management, cluster information gathering, and power management, bringing the total module count to **10 modules**.

---

## New Features

### New Modules (4)

#### 1. **bcm_user** - User Management
Manage BCM users with comprehensive property control:
- **Query Operations**: Retrieve user information (UID, GID, home, shell, email, groups)
- **Update Operations**: Modify user properties (home directory, shell, email, notes)
- **Delete Operations**: Remove users with proper validation
- **Features**: Idempotent, check mode support, Entity API integration

**Example:**
```yaml
- name: Update user email
  nvidia.bcm.bcm_user:
    name: testuser
    state: present
    email: testuser@example.com
```

#### 2. **bcm_group** - Group Management
Manage BCM groups with full integration into the user system:
- **Query Operations**: View group membership and metadata
- **Update Operations**: Modify group properties and notes
- **Delete Operations**: Remove groups with safety checks
- **Features**: Idempotent operations, member tracking

**Example:**
```yaml
- name: Update group notes
  nvidia.bcm.bcm_group:
    name: developers
    state: present
    notes: Development team group
```

#### 3. **bcm_info** - Cluster Facts Gathering
Comprehensive cluster information and inventory reporting:
- **Entity Counts**: Get counts for all BCM object types (devices, users, groups, categories, images, networks, overlays, partitions, racks)
- **Device Summary**: List all devices with type, UUID, and MAC address
- **User Summary**: List all users with UID and home directory
- **Network Summary**: List all networks with MTU and domain configuration
- **Flexible Subsets**: Choose which facts to gather (all, counts, devices, users, networks)

**Example:**
```yaml
- name: Gather cluster facts
  nvidia.bcm.bcm_info:
  register: bcm_facts

- name: Display device count
  debug:
    msg: "Total devices: {{ bcm_facts.bcm.counts.devices }}"
```

#### 4. **bcm_power** - Power Management
Control node power states with IPMI/Redfish integration:
- **Power Status**: Query current power state
- **Power On**: Boot nodes remotely
- **Power Off**: Gracefully shut down nodes
- **Hard Reset**: Power cycle nodes
- **Features**: Conditional operations, batch support, detailed status reporting

**Example:**
```yaml
- name: Power on multiple nodes
  nvidia.bcm.bcm_power:
    name: "{{ item }}"
    state: on
  loop:
    - node001
    - node002
    - node003
```

---

## New Example Playbooks (4)

1. **user_management_example.yml** - User query and update workflows
2. **group_management_example.yml** - Group management workflows
3. **cluster_info_example.yml** - Cluster information gathering and reporting
4. **power_management_example.yml** - Power management operations with safety examples

All example playbooks include:
- Safe defaults (query operations enabled, destructive operations commented out)
- Real-world usage patterns
- Best practices documentation

---

## Updated Components

### bcm_common.py
Added two new helper methods:
- `get_user(name)` - Retrieve user by name (uses manual search pattern)
- `get_group(name)` - Retrieve group by name (uses manual search pattern)

These methods follow the same pattern as `get_category()` since `get_by_name()` doesn't work for these entity types.

### Documentation
- **README.md**: Updated module list with categorization (Device, Network, User, Operations)
- **CHANGELOG.md**: Complete v1.1.0 release notes
- **galaxy.yml**: Version bumped to 1.1.0

---

## Module Summary

The collection now includes **10 modules** across 4 categories:

### Device Management (3 modules)
- `bcm_node` - Node management
- `bcm_category` - Category management
- `bcm_software_image` - Software image management

### Network Management (2 modules)
- `bcm_network` - Network management
- `bcm_overlay` - Configuration overlay queries

### User Management (2 modules)
- `bcm_user` - User management ✨ NEW
- `bcm_group` - Group management ✨ NEW

### Operations (3 modules)
- `bcm_inventory` - Dynamic inventory plugin
- `bcm_power` - Power management ✨ NEW
- `bcm_info` - Cluster facts gathering ✨ NEW

---

## Installation

### From Tarball
```bash
ansible-galaxy collection install nvidia-bcm-1.1.0.tar.gz
```

### Upgrade from v1.0.0
```bash
ansible-galaxy collection install nvidia-bcm-1.1.0.tar.gz --force
```

### Verify Installation
```bash
ansible-galaxy collection list | grep nvidia.bcm
# Should show: nvidia.bcm   1.1.0
```

---

## Testing

All modules have been tested successfully:

```bash
# Test bcm_user
ansible localhost -m nvidia.bcm.bcm_user -a "name=cmsupport state=query" -c local

# Test bcm_group
ansible localhost -m nvidia.bcm.bcm_group -a "name=cmsupport state=query" -c local

# Test bcm_info
ansible localhost -m nvidia.bcm.bcm_info -c local

# Test bcm_power
ansible localhost -m nvidia.bcm.bcm_power -a "name=node001 state=status" -c local
```

Example playbooks tested:
- ✅ cluster_info_example.yml
- ✅ user_management_example.yml
- ✅ group_management_example.yml
- ✅ power_management_example.yml

---

## Known Limitations

Same as v1.0.0:
- Entity creation not supported (must use cmsh/GUI to create users, groups, etc.)
- `bcm_overlay` is query-only
- Power management requires BMC/IPMI access configured in BCM
- Limited to property updates for existing entities

---

## Migration from v1.0.0

No breaking changes. The v1.1.0 release is fully backward compatible with v1.0.0:
- All existing modules work identically
- New modules are additive only
- No configuration changes required

Simply upgrade the collection:
```bash
ansible-galaxy collection install nvidia-bcm-1.1.0.tar.gz --force
```

---

## What's Next?

### Planned for v1.2.0
- Add entity creation support to existing modules
- Implement comprehensive unit tests
- Add integration test suite
- Performance optimizations for large clusters

### Planned for v2.0.0
- Full CRUD support for all modules
- Advanced workflow automation
- Monitoring and health check modules
- Backup and restore capabilities
- Ansible Automation Platform integration

---

## File Locations

**Collection Package:**
- `/root/bcm/ansible_collections/nvidia/bcm/nvidia-bcm-1.1.0.tar.gz`

**Example Playbooks:**
- `/root/bcm/ansible_collections/nvidia/bcm/playbooks/user_management_example.yml`
- `/root/bcm/ansible_collections/nvidia/bcm/playbooks/group_management_example.yml`
- `/root/bcm/ansible_collections/nvidia/bcm/playbooks/cluster_info_example.yml`
- `/root/bcm/ansible_collections/nvidia/bcm/playbooks/power_management_example.yml`

**Module Files:**
- `/root/bcm/ansible_collections/nvidia/bcm/plugins/modules/bcm_user.py`
- `/root/bcm/ansible_collections/nvidia/bcm/plugins/modules/bcm_group.py`
- `/root/bcm/ansible_collections/nvidia/bcm/plugins/modules/bcm_info.py`
- `/root/bcm/ansible_collections/nvidia/bcm/plugins/modules/bcm_power.py`

---

## Support

For issues, questions, or contributions:
- **Documentation**: See README.md, QUICKSTART.md, and module documentation
- **Issues**: GitHub issue tracker
- **Contributing**: See CONTRIBUTING.md

---

**Enjoy the new features in v1.1.0!** 🎉
