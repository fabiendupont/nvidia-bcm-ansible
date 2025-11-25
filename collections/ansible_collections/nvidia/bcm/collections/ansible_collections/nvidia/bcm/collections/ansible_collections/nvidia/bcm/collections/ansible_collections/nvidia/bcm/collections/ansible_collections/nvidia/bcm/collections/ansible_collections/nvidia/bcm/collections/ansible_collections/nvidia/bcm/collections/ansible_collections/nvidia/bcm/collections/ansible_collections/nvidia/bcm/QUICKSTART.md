# NVIDIA BCM Ansible Collection - Quick Start Guide

## Installation

### Prerequisites

- **NVIDIA Base Command Manager** 11.0 or later
- **Red Hat Enterprise Linux 9** (on the control node)
- **Ansible** 2.14 or later
- **Python** 3.6 or later
- **pythoncm** package from BCM repository

### Step 1: Install System Dependencies

On your Ansible control node (typically the BCM head node):

```bash
# Install Ansible
dnf install -y ansible-core

# Install Python dependencies
dnf install -y python3-lxml python3-passlib python3-tabulate python3-pyOpenSSL

# Install BCM pythoncm package
dnf install -y cmdaemon-pythoncm
```

### Step 2: Install the Collection

#### Option A: From Local Tarball (Recommended for now)

```bash
# Install from the built package
ansible-galaxy collection install /root/bcm/ansible_collections/nvidia/bcm/nvidia-bcm-1.0.0.tar.gz
```

#### Option B: From Source Directory

```bash
# Install directly from source
ansible-galaxy collection install /root/bcm/ansible_collections/nvidia/bcm
```

#### Option C: Using requirements.yml

Create a `requirements.yml` file:

```yaml
---
collections:
  - name: /root/bcm/ansible_collections/nvidia/bcm/nvidia-bcm-1.0.0.tar.gz
    type: file
```

Then install:

```bash
ansible-galaxy collection install -r requirements.yml
```

### Step 3: Verify Installation

```bash
# List installed collections
ansible-galaxy collection list | grep nvidia.bcm

# View module documentation
ansible-doc nvidia.bcm.bcm_node
ansible-doc nvidia.bcm.bcm_category

# View inventory plugin documentation
ansible-doc -t inventory nvidia.bcm.bcm_inventory
```

Expected output:
```
nvidia.bcm    1.0.0
```

---

## Quick Test

### Test 1: Use the Dynamic Inventory

Create `test_inventory.yml`:

```yaml
plugin: nvidia.bcm.bcm_inventory
host: localhost
```

List all hosts:

```bash
ansible-inventory -i test_inventory.yml --list
ansible-inventory -i test_inventory.yml --graph
```

### Test 2: Query a Node

```bash
ansible localhost -m nvidia.bcm.bcm_node -a "name=bcm11-headnode state=query"
```

### Test 3: Run a Simple Playbook

Create `test.yml`:

```yaml
---
- name: Test BCM Collection
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Query default category
      nvidia.bcm.bcm_category:
        name: default
        state: query
      register: result

    - name: Display result
      debug:
        var: result.category
```

Run it:

```bash
ansible-playbook test.yml
```

---

## First Real Playbook

Here's a practical example that queries your cluster configuration:

```yaml
---
- name: BCM Cluster Audit
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Get head node info
      nvidia.bcm.bcm_node:
        name: bcm11-headnode
        state: query
      register: headnode

    - name: Get default category
      nvidia.bcm.bcm_category:
        name: default
        state: query
      register: category

    - name: Get software image
      nvidia.bcm.bcm_software_image:
        name: default-image
        state: query
      register: image

    - name: Get internal network
      nvidia.bcm.bcm_network:
        name: internalnet
        state: query
      register: network

    - name: Display cluster summary
      debug:
        msg: |
          BCM Cluster Configuration:
            Head Node: {{ headnode.node.hostname }} ({{ headnode.node.type }})
            Default Category: {{ category.category.name }}
            Software Image: {{ image.image.name }} ({{ image.image.kernel_version }})
            Internal Network: {{ network.network.domain_name }} (MTU: {{ network.network.mtu }})
```

