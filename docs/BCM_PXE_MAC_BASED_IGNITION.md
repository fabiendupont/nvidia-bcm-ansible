# BCM PXE with MAC-based Ignition and Simplified Category Naming

## Overview

This approach combines:
- **Simplified category naming**: `openshift-<version>-<cluster>-<role>`
- **MAC-based Ignition files**: Each node gets its own Ignition based on MAC address
- **Reusable categories**: Same category serves initial and expansion nodes

## Category Naming Convention

### Pattern

```
openshift-<ocp_version>-<cluster_name>-<node_role>
```

### Examples

```
openshift-416-prod-master        # OpenShift 4.16, prod cluster, master nodes
openshift-416-prod-worker        # OpenShift 4.16, prod cluster, worker nodes
openshift-416-prod-infra         # OpenShift 4.16, prod cluster, infra nodes
openshift-416-test-master        # OpenShift 4.16, test cluster, master nodes
openshift-417-prod-worker        # OpenShift 4.17, prod cluster, worker nodes (upgrade)
```

### For RHEL + Slurm

```
slurm-<cluster_name>-<role>
```

Examples:
```
slurm-hpc01-login
slurm-hpc01-compute
slurm-hpc01-gpu-a100
slurm-hpc01-storage
```

## MAC-based Ignition File Structure

### File Organization

```
/tftpboot/
├── repos/
│   └── openshift-4.16/
│       ├── agent.x86_64.iso
│       └── rootfs.img
│
├── images/
│   ├── installer-openshift-4.16/      # Shared boot files
│   │   ├── vmlinuz
│   │   └── initrd
│   ├── openshift-416-prod-master -> installer-openshift-4.16/
│   ├── openshift-416-prod-worker -> installer-openshift-4.16/
│   └── openshift-416-test-master -> installer-openshift-4.16/
│
└── ignition/
    ├── openshift-4.16/                # Version-specific
    │   ├── prod/                      # Cluster-specific
    │   │   ├── master/                # Role-specific
    │   │   │   ├── 52-54-00-aa-bb-01.ign    # MAC-based
    │   │   │   ├── 52-54-00-aa-bb-02.ign
    │   │   │   └── 52-54-00-aa-bb-03.ign
    │   │   ├── worker/
    │   │   │   ├── 52-54-00-aa-bb-10.ign    # Initial workers
    │   │   │   ├── 52-54-00-aa-bb-11.ign
    │   │   │   ├── 52-54-00-cc-dd-01.ign    # Expansion workers (added later)
    │   │   │   └── 52-54-00-cc-dd-02.ign
    │   │   └── infra/
    │   │       └── 52-54-00-ee-ff-01.ign
    │   └── test/
    │       ├── master/
    │       │   └── 52-54-00-99-88-01.ign
    │       └── worker/
    │           └── 52-54-00-99-88-10.ign
    └── openshift-4.17/                # Next version
        └── prod/
            └── ...
```

### MAC Address Format for Filenames

Convert MAC address to filename:
- **MAC address**: `52:54:00:AA:BB:01`
- **Filename**: `52-54-00-aa-bb-01.ign` (lowercase, colons→hyphens)

## How It Works

### 1. PXE Boot Process

```
Node boots via PXE
  ↓
DHCP provides: IP, next-server, boot file
  ↓
TFTP downloads: pxelinux.0
  ↓
TFTP downloads PXE config (tries in order):
  1. /tftpboot/pxelinux.cfg/01-52-54-00-aa-bb-01  ← MAC-based (not used by BCM)
  2. /tftpboot/pxelinux.cfg/C0A8FE01            ← IP-based (hex)
  3. /tftpboot/pxelinux.cfg/default             ← Falls back to default
  4. → default → category.default               ← BCM uses category-based

BCM registers node with category → uses category PXE config
  ↓
Kernel parameter includes Ignition URL with ${NODE_MAC} variable
  ↓
Node downloads: http://.../ignition/.../52-54-00-aa-bb-01.ign
```

### 2. Kernel Parameters with MAC Variable

BCM can substitute node-specific variables in kernel parameters. We leverage this:

```bash
# Category kernel parameters
kernelparameters="coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/openshift-4.16/prod/worker/NODE_MAC.ign ..."
```

**Challenge**: BCM doesn't natively support `${NODE_MAC}` substitution in kernel params.

**Solutions**:

#### Solution 1: Dynamic Script (Recommended)

Create a simple HTTP handler that redirects based on requesting IP to MAC:

