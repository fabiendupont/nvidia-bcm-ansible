# NVIDIA BCM Ansible Collection - Module Index

## Overview

Complete reference for all modules in the nvidia.bcm collection.

## Modules

### Information Gathering

#### bcm_info
Query BCM cluster information and configuration.

```yaml
- nvidia.bcm.bcm_info:
    gather_subset:
      - cluster
      - version
      - networks
```

**Capabilities:**
- Cluster configuration
- Version information
- Network details
- System status

**Documentation:** `ansible-doc nvidia.bcm.bcm_info`

---

### Node Management

#### bcm_node
Manage compute nodes and devices.

```yaml
- nvidia.bcm.bcm_node:
    name: node001
    state: present
    category: compute
    mac: "52:54:00:11:22:33"
```

**Capabilities:**
- List devices
- Query node details
- Modify node properties
- Assign categories
- Set MAC addresses, hostnames, IPs

**Documentation:** `ansible-doc nvidia.bcm.bcm_node`

---

### Network Management

#### bcm_network
Manage BCM networks.

```yaml
- nvidia.bcm.bcm_network:
    name: compute-network
    state: present
    network: 10.0.0.0
    netmask: 255.255.0.0
```

**Capabilities:**
- Create networks
- Modify network configuration
- Query network details
- Remove networks

**Documentation:** `ansible-doc nvidia.bcm.bcm_network`

---

### Category Management

#### bcm_category
Manage node categories and software images.

```yaml
- nvidia.bcm.bcm_category:
    name: gpu-nodes
    state: present
    software_image: rocky-9-gpu
```

**Capabilities:**
- Create categories
- Assign software images
- Set category properties
- Remove categories

**Documentation:** `ansible-doc nvidia.bcm.bcm_category`

---

### User Management

#### bcm_user
Manage BCM users.

```yaml
- nvidia.bcm.bcm_user:
    name: newuser
    state: present
    uid: "2000"
    home: /home/newuser
```

**Capabilities:**
- Create users
- Modify user properties (UID, GID, home, shell, email)
- Query user information
- Remove users

**Documentation:** `ansible-doc nvidia.bcm.bcm_user`

---

### Group Management

#### bcm_group
Manage BCM groups.

```yaml
- nvidia.bcm.bcm_group:
    name: developers
    state: present
    gid: "3000"
```

**Capabilities:**
- Create groups
- Modify group properties (GID)
- Query group information
- Remove groups

**Documentation:** `ansible-doc nvidia.bcm.bcm_group`

---

### Certificate Management

#### bcm_certificate
Manage X.509 certificates.

```yaml
- nvidia.bcm.bcm_certificate:
    serial_number: 26
    state: query
    cert_file: /tmp/node.pem
```

**Capabilities:**
- Query certificates (by serial, name, profile)
- Save certificates to files
- Revoke/unrevoke certificates
- Remove certificates
- Filter by profile or revocation status

**Documentation:** `ansible-doc nvidia.bcm.bcm_certificate`
**Guide:** README-CERTIFICATES.md

---

### Software Image Management

#### bcm_software_image
Manage software images.

```yaml
- nvidia.bcm.bcm_software_image:
    name: default-image
    state: query
```

**Capabilities:**
- Query software images
- View image properties

**Note:** Image creation limited by pythoncm API (images must be cloned)

**Documentation:** `ansible-doc nvidia.bcm.bcm_software_image`

---

### Configuration Management

#### bcm_overlay
Manage configuration overlays.

```yaml
- nvidia.bcm.bcm_overlay:
    name: gpu-settings
    state: present
```

**Capabilities:**
- Create configuration overlays
- Query overlay details
- Remove overlays

**Documentation:** `ansible-doc nvidia.bcm.bcm_overlay`

---

### Power Management

#### bcm_power
Control node power state.

```yaml
- nvidia.bcm.bcm_power:
    nodes:
      - node001
      - node002
    action: on
```

**Capabilities:**
- Power on/off nodes
- Query power status
- Power cycle
- Force power operations

**Documentation:** `ansible-doc nvidia.bcm.bcm_power`

---

## Plugins

### Inventory

#### bcm_inventory
Dynamic inventory plugin for BCM.

```yaml
# inventory.yml
plugin: nvidia.bcm.bcm_inventory
bcm_host: bcm-headnode
pythoncm_path: /cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages
groups:
  - category
  - rack
```

**Capabilities:**
- Discover nodes dynamically
- Group by category, rack, partition
- Auto-populate hostnames and IPs

**Documentation:** `ansible-doc -t inventory nvidia.bcm.bcm_inventory`

---

## Module Utilities

### bcm_common
Common utilities for BCM modules.

**Provides:**
- BCM connection management
- Error handling
- Parameter validation
- Common argument specs

**Used by:** All bcm_* modules

---

## Quick Reference

### Query Operations
```yaml
# Get cluster info
- nvidia.bcm.bcm_info:

# List all nodes
- nvidia.bcm.bcm_node:
    state: list

# Query specific network
- nvidia.bcm.bcm_network:
    name: internalnet
    state: query

# List certificates by profile
- nvidia.bcm.bcm_certificate:
    state: query
    filter_profile: node
```

### Create Operations
```yaml
# Create category
- nvidia.bcm.bcm_category:
    name: gpu-cluster
    state: present

# Create user
- nvidia.bcm.bcm_user:
    name: testuser
    state: present
    uid: "5000"

# Create network
- nvidia.bcm.bcm_network:
    name: storage-net
    state: present
    network: 10.10.0.0
    netmask: 255.255.255.0
```

### Modify Operations
```yaml
# Update node category
- nvidia.bcm.bcm_node:
    name: node001
    state: present
    category: new-category

# Update user shell
- nvidia.bcm.bcm_user:
    name: username
    state: present
    shell: /bin/zsh
```

### Delete Operations
```yaml
# Remove category
- nvidia.bcm.bcm_category:
    name: old-category
    state: absent

# Remove certificate
- nvidia.bcm.bcm_certificate:
    serial_number: 100
    state: absent
```

## Module Status

| Module | Status | Create | Read | Update | Delete | Tested |
|--------|--------|--------|------|--------|--------|--------|
| bcm_info | ✅ | N/A | ✅ | N/A | N/A | ✅ |
| bcm_node | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| bcm_network | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| bcm_category | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| bcm_user | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| bcm_group | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| bcm_certificate | ✅ | ⚠️ | ✅ | ✅ | ✅ | ✅ |
| bcm_software_image | ✅ | ⚠️ | ✅ | ❌ | ✅ | ✅ |
| bcm_overlay | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ |
| bcm_power | ✅ | N/A | ✅ | ✅ | N/A | ✅ |
| bcm_inventory | ✅ | N/A | ✅ | N/A | N/A | ✅ |

Legend:
- ✅ Fully supported
- ⚠️ Limited support (see module docs)
- ❌ Not supported
- N/A Not applicable

## See Also

- [README.md](README.md) - Collection overview
- [QUICKSTART.md](QUICKSTART.md) - Getting started guide
- [TEST_SUITE.md](TEST_SUITE.md) - Testing documentation
- [README-CERTIFICATES.md](README-CERTIFICATES.md) - Certificate management guide
- [ENTITY_CREATION_SUMMARY.md](ENTITY_CREATION_SUMMARY.md) - Technical details
