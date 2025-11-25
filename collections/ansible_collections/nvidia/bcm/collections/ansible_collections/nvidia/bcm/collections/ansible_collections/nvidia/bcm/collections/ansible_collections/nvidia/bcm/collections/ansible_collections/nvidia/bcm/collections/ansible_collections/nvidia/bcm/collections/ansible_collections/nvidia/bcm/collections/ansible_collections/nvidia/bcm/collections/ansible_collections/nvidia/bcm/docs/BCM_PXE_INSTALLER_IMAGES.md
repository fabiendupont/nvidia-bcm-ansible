# BCM PXE Boot - Installer Images vs Software Images

## Overview

This guide explains how to set up PXE boot for **installer images** (non-BCM managed OS installations) versus **software images** (BCM-managed nodes). Understanding this distinction is critical for reliable PXE deployments.

## The Two Approaches

### Approach 1: BCM Software Images (Stateful Image Sync)

**Use Case**: BCM-managed cluster nodes that sync to a golden master image

**Characteristics**:
- Full OS image stored in `/cm/images/<image-name>/`
- BCM manages the entire filesystem
- Nodes boot from local disk after initial "burn" (installation)
- Updates propagate via image sync (SYNC install mode)
- Best for: Traditional HPC clusters with uniform node configuration

**Example**: `default-image`, `slurm-rhel-9.6`

**Workflow**:
```
1. Create BCM software image in /cm/images/
2. Configure category to use software image
3. Node PXE boots → BCM initrd → Install from software image
4. Subsequent boots: Local disk (with periodic syncs)
```

### Approach 2: Installer Images (Stateless PXE Boot)

**Use Case**: External OS installations not managed by BCM's image sync

**Characteristics**:
- Boot files only in `/tftpboot/images/installer-<name>/`
- NO software image in `/cm/images/`
- Each boot can be from network (stateless) or local disk after install
- Configuration via Kickstart (RHEL) or Ignition (CoreOS/OpenShift)
- Best for: Kickstart installations, OpenShift, external OS deployments

**Example**: `installer-rhel-9.6`, `installer-openshift-4.16`

**Workflow**:
```
1. Extract boot files to /tftpboot/images/installer-*/
2. Create Kickstart/Ignition configuration
3. Configure category WITHOUT software image reference
4. Node PXE boots → Installer initrd → External installation
5. Subsequent boots: Typically local disk (or PXE for stateless)
```

## Key Differences

| Aspect | BCM Software Image | Installer Image |
|--------|-------------------|-----------------|
| **Location** | `/cm/images/<name>/` | `/tftpboot/images/installer-<name>/` |
| **Size** | Full OS (~10-50GB) | Boot files only (~150MB) |
| **Management** | BCM-managed | External (Kickstart/Ignition) |
| **Install Mode** | AUTO/FULL/SYNC | NEVER (external installer) |
| **Updates** | Image sync | Standard package management |
| **Use Cases** | HPC clusters, BCM-managed | Kickstart, OpenShift, custom OS |
| **cmsh softwareimage** | YES (visible) | NO (not a software image) |

## When to Use Each Approach

### Use BCM Software Images When:
- ✅ You want BCM to manage the full OS lifecycle
- ✅ Nodes should be identical (golden master)
- ✅ You need rapid provisioning via image sync
- ✅ Traditional HPC cluster with Slurm
- ✅ Uniform node configuration

### Use Installer Images When:
- ✅ Installing via Kickstart with custom partitioning
- ✅ OpenShift/CoreOS with Ignition
- ✅ OS managed outside of BCM (yum/dnf updates)
- ✅ Per-node customization (MAC-based Ignition)
- ✅ Stateless boot scenarios
- ✅ You don't want BCM controlling the OS filesystem

## Setting Up Installer Images (The Right Way)

### Step 1: Extract Boot Files from ISO

```bash
# Mount the OS ISO temporarily
mkdir -p /mnt/rhel96-iso
mount -o loop /root/rhel-9.6-x86_64-dvd.iso /mnt/rhel96-iso

# Create installer directory (NOT in /cm/images/)
mkdir -p /tftpboot/images/installer-rhel-9.6

# Extract boot files
cp /mnt/rhel96-iso/images/pxeboot/vmlinuz \
   /tftpboot/images/installer-rhel-9.6/vmlinuz
cp /mnt/rhel96-iso/images/pxeboot/initrd.img \
   /tftpboot/images/installer-rhel-9.6/initrd

# Set permissions
chmod 644 /tftpboot/images/installer-rhel-9.6/*

# Unmount ISO
umount /mnt/rhel96-iso
```

