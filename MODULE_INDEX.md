# BCM Ansible Collection - Role and Module Reference

## Overview

The `fabiendupont.bcm` collection provides **high-level automation roles** for deploying OpenShift and RHEL clusters on NVIDIA Base Command Manager (BCM).

> **Important:** This is an independent community project and is **not officially supported or endorsed by NVIDIA**.

For low-level BCM entity management, this collection uses the official **NVIDIA Bright Computing collection** (`brightcomputing.bcm110`) which provides 190+ modules covering all BCM entities.

## Architecture

```
fabiendupont.bcm (High-level automation)
├── Dependencies
│   └── brightcomputing.bcm110 (190+ official BCM modules)
└── Roles (14 total)
    ├── Deployment Roles
    │   ├── openshift_cluster    - OpenShift cluster deployment
    │   └── rhel_cluster          - RHEL cluster deployment
    ├── Infrastructure Roles
    │   ├── pxe_setup             - PXE boot infrastructure
    │   ├── dns_setup             - DNS configuration
    │   └── registry_setup        - Container registry management
    ├── Shared Utility Roles
    │   ├── bcm_agent_image       - Build/push BCM agent container image
    │   ├── litenode_certificates - Generate per-node litenode certificates
    │   ├── register_bcm_nodes    - Register nodes in BCM
    │   ├── convert_to_litenode   - Convert PhysicalNode to LiteNode
    │   └── pythoncm_setup        - Setup pythoncm for dynamic inventory
    └── Configuration Roles
        ├── bcm_agent             - BCM agent management on nodes
        ├── cluster_audit         - Cluster health checks
        ├── gpu_cluster_config    - GPU cluster configuration
        └── network_optimization  - Network performance tuning
```

## Official BCM Modules (brightcomputing.bcm110)

The `fabiendupont.bcm` collection depends on and uses the official NVIDIA Bright Computing collection for all BCM entity operations.

**Installation:**
```bash
ansible-galaxy collection install fabiendupont.bcm
# This automatically installs brightcomputing.bcm110 as a dependency
```

### Core Entity Management

#### Categories
```yaml
- brightcomputing.bcm110.category:
    name: "openshift-master"
    state: present
    bootLoader: "syslinux"
    bootLoaderProtocol: "http"
    kernelParameters: "console=ttyS0"
    softwareImageProxy:
      parentSoftwareImage: "rocky-9"
```

**Documentation:** `ansible-doc brightcomputing.bcm110.category`

#### Nodes
```yaml
# Physical Nodes
- brightcomputing.bcm110.physical_node:
    name: "node001"
    state: present
    category: "compute"
    mac: "52:54:00:11:22:33"

# LiteNodes (for BCM agent management)
- brightcomputing.bcm110.lite_node:
    name: "node001"
    state: present
```

**Documentation:**
- `ansible-doc brightcomputing.bcm110.physical_node`
- `ansible-doc brightcomputing.bcm110.lite_node`

#### Networks
```yaml
- brightcomputing.bcm110.network:
    name: "compute-network"
    state: present
    network: "10.0.0.0"
    netmask: "255.255.0.0"
```

**Documentation:** `ansible-doc brightcomputing.bcm110.network`

#### Software Images
```yaml
- brightcomputing.bcm110.software_image:
    name: "rocky-9-gpu"
    state: present
```

**Documentation:** `ansible-doc brightcomputing.bcm110.software_image`

#### Certificates
```yaml
- brightcomputing.bcm110.certificate:
    commonName: "node001"
    profile: "admin"
    bits: 4096
    state: present
```

**Documentation:** `ansible-doc brightcomputing.bcm110.certificate`

### Query Modules

Each entity type has a corresponding `*_info` module for querying:

```yaml
# Query category
- brightcomputing.bcm110.category_info:
    name: "openshift-master"
  register: category_info

# Query nodes
- brightcomputing.bcm110.physical_node_info:
    name: "node001"
  register: node_info

# Query networks
- brightcomputing.bcm110.network_info:
    name: "compute-network"
  register: network_info
```

### Advanced Modules

The official collection provides 190+ modules including:

**Node Types:**
- `physical_node`, `lite_node`, `cloud_node`, `dpu_node`, `head_node`

**Infrastructure:**
- `network`, `partition`, `rack`, `chassis`, `switch`
- `power_distribution_unit`, `cooling_distribution_unit`

