# BCM Ansible Collection

**Community-driven** Ansible collection for high-level automation on NVIDIA Base Command Manager (BCM) - deploying OpenShift and RHEL clusters with ease.

> **Important:** This is an independent community project by Fabien Dupont and is **not officially supported or endorsed by NVIDIA**. For official BCM modules, use the `brightcomputing.bcm110` collection.

## Overview

The `fabiendupont.bcm` collection provides **specialized roles** for automating complex deployment workflows on BCM infrastructure:

- **OpenShift Agent-Based Installer** - Automated PXE-based deployment
- **RHEL Cluster Deployment** - Kickstart-based provisioning
- **PXE Infrastructure** - HTTP/TFTP server configuration
- **DNS Management** - Cluster domain and VIP configuration

For low-level BCM entity management (categories, nodes, networks, etc.), this collection leverages the official **NVIDIA Bright Computing collection** (`brightcomputing.bcm110`) which provides 190+ modules.

## Architecture

```
fabiendupont.bcm (High-level automation)
├── Dependencies
│   └── brightcomputing.bcm110 (190+ official BCM modules)
│       └── pythoncm (BCM Python API)
└── Roles
    ├── openshift_cluster  - OpenShift Agent-Based Installer automation
    ├── rhel_cluster       - RHEL cluster deployment
    ├── pxe_setup          - PXE infrastructure setup
    └── dns_setup          - DNS configuration
```

## Requirements

- **Ansible:** 2.15 or later
- **Python:** 3.9 or later
- **BCM:** 11.0 or later
- **pythoncm:** Installed on BCM head node (provided by BCM)
- **Access:** BCM head node with cmdaemon

## Installation

Install the collection from Ansible Galaxy (includes official dependencies):

```bash
ansible-galaxy collection install fabiendupont.bcm
```

This automatically installs:
- `fabiendupont.bcm` - High-level automation roles
- `brightcomputing.bcm110` - Official BCM modules (190+)
- `containers.podman` - Container management

## Quick Start

### Deploy OpenShift Cluster

```yaml
---
- name: Deploy OpenShift 4.20 on BCM
  hosts: bcm_headnode
  become: true

  vars:
    cluster_name: "production-ocp"
    openshift_version: "4.20"
    openshift_pull_secret_path: "/path/to/pull-secret.json"

    node_roles:
      - name: "master"
        category: "ocp-master"

    cluster_nodes:
      - name: "master001"
        mac: "52:54:00:11:22:01"
        ip: "10.0.1.10"
        role: "master"
      - name: "master002"
        mac: "52:54:00:11:22:02"
        ip: "10.0.1.11"
        role: "master"
      - name: "master003"
        mac: "52:54:00:11:22:03"
        ip: "10.0.1.12"
        role: "master"

  roles:
    - fabiendupont.bcm.dns_setup
    - fabiendupont.bcm.pxe_setup
    - fabiendupont.bcm.openshift_cluster
```

**What it does:**
1. Installs OpenShift tools (oc, openshift-install)
2. Generates Agent-Based Installer artifacts
3. Creates BCM software images and categories
4. Sets up PXE boot infrastructure
5. Registers nodes as PhysicalNode
6. Configures MAC-based Ignition files
7. Nodes PXE boot and install OpenShift
8. Converts nodes to LiteNode
9. Deploys BCM Lite Daemon DaemonSet

See: [docs/AUTOMATED_OPENSHIFT_DEPLOYMENT.md](docs/AUTOMATED_OPENSHIFT_DEPLOYMENT.md)

### Deploy RHEL Cluster

```yaml
---
- name: Deploy RHEL 9.5 cluster
  hosts: bcm_headnode
  become: true

  vars:
    rhel_version: "9.5"
    rhel_iso_path: "/path/to/rhel-9.5.iso"

  roles:
    - fabiendupont.bcm.rhel_cluster
```

See: [docs/USAGE_GUIDE_RHEL_DEPLOYMENT.md](docs/USAGE_GUIDE_RHEL_DEPLOYMENT.md)

### Use Official BCM Modules

For direct BCM entity management, use the official `brightcomputing.bcm110` modules:

```yaml
---
- name: Manage BCM entities
  hosts: bcm_headnode
  tasks:
    # Create category
    - brightcomputing.bcm110.category:
        name: "gpu-nodes"
        state: present
        bootLoader: "syslinux"
        softwareImageProxy:
          parentSoftwareImage: "rocky-9-gpu"

    # Register node
    - brightcomputing.bcm110.physical_node:
        name: "node001"
        state: present
        category: "gpu-nodes"
        mac: "52:54:00:11:22:33"
        hostname: "node001.example.com"

    # Query node info
    - brightcomputing.bcm110.physical_node_info:
        name: "node001"
      register: node_info

    # Convert to LiteNode
    - brightcomputing.bcm110.lite_node:
        name: "node001"
        state: present
```

