# BCM PXE Deployment Guide - Unified Strategy

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Category Naming Convention](#category-naming-convention)
4. [File Organization](#file-organization)
5. [RHEL + Slurm Deployment](#rhel--slurm-deployment)
6. [OpenShift Deployment](#openshift-deployment)
7. [Deployment Workflows](#deployment-workflows)
8. [Best Practices](#best-practices)

## Overview

This guide consolidates the PXE boot deployment strategy for NVIDIA Base Command Manager (BCM) supporting:
- **RHEL + Slurm**: Traditional HPC clusters with Kickstart
- **OpenShift**: Container orchestration with Ignition

**Key Principles**:
- Leverage BCM's PXE templating system (minimal manual file editing)
- Use MAC-based configuration files for per-node customization
- Simplified category naming without deployment phases
- Copy files (don't bind mount) for robustness
- Reuse boot files via symlinks

## Architecture

### BCM PXE Boot Flow

```
Node PXE Boot
    ↓
DHCP (IP + boot server)
    ↓
TFTP (bootloader + PXE config)
    ↓
BCM Category PXE Config (auto-generated from template)
    ↓
HTTP Download (kernel + initrd + config)
    ↓
Installation (Kickstart for RHEL / Ignition for OpenShift)
```

### Component Relationships

```
Software Repository (ISO content) → Shared across categories
    ↓
Boot Files (kernel + initrd) → Shared via symlinks
    ↓
Categories (role-based) → BCM templating generates PXE configs
    ↓
Nodes → Per-node kernel parameters → MAC-based config files
```

## Category Naming Convention

### Pattern

**RHEL + Slurm**: `slurm-<cluster>-<role>`
**OpenShift**: `openshift-<version>-<cluster>-<role>`

### Examples

```
# RHEL + Slurm
slurm-hpc01-login
slurm-hpc01-compute
slurm-hpc01-gpu-a100
slurm-hpc01-storage

# OpenShift
openshift-416-prod-master
openshift-416-prod-worker
openshift-416-prod-infra
openshift-416-test-master
openshift-417-prod-worker    # Version upgrade
```

### Rationale

- **Cluster Identification**: First component identifies cluster
- **Role Clarity**: Role clearly stated
- **No Phases**: Avoid `init`/`expand` suffixes - use MAC-based configs instead
- **Version in Name** (OpenShift): Track OS version for upgrades
- **Sortable**: Natural alphabetical grouping

## File Organization

### Directory Structure

```
/tftpboot/
├── repos/                              # Installation repositories (copied from ISOs)
│   ├── rhel-9.6/                       # RHEL repository (shared)
│   ├── rocky-9.5/
│   └── openshift-4.16/                 # OpenShift assets
│       ├── agent.x86_64.iso
│       └── rootfs.img
│
├── images/                             # Boot files (kernel + initrd)
│   ├── installer-rhel-9.6/             # Master RHEL installer
│   │   ├── vmlinuz
│   │   └── initrd
│   ├── installer-openshift-4.16/       # Master OpenShift installer
│   │   ├── vmlinuz
│   │   └── initrd
│   │
│   # Symlinks for categories
│   ├── slurm-hpc01-compute -> installer-rhel-9.6/
│   ├── slurm-hpc01-gpu-a100 -> installer-rhel-9.6/
│   ├── openshift-416-prod-master -> installer-openshift-4.16/
│   └── openshift-416-prod-worker -> installer-openshift-4.16/
│
├── ks/                                 # Kickstart files (RHEL - role-based)
│   ├── slurm-hpc01-compute.cfg
│   ├── slurm-hpc01-gpu-a100.cfg
│   └── slurm-hpc02-compute.cfg
│
├── ignition/                           # Ignition files (OpenShift - MAC-based)
│   └── openshift-4.16/
│       ├── prod/
│       │   ├── master/
│       │   │   ├── 52-54-00-aa-bb-01.ign
│       │   │   └── 52-54-00-aa-bb-02.ign
│       │   └── worker/
│       │       ├── 52-54-00-cc-dd-01.ign  # Initial deployment
│       │       └── 52-54-00-ee-ff-01.ign  # Expansion (same category!)
│       └── test/
│           └── ...
│
└── pxelinux.cfg/                       # PXE configs (BCM auto-generated)
    ├── template                        # Template (DO NOT EDIT generated files)
    ├── category.slurm-hpc01-compute
    ├── category.openshift-416-prod-master
    └── default -> category.default
```

## RHEL + Slurm Deployment

### Characteristics

- **Installation**: Anaconda installer with Kickstart
- **Config Format**: INI-style text files
- **Config Location**: `/tftpboot/ks/<category>.cfg`
- **Per-Category**: Each role has its own kickstart
- **BCM Install Mode**: AUTO/FULL/SYNC

### Workflow

#### 1. Prepare Repository (One-Time)

```bash
# Mount ISO temporarily
mount -o loop /root/rhel-9.6-x86_64-dvd.iso /mnt/rhel-iso

# Copy to permanent location
mkdir -p /tftpboot/repos/rhel-9.6
rsync -av /mnt/rhel-iso/ /tftpboot/repos/rhel-9.6/

# Unmount and remove ISO
umount /mnt/rhel-iso
rm /root/rhel-9.6-x86_64-dvd.iso  # Optional: save space
```

#### 2. Extract Boot Files (One-Time per OS Version)

```bash
# Create installer directory
mkdir -p /tftpboot/images/installer-rhel-9.6

# Copy kernel and initrd
cp /tftpboot/repos/rhel-9.6/images/pxeboot/vmlinuz \
   /tftpboot/images/installer-rhel-9.6/vmlinuz
cp /tftpboot/repos/rhel-9.6/images/pxeboot/initrd.img \
   /tftpboot/images/installer-rhel-9.6/initrd

chmod 644 /tftpboot/images/installer-rhel-9.6/*
```

#### 3. Create Role-Specific Kickstarts

```bash
# Compute nodes kickstart
cat > /tftpboot/ks/slurm-hpc01-compute.cfg << 'EOF'
#version=RHEL9
url --url="http://10.141.255.254:8080/tftpboot/repos/rhel-9.6"
auth --enableshadow --passalgo=sha512
keyboard --vckeymap=us
lang en_US.UTF-8
network --bootproto=dhcp --device=link --onboot=on
rootpw --plaintext changeme123
timezone UTC --utc
ignoredisk --only-use=sda
clearpart --all --initlabel
autopart --type=lvm
bootloader --location=mbr
selinux --enforcing
firewall --enabled --ssh
skipx
reboot

%packages
@^minimal-environment
@development-tools
slurm-slurmd
%end

%post --log=/root/ks-post.log
echo "Compute node configured"
%end
EOF

# GPU nodes kickstart (different packages/config)
cat > /tftpboot/ks/slurm-hpc01-gpu-a100.cfg << 'EOF'
# Similar to above but with GPU-specific packages
%packages
@^minimal-environment
@development-tools
slurm-slurmd
pciutils
kernel-devel
%end

%post --log=/root/ks-post.log
# Install NVIDIA drivers
# Configure GPU settings
%end
EOF

chmod 644 /tftpboot/ks/*.cfg
```

#### 4. Create Symlinks for Categories

```bash
ln -sf /tftpboot/images/installer-rhel-9.6 \
       /tftpboot/images/slurm-hpc01-compute

ln -sf /tftpboot/images/installer-rhel-9.6 \
       /tftpboot/images/slurm-hpc01-gpu-a100
```

#### 5. Configure BCM Categories

```bash
cmsh << 'EOF'
category
add slurm-hpc01-compute
set bootloader syslinux
set bootloaderprotocol HTTP
set kernelparameters "inst.stage2=http://10.141.255.254:8080/tftpboot/repos/rhel-9.6 inst.ks=http://10.141.255.254:8080/tftpboot/ks/slurm-hpc01-compute.cfg console=tty0"
set kerneloutputconsole tty0
set installmode AUTO
set newnodeinstallmode FULL
set notes "RHEL 9.6 - HPC01 Cluster - Compute Nodes"
commit

category
add slurm-hpc01-gpu-a100
set bootloader syslinux
set bootloaderprotocol HTTP
set kernelparameters "inst.stage2=http://10.141.255.254:8080/tftpboot/repos/rhel-9.6 inst.ks=http://10.141.255.254:8080/tftpboot/ks/slurm-hpc01-gpu-a100.cfg console=tty0"
set kerneloutputconsole tty0
set installmode AUTO
set newnodeinstallmode FULL
set notes "RHEL 9.6 - HPC01 Cluster - GPU Nodes (A100)"
commit
EOF
```

BCM automatically generates `/tftpboot/pxelinux.cfg/category.slurm-hpc01-compute`

#### 6. Register Nodes

```bash
cmsh << 'EOF'
device
add genericdevice compute-01
set mac 52:54:00:AA:01:01
set ip 10.141.100.1
set category slurm-hpc01-compute
commit

device
add genericdevice gpu-01
set mac 52:54:00:BB:01:01
set ip 10.141.101.1
set category slurm-hpc01-gpu-a100
commit
EOF
```

## OpenShift Deployment

### Characteristics

- **Installation**: CoreOS with Ignition
- **Config Format**: JSON
- **Config Location**: `/tftpboot/ignition/<version>/<cluster>/<role>/<mac>.ign`
- **Per-Node**: Each node has MAC-based Ignition file
- **BCM Install Mode**: NEVER (CoreOS handles installation)

### Workflow

#### 1. Generate Agent ISO (OpenShift Install)

```bash
# Create installation configs
mkdir ~/openshift-install && cd ~/openshift-install

cat > install-config.yaml << 'EOF'
apiVersion: v1
baseDomain: example.com
metadata:
  name: ocp-prod
networking:
  networkType: OVNKubernetes
  clusterNetwork:
  - cidr: 10.128.0.0/14
    hostPrefix: 23
  serviceNetwork:
  - 172.30.0.0/16
compute:
- name: worker
  replicas: 2
controlPlane:
  name: master
  replicas: 3
platform:
  baremetal:
    apiVIPs: [10.141.160.10]
    ingressVIPs: [10.141.160.11]
pullSecret: '...'
sshKey: 'ssh-rsa ...'
EOF

cat > agent-config.yaml << 'EOF'
apiVersion: v1alpha1
kind: AgentConfig
metadata:
  name: ocp-prod
rendezvousIP: 10.141.160.50
hosts:
- hostname: master-0
  role: master
  interfaces:
  - name: eno1
    macAddress: 52:54:00:AA:BB:01
  networkConfig:
    interfaces:
    - name: eno1
      type: ethernet
      state: up
      ipv4:
        enabled: true
        address:
        - ip: 10.141.160.50
          prefix-length: 16
# ... more hosts
EOF

# Generate agent ISO
openshift-install agent create image
```

#### 2. Extract Boot Files and Ignition

```bash
# Copy ISO to repository
mkdir -p /tftpboot/repos/openshift-4.16
cp agent.x86_64.iso /tftpboot/repos/openshift-4.16/

# Mount ISO
mount -o loop /tftpboot/repos/openshift-4.16/agent.x86_64.iso /mnt/agent-iso

# Extract boot files
mkdir -p /tftpboot/images/installer-openshift-4.16
cp /mnt/agent-iso/images/pxeboot/vmlinuz \
   /tftpboot/images/installer-openshift-4.16/vmlinuz
cp /mnt/agent-iso/images/pxeboot/initrd.img \
   /tftpboot/images/installer-openshift-4.16/initrd

# Extract rootfs
cp /mnt/agent-iso/images/pxeboot/rootfs.img \
   /tftpboot/repos/openshift-4.16/rootfs.img

# Unmount
umount /mnt/agent-iso

chmod 644 /tftpboot/images/installer-openshift-4.16/*
chmod 644 /tftpboot/repos/openshift-4.16/rootfs.img
```

#### 3. Generate MAC-based Ignition Files

```bash
# Create directory structure
mkdir -p /tftpboot/ignition/openshift-4.16/prod/{master,worker,infra}

# Generate Ignition for each node (from agent-config.yaml or cluster)
# Master-0 example
MAC_FILE="52-54-00-aa-bb-01"
cat > /tftpboot/ignition/openshift-4.16/prod/master/${MAC_FILE}.ign << 'EOF'
{
  "ignition": {"version": "3.2.0"},
  "storage": {
    "files": [{
      "path": "/etc/hostname",
      "mode": 420,
      "contents": {"source": "data:,master-0.ocp-prod.example.com"}
    }]
  }
}
EOF

# For expansion nodes (extract from running cluster)
oc extract -n openshift-machine-api secret/worker-user-data \
  --keys=userData \
  --to=/tftpboot/ignition/openshift-4.16/prod/worker/52-54-00-cc-dd-01.ign

chmod 644 /tftpboot/ignition/openshift-4.16/prod/*/*.ign
```

#### 4. Create Symlinks for Categories

```bash
ln -sf /tftpboot/images/installer-openshift-4.16 \
       /tftpboot/images/openshift-416-prod-master

ln -sf /tftpboot/images/installer-openshift-4.16 \
       /tftpboot/images/openshift-416-prod-worker
```

#### 5. Configure BCM Categories

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

#### 6. Register Nodes with MAC-based Ignition URLs

```bash
# Master-0
cmsh << 'EOF'
device
add genericdevice master-0
set mac 52:54:00:AA:BB:01
set ip 10.141.160.50
set category openshift-416-prod-master
set kernelparameters "coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/openshift-4.16/prod/master/52-54-00-aa-bb-01.ign"
commit
EOF

# Worker-0 (initial)
cmsh << 'EOF'
device
add genericdevice worker-0
set mac 52:54:00:CC:DD:01
set ip 10.141.160.60
set category openshift-416-prod-worker
set kernelparameters "coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/openshift-4.16/prod/worker/52-54-00-cc-dd-01.ign"
commit
EOF

# Worker-5 (expansion - months later, SAME category!)
cmsh << 'EOF'
device
add genericdevice worker-5
set mac 52:54:00:EE:FF:01
set ip 10.141.160.65
set category openshift-416-prod-worker
set kernelparameters "coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/openshift-4.16/prod/worker/52-54-00-ee-ff-01.ign"
commit
EOF
```

## Deployment Workflows

### RHEL + Slurm: Adding Nodes

```bash
# 1. Node already registered in BCM
# 2. Already has correct category assigned
# 3. Power on node → PXE boots → Kickstart installs → Joins Slurm

# For new role (new category needed):
# 1. Create new kickstart: /tftpboot/ks/slurm-hpc01-<new-role>.cfg
# 2. Create symlink: slurm-hpc01-<new-role> -> installer-rhel-9.6/
# 3. Create category with new kickstart URL
# 4. Register nodes with new category
```

### OpenShift: Adding Nodes

```bash
# 1. Generate MAC-based Ignition file
MAC_NEW="52:54:00:FF:FF:01"
MAC_FILE=$(echo $MAC_NEW | tr 'A-Z' 'a-z' | tr ':' '-')

# Option A: From new agent ISO
openshift-install agent create image  # with new node in agent-config.yaml
# Extract Ignition from ISO

# Option B: From running cluster (workers only)
oc extract -n openshift-machine-api secret/worker-user-data \
  --keys=userData \
  --to=/tftpboot/ignition/openshift-4.16/prod/worker/${MAC_FILE}.ign

# 2. Register node (SAME category as existing workers!)
cmsh << EOF
device add worker-10
set mac $MAC_NEW
set ip 10.141.160.70
set category openshift-416-prod-worker
set kernelparameters "coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/openshift-4.16/prod/worker/${MAC_FILE}.ign"
commit
EOF

# 3. Power on node
```

## Best Practices

### 1. File Management

- **Copy, don't bind mount**: Copy ISO contents to permanent locations
- **Symlinks for reuse**: Multiple categories share same boot files via symlinks
- **MAC-based configs**: Use MAC addresses in filenames for per-node customization
- **Version control**: Track Ignition/Kickstart files in git

### 2. Category Organization

- **Simplified naming**: No phase suffixes (init/expand)
- **Role-based**: One category per cluster/role combination
- **Metadata in notes**: Store cluster info in category notes field
- **Minimal categories**: Reuse categories for expansion via per-node configs

### 3. BCM Integration

- **Use templating**: Let BCM generate PXE configs from template
- **Per-node parameters**: Override category defaults at node level
- **HTTP preferred**: Use HTTP for boot file transfer (faster than TFTP)
- **Install modes**: AUTO/FULL for RHEL, NEVER for CoreOS

### 4. Deployment Strategy

- **One-time setup**: Repository and boot file extraction per OS version
- **Role-specific configs**: Different kickstarts/ignitions per role
- **Expansion-friendly**: Add nodes without creating new categories
- **Audit trail**: File timestamps and git history track deployments

### 5. Security

- **Secrets management**: Don't commit pull secrets or passwords to git
- **File permissions**: 0644 for boot files and configs
- **Network isolation**: Use dedicated management network for PXE
- **Encrypted passwords**: Use encrypted passwords in kickstart

## Comparison: RHEL vs OpenShift

| Aspect | RHEL + Slurm | OpenShift |
|--------|--------------|-----------|
| **Installer** | Anaconda | CoreOS Agent |
| **Config Format** | Kickstart (INI) | Ignition (JSON) |
| **Config Scope** | Per-category | Per-node (MAC-based) |
| **Config Location** | `/tftpboot/ks/` | `/tftpboot/ignition/` |
| **Boot Files** | kernel + initrd | kernel + initrd + rootfs |
| **Install Mode** | AUTO/FULL/SYNC | NEVER (self-installs) |
| **Expansion** | Same kickstart | New MAC-based Ignition |
| **Kernel Param** | `inst.ks=http://...` | `coreos.inst.ignition_url=http://...` |
| **Category Reuse** | Yes (shared kickstart) | Yes (per-node Ignition URLs) |

## Summary

This unified strategy provides:

- **Consistent approach** across RHEL and OpenShift deployments
- **BCM native** integration using templating and categories
- **Minimal manual files** - only ISO extraction and config generation
- **Scalable** - easy to add nodes without category proliferation
- **Maintainable** - clear structure, version controlled configs
- **Flexible** - per-node customization via MAC-based configs

The key insight: **Use BCM categories for roles, not deployment phases. Use MAC-based config files for per-node customization.**
