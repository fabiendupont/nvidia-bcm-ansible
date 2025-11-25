# BCM Category Naming Strategy for Multi-Cluster Environments

## The Challenge

When managing multiple clusters with BCM:
- RHEL + Slurm clusters (HPC workloads)
- OpenShift clusters (container workloads)
- Different lifecycle phases (initial deployment vs expansion)
- Multiple distinct clusters of the same type

**Questions**:
1. How to identify which cluster a category belongs to?
2. How to handle OpenShift node additions (new ISO vs new Ignition)?
3. How to organize categories semantically?

## Category Naming Convention

### Recommended Naming Pattern

```
<cluster-name>-<role>[-<phase>]
```

**Components**:
- `cluster-name`: Unique cluster identifier
- `role`: Node role/purpose
- `phase`: Optional lifecycle phase (initial/expand/upgrade)

### Examples

#### RHEL + Slurm Clusters
```
slurm-prod-login         # Production Slurm login nodes
slurm-prod-compute       # Production Slurm compute nodes
slurm-prod-gpu           # Production Slurm GPU nodes
slurm-test-compute       # Test Slurm compute nodes
slurm-dev-all            # Development Slurm all-in-one
```

#### OpenShift Clusters
```
ocp-prod-master-init     # Initial master nodes
ocp-prod-master-expand   # Additional master nodes
ocp-prod-worker-init     # Initial worker nodes
ocp-prod-worker-expand   # Additional worker nodes
ocp-test-master-init     # Test cluster masters
ocp-test-worker-init     # Test cluster workers
```

#### Mixed Environment
```
slurm-ml-gpu             # ML workload GPU nodes (RHEL + Slurm)
slurm-ml-storage         # ML workload storage nodes
ocp-ml-worker-gpu        # ML workload OpenShift GPU workers
ocp-ml-worker-cpu        # ML workload OpenShift CPU workers
```

### Why This Pattern?

1. **Cluster Identification**: First component clearly identifies the cluster
2. **Role Clarity**: Second component describes node purpose
3. **Lifecycle Support**: Optional phase handles expansion/upgrades
4. **Sortable**: Alphabetical sorting groups by cluster
5. **Searchable**: Easy to filter by cluster or role
6. **No Ambiguity**: Clear ownership and purpose

## OpenShift Agent-based Installer: Initial vs Additional Nodes

### How ABI Works

**Initial Cluster Installation**:
```bash
# Create install-config.yaml and agent-config.yaml
# with ALL nodes (masters + initial workers)
openshift-install agent create image

# Generates: agent.x86_64.iso
# Contains: kernel + initrd + rootfs + embedded ignition for ALL listed nodes
```

**Adding Nodes Later** (Two Approaches):

#### Approach 1: Generate New ISO (Recommended for New Node Types)

When adding nodes with different roles or configurations:

```bash
# Update agent-config.yaml with NEW nodes
# Keep install-config.yaml pointing to existing cluster

openshift-install agent create image

# Generates: NEW agent.x86_64.iso
# Contains: kernel + initrd + rootfs + ignition for NEW nodes
```

**What Changes**:
- ✅ New ISO generated
- ✅ New kernel/initrd (might be updated version)
- ✅ New rootfs
- ✅ New embedded Ignition configs for new nodes
- ⚠️ Different from initial ISO

#### Approach 2: Use Cluster's CA and Manual Ignition (Advanced)

For homogeneous worker additions:

```bash
# Extract cluster CA and generate worker ignition
oc extract -n openshift-machine-api secret/worker-user-data --keys=userData --to=- > worker.ign

# Use SAME kernel/initrd/rootfs as initial install
# Only Ignition config differs
```

**What's Reused**:
- ✅ Same kernel/initrd from initial ISO
- ✅ Same rootfs from initial ISO
- ✅ Only worker.ign is new

### BCM Category Strategy for OpenShift

#### Strategy 1: Separate Categories per Phase (Recommended)

**Advantages**:
- Clear separation of initial vs expansion deployments
- Different Ignition configs per phase
- Can use different kernel/initrd versions
- Easy to track which nodes are part of which deployment wave