**Official Collection Documentation:**
- Galaxy: https://galaxy.ansible.com/ui/repo/published/brightcomputing/bcm110/
- Modules: `ansible-doc brightcomputing.bcm110.<module_name>`

## Roles

### openshift_cluster

Automates OpenShift Agent-Based Installer deployment via PXE boot.

**Features:**
- OpenShift tools installation (version-specific)
- Agent-config generation with node MAC addresses
- BCM software image creation (reusable across clusters)
- PXE boot file installation
- BCM category and node registration
- PhysicalNode → LiteNode conversion
- BCM Lite Daemon DaemonSet deployment
- Bootstrap certificate + per-node certificates

**Variables:**
```yaml
cluster_name: "test-ocp"
openshift_version: "4.20"
openshift_pull_secret_path: "/path/to/pull-secret.json"
openshift_api_vips: ["10.0.1.100"]
openshift_ingress_vips: ["10.0.1.101"]
node_roles:
  - name: "master"
    category: "ocp-master"
cluster_nodes:
  - name: "master001"
    mac: "52:54:00:11:22:01"
    ip: "10.0.1.10"
    role: "master"
```

**Documentation:** [docs/AUTOMATED_OPENSHIFT_DEPLOYMENT.md](docs/AUTOMATED_OPENSHIFT_DEPLOYMENT.md)

### pxe_setup

Sets up PXE boot infrastructure for OS deployment.

**Features:**
- HTTP/TFTP server configuration
- Software image management
- Boot file installation
- MAC-based boot configuration

**Variables:**
```yaml
pxe_os_type: "rhel"
pxe_version: "9.5"
```

**Documentation:** [docs/BCM_PXE_DEPLOYMENT_GUIDE.md](docs/BCM_PXE_DEPLOYMENT_GUIDE.md)

### dns_setup

Configures DNS for cluster networking.

**Features:**
- Dnsmasq configuration
- Forward/reverse DNS zones
- Cluster domain setup
- VIP DNS entries

**Variables:**
```yaml
cluster_name: "test-ocp"
cluster_domain: "example.com"
```

**Documentation:** [docs/DNS_ARCHITECTURE.md](docs/DNS_ARCHITECTURE.md)

### rhel_cluster

Deploys RHEL clusters via PXE boot.

**Features:**
- RHEL installation media preparation
- Kickstart configuration
- Node provisioning

**Variables:**
```yaml
rhel_version: "9.5"
rhel_iso_path: "/path/to/rhel.iso"
```

**Documentation:** [docs/USAGE_GUIDE_RHEL_DEPLOYMENT.md](docs/USAGE_GUIDE_RHEL_DEPLOYMENT.md)

## Plugins

### bcm_inventory

Dynamic inventory plugin for discovering BCM nodes.

**Usage:**
```yaml
# inventory.yml
plugin: fabiendupont.bcm.bcm_inventory
bcm_host: bcm-headnode
pythoncm_path: /cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages
groups:
  - category
  - rack
```

**Commands:**
```bash
ansible-inventory -i inventory.yml --list
ansible -i inventory.yml all -m ping
```

**Documentation:** `ansible-doc -t inventory fabiendupont.bcm.bcm_inventory`

## Official BCM Modules

The `brightcomputing.bcm110` collection provides 190+ modules for comprehensive BCM management.

### Core Modules

| Category | Modules |
|----------|---------|
| **Nodes** | `physical_node`, `lite_node`, `cloud_node`, `dpu_node`, `head_node` |
| **Infrastructure** | `category`, `network`, `partition`, `rack`, `chassis`, `switch` |
| **Storage** | `bee_gfs_cluster`, `fs_part` |
| **WLM** | `slurm_wlm_cluster`, `pbs_pro_wlm_cluster`, `lsf_wlm_cluster` |
| **Cloud** | `ec2_provider`, `azure_provider`, `gcp_provider`, `oci_provider` |
| **Management** | `user`, `group`, `certificate`, `software_image` |
| **Monitoring** | `monitoring_trigger`, `monitoring_data_producer_*` |
| **Kubernetes** | `kube_cluster`, `etcd_cluster` |