**Important**:
- Use `/tftpboot/images/installer-*` prefix to distinguish from software images
- Do NOT create this in `/cm/images/` (that's for BCM software images)
- Do NOT register this as a BCM software image via cmsh

### Step 2: Copy Installation Repository

```bash
# Create repository directory
mkdir -p /tftpboot/repos/rhel-9.6

# Mount ISO again (if unmounted)
mount -o loop /root/rhel-9.6-x86_64-dvd.iso /mnt/rhel96-iso

# Copy full repository (can take 5-10 minutes for DVD)
rsync -av --progress /mnt/rhel96-iso/ /tftpboot/repos/rhel-9.6/

# Unmount and optionally remove ISO
umount /mnt/rhel96-iso
# rm /root/rhel-9.6-x86_64-dvd.iso  # Free up space

# Verify HTTP access
curl -I http://10.141.255.254:8080/tftpboot/repos/rhel-9.6/.treeinfo
```

### Step 3: Create Kickstart Configuration

```bash
# Create kickstart directory
mkdir -p /tftpboot/ks

# Create kickstart file
cat > /tftpboot/ks/rhel96-compute.cfg << 'EOF'
#version=RHEL9

# Installation source
url --url="http://10.141.255.254:8080/tftpboot/repos/rhel-9.6"

# System configuration
auth --enableshadow --passalgo=sha512
keyboard --vckeymap=us
lang en_US.UTF-8
timezone UTC --utc
rootpw --plaintext changeme123

# Network configuration
network --bootproto=dhcp --device=link --onboot=on

# Disk partitioning
ignoredisk --only-use=sda
clearpart --all --initlabel
autopart --type=lvm

# Bootloader
bootloader --location=mbr --boot-drive=sda

# Security
selinux --enforcing
firewall --enabled --ssh

# Installation behavior
skipx
reboot

# Packages
%packages
@^minimal-environment
@development-tools
%end

%post --log=/root/ks-post.log
echo "Installation completed at $(date)" > /root/install-info.txt
%end
EOF

chmod 644 /tftpboot/ks/rhel96-compute.cfg

# Verify HTTP access
curl http://10.141.255.254:8080/tftpboot/ks/rhel96-compute.cfg
```

### Step 4: Configure BCM Category (Without Software Image)

This is the **critical step** where we configure the category to use installer images:

```bash
cmsh << 'EOF'
category
add rhel96-compute

# Boot loader configuration
set bootloader syslinux
set bootloaderprotocol HTTP

# Kernel parameters for Kickstart installation
# Point to installer boot files (will resolve to installer-rhel-9.6 via symlink)
set kernelparameters "inst.stage2=http://10.141.255.254:8080/tftpboot/repos/rhel-9.6 inst.ks=http://10.141.255.254:8080/tftpboot/ks/rhel96-compute.cfg console=tty0"

set kerneloutputconsole tty0

# IMPORTANT: Install mode NEVER (external installer handles it)
set installmode NEVER
set newnodeinstallmode NEVER

# Optional: Notes for documentation
set notes "RHEL 9.6 Compute Nodes - Kickstart Installation"

commit
EOF
```

**Critical Parameters**:
- `installmode NEVER` - BCM won't manage the installation
- `newnodeinstallmode NEVER` - New nodes use external installer
- `inst.stage2=...` - Anaconda installer location
- `inst.ks=...` - Kickstart file URL

### Step 5: Create Symlink for Category

BCM expects boot files at `/tftpboot/images/<category-name>/`. Create a symlink:

```bash
# Create symlink from category name to installer directory
ln -sf /tftpboot/images/installer-rhel-9.6 \
       /tftpboot/images/rhel96-compute

# Verify
ls -la /tftpboot/images/rhel96-compute/
# Should show: vmlinuz, initrd pointing to installer-rhel-9.6
```

**Why This Works**:
- BCM generates PXE config referencing `images/rhel96-compute/vmlinuz`
- Symlink redirects to `installer-rhel-9.6/vmlinuz`
- Multiple categories can share the same installer via different symlinks

### Step 6: Verify PXE Configuration

```bash
# Check generated PXE config
cat /tftpboot/pxelinux.cfg/category.rhel96-compute
```

Expected output:
```
LABEL linux
  KERNEL images/rhel96-compute/vmlinuz
  IPAPPEND 3
  APPEND initrd=images/rhel96-compute/initrd inst.stage2=http://10.141.255.254:8080/tftpboot/repos/rhel-9.6 inst.ks=http://10.141.255.254:8080/tftpboot/ks/rhel96-compute.cfg console=tty0
  MENU LABEL ^AUTO       - Normal node boot
  MENU DEFAULT
```

**Key Points**:
- Boot files come from installer image (via symlink)
- Kernel parameters include Kickstart URL
- No BCM install modes (FULL/SYNC) in APPEND line

## Reusing Installer Images for Multiple Categories

One installer image can serve multiple categories with different kickstarts:

```bash
# Category 1: Compute nodes
ln -sf /tftpboot/images/installer-rhel-9.6 \
       /tftpboot/images/rhel96-compute

cat > /tftpboot/ks/rhel96-compute.cfg << 'EOF'
# Compute-specific kickstart
%packages
@development-tools
%end
EOF

cmsh << 'EOF'
category add rhel96-compute
set bootloader syslinux
set bootloaderprotocol HTTP
set kernelparameters "inst.stage2=http://10.141.255.254:8080/tftpboot/repos/rhel-9.6 inst.ks=http://10.141.255.254:8080/tftpboot/ks/rhel96-compute.cfg"
set installmode NEVER
commit
EOF

# Category 2: GPU nodes (same installer, different kickstart)
ln -sf /tftpboot/images/installer-rhel-9.6 \
       /tftpboot/images/rhel96-gpu

cat > /tftpboot/ks/rhel96-gpu.cfg << 'EOF'
# GPU-specific kickstart
%packages
@development-tools
pciutils
kernel-devel
%end

%post
# Install NVIDIA drivers
%end
EOF

cmsh << 'EOF'
category add rhel96-gpu
set bootloader syslinux
set bootloaderprotocol HTTP
set kernelparameters "inst.stage2=http://10.141.255.254:8080/tftpboot/repos/rhel-9.6 inst.ks=http://10.141.255.254:8080/tftpboot/ks/rhel96-gpu.cfg"
set installmode NEVER
commit
EOF
```

**Result**:
- One installer image (`installer-rhel-9.6`)
- Two categories (`rhel96-compute`, `rhel96-gpu`)
- Two kickstarts (different configurations)
- Two symlinks (for BCM category resolution)

## OpenShift Example (Installer Image with Ignition)

For OpenShift/CoreOS with Ignition:

```bash
# Extract boot files from agent ISO
mkdir -p /mnt/agent-iso
mount -o loop /root/agent.x86_64.iso /mnt/agent-iso

mkdir -p /tftpboot/images/installer-openshift-4.16
cp /mnt/agent-iso/images/pxeboot/vmlinuz \
   /tftpboot/images/installer-openshift-4.16/
cp /mnt/agent-iso/images/pxeboot/initrd.img \
   /tftpboot/images/installer-openshift-4.16/initrd

# Copy rootfs
mkdir -p /tftpboot/repos/openshift-4.16
cp /mnt/agent-iso/images/pxeboot/rootfs.img \
   /tftpboot/repos/openshift-4.16/

umount /mnt/agent-iso
chmod 644 /tftpboot/images/installer-openshift-4.16/*

# Create MAC-based Ignition files
mkdir -p /tftpboot/ignition/openshift-4.16/prod/master
cat > /tftpboot/ignition/openshift-4.16/prod/master/52-54-00-aa-bb-01.ign << 'EOF'
{
  "ignition": {"version": "3.2.0"},
  "storage": {
    "files": [{
      "path": "/etc/hostname",
      "mode": 420,
      "contents": {"source": "data:,master-0.example.com"}
    }]
  }
}
EOF

# Create category
cmsh << 'EOF'
category
add openshift-416-prod-master
set bootloader syslinux
set bootloaderprotocol HTTP
set kernelparameters "coreos.inst.install_dev=/dev/sda coreos.inst.image_url=http://10.141.255.254:8080/tftpboot/repos/openshift-4.16/rootfs.img coreos.live.rootfs_url=http://10.141.255.254:8080/tftpboot/repos/openshift-4.16/rootfs.img console=tty0"
set kerneloutputconsole tty0
set installmode NEVER
set newnodeinstallmode NEVER
commit
EOF

# Create symlink
ln -sf /tftpboot/images/installer-openshift-4.16 \
       /tftpboot/images/openshift-416-prod-master

# Register node with MAC-based Ignition URL
cmsh << 'EOF'
device
add genericdevice master-0
set mac 52:54:00:AA:BB:01
set ip 10.141.160.50
set category openshift-416-prod-master
set kernelparameters "coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/openshift-4.16/prod/master/52-54-00-aa-bb-01.ign"
commit
EOF
```

## Common Pitfalls and Solutions

### Pitfall 1: Creating Software Image When You Need Installer Image

**Wrong**:
```bash
# This creates a BCM software image (not what you want for Kickstart)
cmsh << 'EOF'
softwareimage
add rhel96-installer
set path /cm/images/rhel96-installer
commit
EOF
```

**Correct**:
```bash
# Just create installer directory, no cmsh softwareimage command
mkdir -p /tftpboot/images/installer-rhel-9.6
# Extract boot files here
```

### Pitfall 2: Using Wrong Install Mode

**Wrong**:
```bash
# This makes BCM try to manage installation
set installmode AUTO
set newnodeinstallmode FULL
```

**Correct**:
```bash
# External installer handles it
set installmode NEVER
set newnodeinstallmode NEVER
```

### Pitfall 3: Forgetting the Symlink

**Wrong**:
```bash
# Category references installer-rhel-9.6 directly
category add rhel96-compute
# No symlink created
```

**Result**: BCM looks for `/tftpboot/images/rhel96-compute/` (doesn't exist)

**Correct**:
```bash
# Create symlink so BCM finds boot files
ln -sf /tftpboot/images/installer-rhel-9.6 \
       /tftpboot/images/rhel96-compute
```

### Pitfall 4: Binding ISO Instead of Copying

**Wrong**:
```bash
mount --bind /mnt/iso /tftpboot/repos/rhel-9.6
# ISO must stay mounted, not in fstab, fragile
```

**Correct**:
```bash
rsync -av /mnt/iso/ /tftpboot/repos/rhel-9.6/
umount /mnt/iso
# Can delete ISO, no fstab dependency
```

## File Organization Best Practices

```
/tftpboot/
├── repos/                                  # Installation repositories
│   ├── rhel-9.6/                          # Copied from ISO (shared)
│   │   ├── BaseOS/
│   │   ├── AppStream/
│   │   └── .treeinfo
│   └── openshift-4.16/
│       ├── agent.x86_64.iso
│       └── rootfs.img
│
├── images/                                 # Boot files
│   ├── installer-rhel-9.6/                # Master installer (reusable)
│   │   ├── vmlinuz
│   │   └── initrd
│   ├── installer-openshift-4.16/          # Master installer
│   │   ├── vmlinuz
│   │   └── initrd
│   │
│   # Category symlinks (point to installers)
│   ├── rhel96-compute -> installer-rhel-9.6/
│   ├── rhel96-gpu -> installer-rhel-9.6/
│   ├── openshift-416-prod-master -> installer-openshift-4.16/
│   └── openshift-416-prod-worker -> installer-openshift-4.16/
│
├── ks/                                     # Kickstart files (category-specific)
│   ├── rhel96-compute.cfg
│   └── rhel96-gpu.cfg
│
├── ignition/                               # Ignition files (MAC-based)
│   └── openshift-4.16/
│       └── prod/
│           └── master/
│               └── 52-54-00-aa-bb-01.ign
│
└── pxelinux.cfg/                           # PXE configs (BCM generated)
    ├── category.rhel96-compute
    └── category.openshift-416-prod-master

/cm/images/                                 # BCM Software Images (separate)
├── default-image/                          # BCM-managed
└── slurm-cluster/                          # BCM-managed
```

## Verification Checklist

After setup, verify:

- [ ] Installer directory exists: `/tftpboot/images/installer-<name>/`
- [ ] Boot files present: `vmlinuz`, `initrd`
- [ ] Repository accessible via HTTP: `curl http://<bcm>:8080/tftpboot/repos/<name>/.treeinfo`
- [ ] Kickstart/Ignition accessible: `curl http://<bcm>:8080/tftpboot/ks/<category>.cfg`
- [ ] Category symlink created: `ls -la /tftpboot/images/<category>/`
- [ ] Category configured with `installmode NEVER`
- [ ] PXE config generated: `cat /tftpboot/pxelinux.cfg/category.<category>`
- [ ] Kernel parameters include installer URL (inst.stage2 or coreos.inst)
- [ ] NOT registered as BCM software image: `cmsh -c 'softwareimage; list'` should NOT show it

## Summary

**For Kickstart/Ignition/External OS Installation**:
1. Use **installer images** in `/tftpboot/images/installer-*/`
2. Do NOT create BCM software images
3. Set `installmode NEVER`
4. Create symlinks for category name resolution
5. Provide Kickstart/Ignition via HTTP
6. One installer can serve multiple categories

**For BCM-Managed Clusters**:
1. Use **software images** in `/cm/images/*/`
2. Register via `cmsh softwareimage add`
3. Set `installmode AUTO/FULL/SYNC`
4. BCM manages the OS lifecycle
5. Nodes sync to golden master

**Key Principle**: Installer images are lightweight boot files for external installation, while software images are full OS filesystems managed by BCM.