**File Organization**:
```
/tftpboot/
├── repos/
│   ├── openshift-4.16-initial/       # Initial cluster ISO assets
│   │   ├── agent.x86_64.iso
│   │   └── rootfs.img
│   └── openshift-4.16-expand-2025-01/ # Expansion ISO (different month/version)
│       ├── agent.x86_64.iso
│       └── rootfs.img
│
├── images/
│   ├── installer-ocp-prod-initial/    # Initial deployment boot files
│   │   ├── vmlinuz
│   │   └── initrd
│   ├── installer-ocp-prod-expand-2025-01/  # Expansion boot files
│   │   ├── vmlinuz
│   │   └── initrd
│   ├── ocp-prod-master-init -> installer-ocp-prod-initial/
│   ├── ocp-prod-worker-init -> installer-ocp-prod-initial/
│   ├── ocp-prod-worker-expand -> installer-ocp-prod-expand-2025-01/
│   └── ocp-prod-infra-expand -> installer-ocp-prod-expand-2025-01/
│
└── ignition/
    ├── ocp-prod/                      # Cluster-specific directory
    │   ├── initial/
    │   │   ├── master-0.ign
    │   │   ├── master-1.ign
    │   │   ├── master-2.ign
    │   │   └── worker-0.ign
    │   └── expand-2025-01/
    │       ├── worker-3.ign
    │       ├── worker-4.ign
    │       └── infra-0.ign
    └── ocp-test/
        └── ...
```

**BCM Categories**:
```bash
# Initial deployment categories
cmsh << 'EOF'
category add ocp-prod-master-init
set bootloader syslinux
set bootloaderprotocol HTTP
set kernelparameters "coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/ocp-prod/initial/master.ign coreos.live.rootfs_url=http://10.141.255.254:8080/tftpboot/repos/openshift-4.16-initial/rootfs.img"
set notes "OpenShift Production - Initial Master Nodes - Cluster: ocp-prod"
commit

category add ocp-prod-worker-init
set bootloader syslinux
set bootloaderprotocol HTTP
set kernelparameters "coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/ocp-prod/initial/worker.ign coreos.live.rootfs_url=http://10.141.255.254:8080/tftpboot/repos/openshift-4.16-initial/rootfs.img"
set notes "OpenShift Production - Initial Worker Nodes - Cluster: ocp-prod"
commit
EOF

# Expansion categories (months later)
cmsh << 'EOF'
category add ocp-prod-worker-expand
set bootloader syslinux
set bootloaderprotocol HTTP
set kernelparameters "coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/ocp-prod/expand-2025-01/worker.ign coreos.live.rootfs_url=http://10.141.255.254:8080/tftpboot/repos/openshift-4.16-expand-2025-01/rootfs.img"
set notes "OpenShift Production - Expansion Workers Jan 2025 - Cluster: ocp-prod"
commit
EOF
```

#### Strategy 2: Shared Boot Files, Different Ignition (Space Efficient)

If kernel/initrd/rootfs versions match:

**File Organization**:
```
/tftpboot/
├── repos/
│   └── openshift-4.16/               # Shared repository
│       ├── agent.x86_64.iso          # Latest ISO
│       └── rootfs.img
│
├── images/
│   ├── installer-ocp-prod/           # Shared boot files
│   │   ├── vmlinuz
│   │   └── initrd
│   ├── ocp-prod-master -> installer-ocp-prod/
│   └── ocp-prod-worker -> installer-ocp-prod/
│
└── ignition/
    └── ocp-prod/
        ├── master-0.ign              # Generated with initial ISO
        ├── worker-0.ign
        ├── worker-3.ign              # Generated with expansion ISO
        └── worker-4.ign
```

**BCM Categories** (Single Set):
```bash
cmsh << 'EOF'
category add ocp-prod-master
category add ocp-prod-worker
# Same kernel parameters, different ignition URLs per node
EOF
```

**Challenge**: Need to dynamically point nodes to correct Ignition file.

#### Strategy 3: Hybrid - Cluster Metadata in Notes Field

Use BCM's `notes` field to store cluster metadata:

```bash
cmsh << 'EOF'
category add ocp-prod-worker
set notes "cluster=ocp-prod,role=worker,phase=initial,version=4.16.0,deployed=2025-01-15"
commit
EOF
```