```bash
# /tftpboot/ignition/get-ignition.sh
#!/bin/bash
# Maps IP to MAC, returns correct Ignition file

IP=$1
CLUSTER=$2
ROLE=$3

# Query BCM for MAC address based on IP
MAC=$(cmsh -c "device use $(cmsh -c "device list" | grep $IP | awk '{print $1}'); get mac" | tr ':' '-' | tr 'A-Z' 'a-z')

# Serve Ignition file
cat /tftpboot/ignition/openshift-4.16/${CLUSTER}/${ROLE}/${MAC}.ign
```

#### Solution 2: Per-Node Kernel Parameters (Simpler)

Set kernel parameters at the **node level** instead of category level:

```bash
cmsh << 'EOF'
device
use master-0
set kernelparameters "coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/openshift-4.16/prod/master/52-54-00-aa-bb-01.ign"
commit
EOF
```

BCM allows node-specific kernel parameters that override category defaults!

#### Solution 3: Static Ignition URL per Node (Production Ready)

Use a well-known pattern that the web server can interpret:

```bash
# Category kernel parameters (template)
kernelparameters="coreos.inst.ignition_url=http://10.141.255.254:8080/ignition-api/openshift-4.16/prod/worker/NODE ..."
```

Then create a simple API endpoint `/ignition-api/` that:
1. Receives request from specific IP
2. Looks up MAC from BCM database
3. Returns appropriate Ignition file

## Implementation Strategy

### Recommended: Per-Node Kernel Parameters

This is the cleanest approach that works natively with BCM.

#### Step 1: Create Shared Category (No Ignition URL Yet)

```bash
cmsh << 'EOF'
category
add openshift-416-prod-master
set bootloader syslinux
set bootloaderprotocol HTTP
set kernelparameters "coreos.inst.install_dev=/dev/sda coreos.inst.image_url=http://10.141.255.254:8080/tftpboot/repos/openshift-4.16/rootfs.img coreos.live.rootfs_url=http://10.141.255.254:8080/tftpboot/repos/openshift-4.16/rootfs.img console=tty0"
set kerneloutputconsole tty0
set installmode NEVER
set newnodeinstallmode NEVER
set notes "OpenShift 4.16 - Production Cluster - Master Nodes"
commit

category
add openshift-416-prod-worker
set bootloader syslinux
set bootloaderprotocol HTTP
set kernelparameters "coreos.inst.install_dev=/dev/sda coreos.inst.image_url=http://10.141.255.254:8080/tftpboot/repos/openshift-4.16/rootfs.img coreos.live.rootfs_url=http://10.141.255.254:8080/tftpboot/repos/openshift-4.16/rootfs.img console=tty0"
set kerneloutputconsole tty0
set installmode NEVER
set newnodeinstallmode NEVER
set notes "OpenShift 4.16 - Production Cluster - Worker Nodes"
commit
EOF
```

#### Step 2: Generate MAC-based Ignition Files

```bash
# Create directory structure
mkdir -p /tftpboot/ignition/openshift-4.16/prod/{master,worker,infra}

# Generate Ignition for each node
# This would typically be done by openshift-install agent create image
# or extracted from the agent ISO

# Example: Master node ignition
MAC_FILENAME="52-54-00-aa-bb-01"
cat > /tftpboot/ignition/openshift-4.16/prod/master/${MAC_FILENAME}.ign << 'EOF'
{
  "ignition": {
    "version": "3.2.0"
  },
  "storage": {
    "files": [
      {
        "path": "/etc/hostname",
        "mode": 420,
        "contents": {
          "source": "data:,master-0.ocp-prod.example.com"
        }
      }
    ]
  }
}
EOF

chmod 644 /tftpboot/ignition/openshift-4.16/prod/master/${MAC_FILENAME}.ign
```

#### Step 3: Register Nodes with Node-Specific Kernel Parameters

```bash
# Master 0
cmsh << 'EOF'
device
add genericdevice master-0
set mac 52:54:00:AA:BB:01
set ip 10.141.160.50
set category openshift-416-prod-master
set kernelparameters "coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/openshift-4.16/prod/master/52-54-00-aa-bb-01.ign"
commit
EOF

# Worker 0 (initial deployment)
cmsh << 'EOF'
device
add genericdevice worker-0
set mac 52:54:00:AA:BB:10
set ip 10.141.160.60
set category openshift-416-prod-worker
set kernelparameters "coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/openshift-4.16/prod/worker/52-54-00-aa-bb-10.ign"
commit
EOF

# Worker 5 (expansion - months later, same category!)
cmsh << 'EOF'
device
add genericdevice worker-5
set mac 52:54:00:CC:DD:01
set ip 10.141.160.65
set category openshift-416-prod-worker
set kernelparameters "coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/openshift-4.16/prod/worker/52-54-00-cc-dd-01.ign"
commit
EOF
```

**Key Point**: Node-level `kernelparameters` override category-level parameters!

### Verification

```bash
# Check node configuration
cmsh -c 'device; use worker-5; show' | grep -A5 "Kernel parameters"

# Should show node-specific Ignition URL
```