**Query Modules:** Each entity has a `*_info` module (e.g., `physical_node_info`, `category_info`)

**Full List:** https://galaxy.ansible.com/ui/repo/published/brightcomputing/bcm110/

## Documentation

- **[MODULE_INDEX.md](MODULE_INDEX.md)** - Complete module and role reference
- **[QUICKSTART.md](QUICKSTART.md)** - Getting started guide
- **[docs/](docs/)** - Detailed guides:
  - [AUTOMATED_OPENSHIFT_DEPLOYMENT.md](docs/AUTOMATED_OPENSHIFT_DEPLOYMENT.md)
  - [BCM_PXE_DEPLOYMENT_GUIDE.md](docs/BCM_PXE_DEPLOYMENT_GUIDE.md)
  - [DNS_ARCHITECTURE.md](docs/DNS_ARCHITECTURE.md)
  - [USAGE_GUIDE_RHEL_DEPLOYMENT.md](docs/USAGE_GUIDE_RHEL_DEPLOYMENT.md)
- **[TEST_SUITE.md](TEST_SUITE.md)** - Testing documentation

## Examples

### Complete OpenShift Deployment

```yaml
---
- name: Deploy OpenShift cluster with VIPs
  hosts: bcm_headnode
  become: true

  vars:
    cluster_name: "production-ocp"
    openshift_version: "4.20"
    cluster_domain: "example.com"
    openshift_pull_secret_path: "/root/pull-secret.json"

    # Virtual IPs
    openshift_api_vips: ["10.0.1.100"]
    openshift_ingress_vips: ["10.0.1.101"]

    # Node roles
    node_roles:
      - name: "master"
        category: "ocp-master"
      - name: "worker"
        category: "ocp-worker"

    # Cluster nodes
    cluster_nodes:
      - name: "master001"
        mac: "52:54:00:11:22:01"
        ip: "10.0.1.10"
        role: "master"
      - name: "master002"
        mac: "52:54:00:11:22:02"
        ip: "10.0.1.11"
        role: "master"
      - name: "master003"
        mac: "52:54:00:11:22:03"
        ip: "10.0.1.12"
        role: "master"
      - name: "worker001"
        mac: "52:54:00:11:22:11"
        ip: "10.0.1.20"
        role: "worker"
      - name: "worker002"
        mac: "52:54:00:11:22:12"
        ip: "10.0.1.21"
        role: "worker"

  roles:
    - fabiendupont.bcm.dns_setup
    - fabiendupont.bcm.pxe_setup
    - fabiendupont.bcm.openshift_cluster
```

### Verify Deployment

```yaml
---
- name: Verify cluster status
  hosts: bcm_headnode
  tasks:
    # Query LiteNodes
    - brightcomputing.bcm110.lite_node_info:
      register: lite_nodes

    - debug:
        msg: "{{ lite_nodes }}"

    # Check OpenShift cluster
    - name: Get cluster nodes
      ansible.builtin.command:
        cmd: "/openshift/tools/{{ openshift_version }}/oc get nodes"
      environment:
        KUBECONFIG: "/openshift/clusters/{{ cluster_name }}/auth/kubeconfig"
      register: nodes

    - debug:
        var: nodes.stdout_lines
```

## Configuration

### Ansible Configuration

Recommended `ansible.cfg`:

```ini
[defaults]
host_key_checking = False
inventory = inventory/

[inventory]
enable_plugins = fabiendupont.bcm.bcm_inventory, yaml, ini
```

### Python Interpreter

For modules requiring pythoncm, configure the Python interpreter:

```yaml
# In inventory or playbook
ansible_python_interpreter: /cm/local/apps/python3/bin/python3
```

Or in `ansible.cfg`:

```ini
[defaults]
interpreter_python = /cm/local/apps/python3/bin/python
```

## Support

> **Important:** This is a community project. It is not officially supported by NVIDIA.

- **Community support:** https://github.com/fabiendupont/nvidia-bcm-ansible/issues
- **Official BCM modules (`brightcomputing.bcm110`):** Contact NVIDIA Bright Computing support
- **BCM platform:** Contact NVIDIA Bright Computing support

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

## License

GPL-3.0-or-later

## Author

Fabien Dupont <fdupont@redhat.com>

## Related Projects

- **brightcomputing.bcm110** - Official NVIDIA Bright Computing Ansible collection
- **nvidia-bcm-lite-daemon** - BCM integration for Kubernetes/OpenShift
- **ocp-nvidia-bcm** - Alternative OpenShift BCM integration via MachineConfig