**Query by Cluster**:
```bash
# List all categories for ocp-prod cluster
cmsh -c 'category; list' | grep ocp-prod

# Via pythoncm
import sys
sys.path.insert(0, '/cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages')
from pythoncm.cluster import Cluster

c = Cluster()
categories = c.get_by_type('Category')
for cat in categories:
    if 'ocp-prod' in cat.name or (cat.notes and 'ocp-prod' in cat.notes):
        print(f"{cat.name}: {cat.notes}")
```

## Recommended Approach

### For Production Environments

**Use Strategy 1 (Separate Categories per Phase)**:

1. **Clear Lifecycle Tracking**: Know which nodes are part of which deployment
2. **Version Control**: Different OpenShift versions between initial and expansion
3. **Rollback Safety**: Keep initial configurations immutable
4. **Audit Trail**: Category creation dates match deployment dates

### Category Naming Examples

```
# RHEL + Slurm
slurm-hpc01-login
slurm-hpc01-compute-cpu
slurm-hpc01-compute-gpu-a100
slurm-hpc01-storage
slurm-hpc02-compute-cpu      # Different cluster

# OpenShift
ocp-prod-master-init         # Initial 3 masters
ocp-prod-worker-init         # Initial 2 workers
ocp-prod-worker-expand-q1    # Q1 expansion
ocp-prod-worker-expand-q2    # Q2 expansion
ocp-prod-infra-init          # Infrastructure nodes

# GPU Cloud (Mixed)
gpu-cloud-slurm-a100         # RHEL nodes with A100
gpu-cloud-slurm-h100         # RHEL nodes with H100
gpu-cloud-ocp-worker-a100    # OpenShift workers with A100
```

## OpenShift ABI: What's Actually Needed for Expansion

### Initial Cluster Deployment

**Generated by ABI**:
```
agent.x86_64.iso contains:
├── images/pxeboot/
│   ├── vmlinuz               # CoreOS kernel
│   ├── initrd.img            # CoreOS initramfs
│   └── rootfs.img            # CoreOS root filesystem
└── config.ign                # Embedded ignition for all listed nodes
```

**Extract for PXE**:
- ✅ vmlinuz → `/tftpboot/images/installer-ocp-prod-initial/vmlinuz`
- ✅ initrd → `/tftpboot/images/installer-ocp-prod-initial/initrd`
- ✅ rootfs.img → `/tftpboot/repos/openshift-4.16-initial/rootfs.img`
- ✅ Per-node ignition → `/tftpboot/ignition/ocp-prod/initial/*.ign`

### Adding Nodes (Months Later)

**Option A: Generate New ISO** (Safest):
```bash
# Update agent-config.yaml with NEW nodes only
openshift-install agent create image --dir ./expansion-2025-01
```

**New ISO Contains**:
- Potentially updated kernel/initrd (if CoreOS version changed)
- New rootfs.img
- New ignition configs for expansion nodes
- Reference to existing cluster (via API VIP)

**Extract for PXE** (New Category):
- ✅ vmlinuz → `/tftpboot/images/installer-ocp-prod-expand-2025-01/vmlinuz`
- ✅ initrd → `/tftpboot/images/installer-ocp-prod-expand-2025-01/initrd`
- ✅ rootfs.img → `/tftpboot/repos/openshift-4.16-expand-2025-01/rootfs.img`
- ✅ Ignition → `/tftpboot/ignition/ocp-prod/expand-2025-01/*.ign`

**Option B: Reuse Boot Files, New Ignition** (If versions match):

```bash
# Check CoreOS version matches
# If yes, reuse kernel/initrd/rootfs from initial deployment
# Only generate new worker ignition from cluster

oc extract -n openshift-machine-api secret/worker-user-data --keys=userData --to=- > worker-new.ign
```

**PXE Setup** (Same Category):
- ✅ Reuse vmlinuz/initrd from initial
- ✅ Reuse rootfs.img from initial
- ✅ New ignition → `/tftpboot/ignition/ocp-prod/worker-new.ign`

**When to Use Each**:
- **Option A**: Different CoreOS versions, major cluster changes, different node types
- **Option B**: Same CoreOS version, homogeneous worker expansion, minor additions