## Ansible Playbook Implementation

```yaml
---
- name: Setup OpenShift with MAC-based Ignition
  hosts: localhost
  become: yes

  vars:
    openshift_version: "4.16"
    cluster_name: "prod"
    bcm_server: "10.141.255.254"

    # Paths
    ignition_base: "/tftpboot/ignition/openshift-{{ openshift_version }}/{{ cluster_name }}"
    repo_path: "/tftpboot/repos/openshift-{{ openshift_version }}"

    # Node definitions
    master_nodes:
      - name: master-0
        mac: "52:54:00:AA:BB:01"
        ip: "10.141.160.50"
        role: master
      - name: master-1
        mac: "52:54:00:AA:BB:02"
        ip: "10.141.160.51"
        role: master

    worker_nodes:
      - name: worker-0
        mac: "52:54:00:AA:BB:10"
        ip: "10.141.160.60"
        role: worker
      - name: worker-5
        mac: "52:54:00:CC:DD:01"
        ip: "10.141.160.65"
        role: worker
        phase: expansion  # Added later

  tasks:
    # =========================================================================
    # PHASE 1: Create Ignition Directory Structure
    # =========================================================================

    - name: Create ignition directories
      ansible.builtin.file:
        path: "{{ ignition_base }}/{{ item }}"
        state: directory
        mode: '0755'
      loop:
        - master
        - worker
        - infra

    # =========================================================================
    # PHASE 2: Generate MAC-based Ignition Files
    # =========================================================================

    - name: Generate MAC-based filename
      ansible.builtin.set_fact:
        mac_filename: "{{ item.mac | lower | replace(':', '-') }}"
      loop: "{{ master_nodes + worker_nodes }}"
      register: mac_conversions

    - name: Generate Ignition configs for masters
      ansible.builtin.template:
        src: ignition-master.ign.j2
        dest: "{{ ignition_base }}/master/{{ item.mac | lower | replace(':', '-') }}.ign"
        mode: '0644'
      loop: "{{ master_nodes }}"
      vars:
        node: "{{ item }}"

    - name: Generate Ignition configs for workers
      ansible.builtin.template:
        src: ignition-worker.ign.j2
        dest: "{{ ignition_base }}/worker/{{ item.mac | lower | replace(':', '-') }}.ign"
        mode: '0644'
      loop: "{{ worker_nodes }}"
      vars:
        node: "{{ item }}"

    # =========================================================================
    # PHASE 3: Create Categories (One per Role)
    # =========================================================================

    - name: Create master category
      nvidia.bcm.bcm_category:
        name: "openshift-{{ openshift_version | replace('.', '') }}-{{ cluster_name }}-master"
        state: present
        bootloader: syslinux
        bootloaderprotocol: HTTP
        kernelparameters: >-
          coreos.inst.install_dev=/dev/sda
          coreos.inst.image_url=http://{{ bcm_server }}:8080{{ repo_path }}/rootfs.img
          coreos.live.rootfs_url=http://{{ bcm_server }}:8080{{ repo_path }}/rootfs.img
          console=tty0
        kerneloutputconsole: tty0
        installmode: NEVER
        newnodeinstallmode: NEVER
        notes: "OpenShift {{ openshift_version }} - {{ cluster_name | upper }} - Master Nodes"

    - name: Create worker category
      nvidia.bcm.bcm_category:
        name: "openshift-{{ openshift_version | replace('.', '') }}-{{ cluster_name }}-worker"
        state: present
        bootloader: syslinux
        bootloaderprotocol: HTTP
        kernelparameters: >-
          coreos.inst.install_dev=/dev/sda
          coreos.inst.image_url=http://{{ bcm_server }}:8080{{ repo_path }}/rootfs.img
          coreos.live.rootfs_url=http://{{ bcm_server }}:8080{{ repo_path }}/rootfs.img
          console=tty0
        kerneloutputconsole: tty0
        installmode: NEVER
        newnodeinstallmode: NEVER
        notes: "OpenShift {{ openshift_version }} - {{ cluster_name | upper }} - Worker Nodes"

    # =========================================================================
    # PHASE 4: Register Nodes with MAC-based Ignition URLs
    # =========================================================================

    - name: Register master nodes
      nvidia.bcm.bcm_node:
        name: "{{ item.name }}"
        mac: "{{ item.mac }}"
        ip: "{{ item.ip }}"
        category: "openshift-{{ openshift_version | replace('.', '') }}-{{ cluster_name }}-master"
        state: present
        # Node-specific kernel parameters (override category)
        kernelparameters: >-
          coreos.inst.ignition_url=http://{{ bcm_server }}:8080{{ ignition_base }}/master/{{ item.mac | lower | replace(':', '-') }}.ign
      loop: "{{ master_nodes }}"

    - name: Register worker nodes
      nvidia.bcm.bcm_node:
        name: "{{ item.name }}"
        mac: "{{ item.mac }}"
        ip: "{{ item.ip }}"
        category: "openshift-{{ openshift_version | replace('.', '') }}-{{ cluster_name }}-worker"
        state: present
        # Node-specific kernel parameters (override category)
        kernelparameters: >-
          coreos.inst.ignition_url=http://{{ bcm_server }}:8080{{ ignition_base }}/worker/{{ item.mac | lower | replace(':', '-') }}.ign
      loop: "{{ worker_nodes }}"
```