**Workload Managers:**
- `slurm_wlm_cluster`, `pbs_pro_wlm_cluster`, `lsf_wlm_cluster`
- `slurm_job_queue`, `pbs_pro_job_queue`, `lsf_job_queue`

**Storage:**
- `bee_gfs_cluster`, `fs_part`

**Cloud Providers:**
- `ec2_provider`, `ec2_region`, `ec2_type`
- `azure_provider`, `azure_location`, `azure_vm_size`
- `gcp_provider`, `gcp_zone`, `gcp_machine_type`
- `oci_provider`, `oci_region`, `oci_shape`
- `os_cloud_provider`, `os_cloud_region`, `os_cloud_flavor`

**Kubernetes:**
- `kube_cluster`, `etcd_cluster`

**Monitoring:**
- `monitoring_trigger`, `monitoring_measurable_metric`
- `monitoring_data_producer_gpu`, `monitoring_data_producer_cpu`
- `monitoring_drain_action`, `monitoring_email_action`

**User Management:**
- `user`, `group`, `profile`

**Configuration:**
- `configuration_overlay`, `software_image_file_selection`

**Full List:** https://galaxy.ansible.com/ui/repo/published/brightcomputing/bcm110/

## High-Level Roles (fabiendupont.bcm)

The `fabiendupont.bcm` collection provides specialized roles for common deployment scenarios.

### openshift_cluster

Automates OpenShift Agent-Based Installer deployment via PXE boot on BCM.

**Features:**
- OpenShift tools installation (oc, openshift-install)
- Agent-based installer artifact generation
- PXE infrastructure setup (software images, boot files)
- BCM category creation and node registration
- MAC-based Ignition file provisioning
- PhysicalNode → LiteNode conversion
- BCM Lite Daemon DaemonSet deployment
- Certificate management (bootstrap + per-node)

**Usage:**
```yaml
- name: Deploy OpenShift cluster
  hosts: bcm_headnode
  roles:
    - fabiendupont.bcm.openshift_cluster
  vars:
    cluster_name: "test-ocp"
    openshift_version: "4.20"
    node_roles:
      - name: "master"
        category: "openshift-master"
```

**Documentation:** [docs/AUTOMATED_OPENSHIFT_DEPLOYMENT.md](docs/AUTOMATED_OPENSHIFT_DEPLOYMENT.md)

### pxe_setup

Sets up PXE boot infrastructure for operating system deployment.

**Features:**
- HTTP/TFTP server configuration
- Software image management
- Boot file installation
- MAC-based boot configuration

**Usage:**
```yaml
- name: Setup PXE infrastructure
  hosts: bcm_headnode
  roles:
    - fabiendupont.bcm.pxe_setup
  vars:
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

**Usage:**
```yaml
- name: Setup DNS
  hosts: bcm_headnode
  roles:
    - fabiendupont.bcm.dns_setup
  vars:
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
- Post-installation configuration

**Usage:**
```yaml
- name: Deploy RHEL cluster
  hosts: bcm_headnode
  roles:
    - fabiendupont.bcm.rhel_cluster
  vars:
    rhel_version: "9.5"
```

**Documentation:** [docs/USAGE_GUIDE_RHEL_DEPLOYMENT.md](docs/USAGE_GUIDE_RHEL_DEPLOYMENT.md)

### registry_setup

Deploys container registry on BCM head node using systemd quadlets.

**Features:**
- Podman-based registry deployment
- TLS certificate signed by BCM CA
- Systemd service management
- Health check verification

**Usage:**
```yaml
- name: Setup container registry
  hosts: bcm_headnode
  roles:
    - fabiendupont.bcm.registry_setup
  vars:
    registry_port: 5000
```

**Documentation:** [roles/registry_setup/README.md](roles/registry_setup/README.md)

### bcm_agent_image

Builds and optionally pushes BCM agent container image.

**Features:**
- Clones nvidia-bcm-lite-daemon repository
- Builds container image with podman
- Optional registry push
- Idempotent operations

**Usage:**
```yaml
- name: Build BCM agent image
  hosts: bcm_headnode
  roles:
    - fabiendupont.bcm.bcm_agent_image
  vars:
    bcm_agent_push_to_registry: true
    bcm_agent_registry_host: "registry.example.com:5000"
```