## Complete Example: Multi-Cluster Setup

### File Structure

```
/tftpboot/
├── repos/
│   ├── rhel-9.6/                          # Shared RHEL repo
│   ├── openshift-4.16-ocp-prod-initial/   # OCP prod initial
│   ├── openshift-4.16-ocp-prod-expand-q2/ # OCP prod Q2 expansion
│   └── openshift-4.16-ocp-test-initial/   # OCP test initial
│
├── images/
│   ├── installer-rhel-9.6/
│   ├── installer-ocp-prod-initial/
│   ├── installer-ocp-prod-expand-q2/
│   ├── installer-ocp-test-initial/
│   │
│   ├── slurm-hpc01-compute -> installer-rhel-9.6/
│   ├── slurm-hpc01-gpu -> installer-rhel-9.6/
│   ├── ocp-prod-master-init -> installer-ocp-prod-initial/
│   ├── ocp-prod-worker-init -> installer-ocp-prod-initial/
│   ├── ocp-prod-worker-expand-q2 -> installer-ocp-prod-expand-q2/
│   ├── ocp-test-master-init -> installer-ocp-test-initial/
│   └── ocp-test-worker-init -> installer-ocp-test-initial/
│
├── ks/
│   ├── slurm-hpc01-compute.cfg
│   └── slurm-hpc01-gpu.cfg
│
└── ignition/
    ├── ocp-prod/
    │   ├── initial/
    │   │   ├── master-0.ign
    │   │   └── worker-0.ign
    │   └── expand-q2/
    │       ├── worker-5.ign
    │       └── worker-6.ign
    └── ocp-test/
        └── initial/
            └── ...
```

### Category Inventory

```yaml
categories:
  # RHEL + Slurm Cluster
  - name: slurm-hpc01-compute
    cluster: hpc01
    type: slurm
    role: compute
    os: rhel-9.6

  - name: slurm-hpc01-gpu
    cluster: hpc01
    type: slurm
    role: gpu
    os: rhel-9.6

  # OpenShift Production Cluster
  - name: ocp-prod-master-init
    cluster: ocp-prod
    type: openshift
    role: master
    phase: initial
    version: 4.16.0

  - name: ocp-prod-worker-init
    cluster: ocp-prod
    type: openshift
    role: worker
    phase: initial
    version: 4.16.0

  - name: ocp-prod-worker-expand-q2
    cluster: ocp-prod
    type: openshift
    role: worker
    phase: expand-q2
    version: 4.16.5

  # OpenShift Test Cluster
  - name: ocp-test-master-init
    cluster: ocp-test
    type: openshift
    role: master
    phase: initial
    version: 4.16.0
```

## Ansible Variable Structure

```yaml
clusters:
  - name: hpc01
    type: slurm
    os: rhel
    os_version: "9.6"
    categories:
      - name: slurm-hpc01-compute
        role: compute
        kickstart: slurm-hpc01-compute.cfg
      - name: slurm-hpc01-gpu
        role: gpu
        kickstart: slurm-hpc01-gpu.cfg

  - name: ocp-prod
    type: openshift
    version: "4.16.0"
    phases:
      - name: initial
        date: "2025-01-15"
        categories:
          - name: ocp-prod-master-init
            role: master
            count: 3
          - name: ocp-prod-worker-init
            role: worker
            count: 2
      - name: expand-q2
        date: "2025-04-01"
        version: "4.16.5"  # Potentially updated
        categories:
          - name: ocp-prod-worker-expand-q2
            role: worker
            count: 5
```

## Summary

### Questions Answered

1. **Category Naming Semantic**: Use `<cluster>-<role>[-<phase>]` pattern
2. **New Node ISO**:
   - Full ISO if CoreOS version changed → New category
   - Same boot files if version matches → Can reuse category with new ignition
3. **Dedicated Categories**:
   - **YES** for different phases with different OS versions
   - **OPTIONAL** for homogeneous expansions with same version

### Best Practice

- **Use separate categories per deployment phase**
- **Store cluster metadata in category names and notes**
- **Keep phase-specific boot files and ignition separate**
- **Enable easy rollback and version tracking**