## Adding Nodes Later (Expansion)

### Step 1: Generate New Ignition File

```bash
# From updated agent-config.yaml or cluster extraction
MAC_NEW="52:54:00:CC:DD:01"
MAC_FILENAME=$(echo $MAC_NEW | tr 'A-Z' 'a-z' | tr ':' '-')

# Generate or copy Ignition
cp worker-template.ign /tftpboot/ignition/openshift-4.16/prod/worker/${MAC_FILENAME}.ign

# Or extract from cluster
oc extract -n openshift-machine-api secret/worker-user-data \
  --keys=userData \
  --to=/tftpboot/ignition/openshift-4.16/prod/worker/${MAC_FILENAME}.ign
```

### Step 2: Register Node (Same Category!)

```bash
cmsh << 'EOF'
device
add genericdevice worker-5
set mac 52:54:00:CC:DD:01
set ip 10.141.160.65
set category openshift-416-prod-worker
set kernelparameters "coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/openshift-4.16/prod/worker/52-54-00-cc-dd-01.ign"
commit
EOF
```

**No new category needed!** Just add the MAC-based Ignition file and register the node.

## Advantages of MAC-based Approach

1. **No Category Proliferation**: Same category for initial + expansion nodes
2. **Clear Node Identity**: Each node has its own Ignition file
3. **Easy Expansion**: Just add MAC-based Ignition and register node
4. **Version Control Friendly**: Track individual node configs
5. **Debugging**: Easy to see which node has which config
6. **Flexibility**: Can customize per-node without category changes
7. **Audit Trail**: File modification dates show when nodes were added

## Category Comparison

### Old Approach (Phase-based)
```
openshift-416-prod-master-init       # 3 nodes
openshift-416-prod-master-expand-q2  # 0 nodes (masters rarely expand)
openshift-416-prod-worker-init       # 5 nodes
openshift-416-prod-worker-expand-q1  # 10 nodes
openshift-416-prod-worker-expand-q2  # 10 nodes
openshift-416-prod-worker-expand-q3  # 10 nodes
```
**Result**: 7 categories, difficult to manage

### New Approach (MAC-based)
```
openshift-416-prod-master            # 3 nodes (any time)
openshift-416-prod-worker            # 35 nodes (all deployments)
openshift-416-prod-infra             # 3 nodes (any time)
```
**Result**: 3 categories, clean and simple

## File Organization Example

```
/tftpboot/ignition/
├── openshift-4.16/
│   ├── prod/
│   │   ├── master/
│   │   │   ├── 52-54-00-aa-bb-01.ign  # master-0
│   │   │   ├── 52-54-00-aa-bb-02.ign  # master-1
│   │   │   └── 52-54-00-aa-bb-03.ign  # master-2
│   │   ├── worker/
│   │   │   ├── 52-54-00-aa-bb-10.ign  # worker-0 (Jan 2025)
│   │   │   ├── 52-54-00-aa-bb-11.ign  # worker-1 (Jan 2025)
│   │   │   ├── 52-54-00-cc-dd-01.ign  # worker-2 (Mar 2025)
│   │   │   ├── 52-54-00-cc-dd-02.ign  # worker-3 (Mar 2025)
│   │   │   └── 52-54-00-ee-ff-01.ign  # worker-4 (Jun 2025)
│   │   └── infra/
│   │       └── 52-54-00-ff-ee-01.ign
│   └── test/
│       └── ...
└── openshift-4.17/
    └── ...
```

Git history shows when each node was added!

## Summary

**Category Naming**: `openshift-<version>-<cluster>-<role>`
- Simple, clear, no phase suffixes needed
- Same category serves all nodes of that role/cluster/version

**Ignition Files**: MAC-based `<mac-with-hyphens>.ign`
- Each node gets unique Ignition
- Organized by version/cluster/role
- Easy to add new nodes without new categories

**Node Registration**: Per-node kernel parameters
- Override category defaults
- Point to MAC-specific Ignition file
- No category changes needed for expansion

This approach is **cleaner, more scalable, and easier to maintain** than phase-based categories!