---

## Using with Ansible Automation Platform

If you're using Red Hat Ansible Automation Platform:

### 1. Create a Project

In AAP, create a new project pointing to your playbook repository.

### 2. Create a Credential

- **Type**: Machine
- **Username**: root
- **Private Key**: Your SSH key for BCM head node

### 3. Add Collection to Execution Environment

Create a `requirements.yml` in your project:

```yaml
---
collections:
  - name: nvidia.bcm
    source: https://your-automation-hub/api/galaxy/
```

### 4. Create Job Template

- **Inventory**: BCM Inventory Source (using bcm_inventory plugin)
- **Project**: Your BCM playbooks project
- **Playbook**: Select your playbook
- **Credentials**: BCM head node credential

---

## Configuration Files

### Ansible Configuration

Create `ansible.cfg` in your project:

```ini
[defaults]
inventory = inventory/bcm.yml
host_key_checking = False
collections_path = ./collections:~/.ansible/collections:/usr/share/ansible/collections

[inventory]
enable_plugins = nvidia.bcm.bcm_inventory
```

### Inventory Configuration

Create `inventory/bcm.yml`:

```yaml
plugin: nvidia.bcm.bcm_inventory
host: localhost
pythoncm_path: /cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages

# Group nodes by type
keyed_groups:
  - key: bcm_type
    prefix: type

# Add computed variables
compose:
  ansible_host: bcm_ip
```

---

## Common Issues & Solutions

### Issue 1: ModuleNotFoundError: No module named 'pythoncm'

**Solution**:
```bash
# Ensure pythoncm is installed
dnf install -y cmdaemon-pythoncm

# Or set PYTHONPATH
export PYTHONPATH=/cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages:$PYTHONPATH
```

### Issue 2: Import Error for lxml, passlib, etc.

**Solution**:
```bash
dnf install -y python3-lxml python3-passlib python3-tabulate python3-pyOpenSSL
```

### Issue 3: Certificate/Authentication Errors

**Solution**:
```bash
# Check admin certificates exist
ls -la ~/.cm/admin.pem ~/.cm/admin.key

# Ensure correct permissions
chmod 600 ~/.cm/admin.pem ~/.cm/admin.key
```

### Issue 4: "Collection not found"

**Solution**:
```bash
# Check where Ansible looks for collections
ansible-galaxy collection list

# Install to user directory
ansible-galaxy collection install nvidia-bcm-1.0.0.tar.gz --force

# Or install system-wide
sudo ansible-galaxy collection install nvidia-bcm-1.0.0.tar.gz --force
```

---

## Next Steps

1. **Read the full documentation**: See [INSTALL.md](INSTALL.md) for detailed installation
2. **Review examples**: Check the [playbooks/](playbooks/) directory
3. **Explore modules**: Run `ansible-doc nvidia.bcm.<module>` for each module
4. **Check development guide**: See [docs/DEVELOPMENT.md](docs/DEVELOPMENT.md) to create custom modules

---

## Available Modules

| Module | Purpose | Status |
|--------|---------|--------|
| bcm_inventory | Dynamic inventory plugin | ✅ Production |
| bcm_node | Manage cluster nodes | ✅ Production |
| bcm_category | Manage node categories | ✅ Production |
| bcm_software_image | Manage OS images | ✅ Production |
| bcm_network | Manage networks | ✅ Production |
| bcm_overlay | Query configuration overlays | ✅ Query-only |

---

## Getting Help

- **Module Documentation**: `ansible-doc nvidia.bcm.<module_name>`
- **Collection Issues**: Create an issue in the repository
- **NVIDIA BCM Documentation**: https://docs.nvidia.com/base-command-manager/

---

## Support Matrix

| Component | Version | Status |
|-----------|---------|--------|
| BCM | 11.0+ | ✅ Tested |
| RHEL | 9.x | ✅ Tested |
| Ansible Core | 2.14+ | ✅ Supported |
| Python | 3.6+ | ✅ Supported |

---

Happy Automating! 🚀