**Documentation:** [roles/bcm_agent_image/README.md](roles/bcm_agent_image/README.md)

### litenode_certificates

Generates per-node litenode certificates for BCM agent authentication.

**Features:**
- Creates certificates via BCM CA
- Supports 3 directory structures (flat, per_node, per_mac)
- Idempotent certificate generation
- Configurable validity period

**Usage:**
```yaml
- name: Generate litenode certificates
  hosts: bcm_headnode
  roles:
    - fabiendupont.bcm.litenode_certificates
  vars:
    cluster_nodes: "{{ cluster_nodes }}"
    litenode_certs_dir: "/path/to/certs"
    litenode_cert_dir_structure: "flat"
```

**Documentation:** [roles/litenode_certificates/README.md](roles/litenode_certificates/README.md)

### register_bcm_nodes

Registers nodes in BCM with automatic or provided category assignment.

**Features:**
- Auto mode: dynamic category generation
- Provided mode: use inventory categories
- Validates node data
- Single registration task

**Usage:**
```yaml
- name: Register nodes
  hosts: bcm_headnode
  roles:
    - fabiendupont.bcm.register_bcm_nodes
  vars:
    bcm_node_category_mode: "auto"
    bcm_node_category_prefix: "openshift_133"
```

**Documentation:** [roles/register_bcm_nodes/README.md](roles/register_bcm_nodes/README.md)

### convert_to_litenode

Converts PhysicalNode to LiteNode after OS installation.

**Features:**
- SSH accessibility check
- Optional installation verification
- PhysicalNode deletion
- LiteNode creation
- Handles node reboot

**Usage:**
```yaml
- name: Convert to LiteNode
  hosts: bcm_headnode
  roles:
    - fabiendupont.bcm.convert_to_litenode
  vars:
    cluster_nodes: "{{ cluster_nodes }}"
    ssh_wait_timeout: 600
```

**Documentation:** [roles/convert_to_litenode/README.md](roles/convert_to_litenode/README.md)

### pythoncm_setup

Sets up pythoncm library for dynamic inventory plugin usage.

**Features:**
- Extracts pythoncm from BCM head node
- Builds Python wheel
- Installs in local environment
- Enables dynamic inventory

**Usage:**
```yaml
- name: Setup pythoncm
  hosts: bcm_headnode
  roles:
    - fabiendupont.bcm.pythoncm_setup
```

**Documentation:** [roles/pythoncm_setup/README.md](roles/pythoncm_setup/README.md)

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

**Documentation:** `ansible-doc -t inventory fabiendupont.bcm.bcm_inventory`

## Complete Example

```yaml
---
- name: Deploy OpenShift cluster on BCM
  hosts: bcm_headnode
  become: true

  vars:
    cluster_name: "production-ocp"
    openshift_version: "4.20"
    cluster_domain: "example.com"

    node_roles:
      - name: "master"
        category: "ocp-master"
      - name: "worker"
        category: "ocp-worker"

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

  tasks:
    # Setup DNS
    - name: Configure DNS for cluster
      ansible.builtin.include_role:
        name: fabiendupont.bcm.dns_setup

    # Setup PXE infrastructure
    - name: Prepare PXE boot environment
      ansible.builtin.include_role:
        name: fabiendupont.bcm.pxe_setup

    # Deploy OpenShift
    - name: Deploy OpenShift cluster
      ansible.builtin.include_role:
        name: fabiendupont.bcm.openshift_cluster

    # Verify with official modules
    - name: Query cluster nodes
      brightcomputing.bcm110.lite_node_info:
      register: lite_nodes

    - name: Display node status
      ansible.builtin.debug:
        msg: "{{ lite_nodes }}"
```

## Additional Resources

- **Official Collection:** https://galaxy.ansible.com/ui/repo/published/brightcomputing/bcm110/
- **Collection README:** [README.md](README.md)
- **Quick Start:** [QUICKSTART.md](QUICKSTART.md)
- **Documentation:** [docs/](docs/)
- **GitHub:** https://github.com/fabiendupont/nvidia-bcm-ansible

## Support

> **Important:** This is a community project and is not officially supported by NVIDIA.

- **Community support:** https://github.com/fabiendupont/nvidia-bcm-ansible/issues
- **Official BCM modules (`brightcomputing.bcm110`):** Contact NVIDIA Bright Computing support
