# BCM PXE Boot - Best Practices and File Organization

## Architecture Overview

### Software Images vs Categories

**Software Image**:
- Represents a complete OS installation image
- Contains: kernel, initrd, full filesystem
- Location: `/cm/images/<image-name>/`
- Boot files: `/cm/images/<image-name>/boot/vmlinuz` and `initrd`
- Purpose: What OS/configuration to install
- Reusable: Multiple categories can use the same software image

**Category**:
- Represents a group of nodes with similar configuration
- References a software image
- Contains: boot parameters, install mode, roles, services
- Purpose: How to install and configure nodes
- Specific: Tailored to node role/purpose

**Kickstart**:
- Installation automation script
- Can be category-specific OR software-image-specific
- Location: `/tftpboot/ks/` (for custom OS installs)
- Referenced via: kernel parameters in category configuration

## File Organization Strategy

### 1. Installation Media (OS Repository)

**Location**: `/tftpboot/repos/<os-name>-<version>/`

**Why**:
- Separate from boot files
- Can be shared across multiple categories/images
- Easy to manage and update
- Clear naming convention

**Example**:
```
/tftpboot/repos/
├── rhel-9.6/
│   ├── BaseOS/
│   ├── AppStream/
│   └── .treeinfo
├── rocky-9.5/
│   └── ...
└── ubuntu-22.04/
    └── ...
```

**Setup** (copy, not bind mount):
```bash
# Mount ISO temporarily
mkdir -p /mnt/rhel96-iso
mount -o loop /root/rhel-9.6-x86_64-dvd.iso /mnt/rhel96-iso

# Copy to permanent location (can unmount ISO after)
mkdir -p /tftpboot/repos/rhel-9.6
rsync -av /mnt/rhel96-iso/ /tftpboot/repos/rhel-9.6/

# Unmount ISO
umount /mnt/rhel96-iso

# Verify HTTP access
curl http://10.141.255.254:8080/tftpboot/repos/rhel-9.6/.treeinfo
```

**Benefits**:
- ✅ ISO can be removed/unmounted
- ✅ Repository persists across reboots
- ✅ No fstab dependencies
- ✅ Can delete ISO to save space

### 2. Boot Files (Kernel & Initrd)

**Location**: `/tftpboot/images/<purpose>-<os>-<version>/`

**Why**:
- Matches BCM's expected structure
- Can be symlinked by multiple categories
- Separate installer kernels from system kernels
- Clear purpose identification

**Example**:
```
/tftpboot/images/
├── installer-rhel-9.6/
│   ├── vmlinuz       # Installer kernel
│   └── initrd        # Installer initrd
├── installer-rocky-9.5/
│   ├── vmlinuz
│   └── initrd
└── default-image/    # BCM managed
    ├── boot -> /cm/images/default-image/boot
    ├── initrd -> /cm/images/default-image/boot/initrd
    └── vmlinuz -> /cm/images/default-image/boot/vmlinuz
```

**Setup**:
```bash
# Extract installer boot files
mkdir -p /tftpboot/images/installer-rhel-9.6

# From mounted ISO
cp /mnt/rhel96-iso/images/pxeboot/vmlinuz \
   /tftpboot/images/installer-rhel-9.6/vmlinuz
cp /mnt/rhel96-iso/images/pxeboot/initrd.img \
   /tftpboot/images/installer-rhel-9.6/initrd

# Set permissions
chmod 644 /tftpboot/images/installer-rhel-9.6/*
```

**Symlinking for Multiple Categories**:
```bash
# Category 1: RHEL compute nodes
ln -s /tftpboot/images/installer-rhel-9.6 \
      /tftpboot/images/rhel96-compute

# Category 2: RHEL GPU nodes
ln -s /tftpboot/images/installer-rhel-9.6 \
      /tftpboot/images/rhel96-gpu

# Both categories use same installer kernel/initrd
# but different kickstarts and configurations
```

### 3. Kickstart Files

**Location**: `/tftpboot/ks/<category-name>.cfg`

**Why Kickstart Belongs to Category**:
- Different categories need different configurations
- Same OS, different purposes (compute vs GPU vs storage)
- Category-specific: hostname patterns, partitioning, packages
- Software image is generic; kickstart is specific

**Example**:
```
/tftpboot/ks/
├── rhel96-compute.cfg    # Compute nodes kickstart
├── rhel96-gpu.cfg        # GPU nodes kickstart (NVIDIA drivers)
├── rhel96-storage.cfg    # Storage nodes kickstart (different partitioning)
└── rocky95-test.cfg      # Test environment
```

**Kickstart Template** (category-specific):
```bash
cat > /tftpboot/ks/rhel96-compute.cfg << 'EOF'
#version=RHEL9

# Installation source - shared repository
url --url="http://10.141.255.254:8080/tftpboot/repos/rhel-9.6"

# Basic configuration
auth --enableshadow --passalgo=sha512
keyboard --vckeymap=us --xlayouts='us'
lang en_US.UTF-8
timezone UTC --utc

# Network - DHCP during install
network --bootproto=dhcp --device=link --onboot=on --activate

# Root password
rootpw --plaintext changeme123

# Disk partitioning - COMPUTE NODE SPECIFIC
ignoredisk --only-use=sda
clearpart --all --initlabel --drives=sda
part /boot --fstype=xfs --size=1024
part /boot/efi --fstype=efi --size=512
part pv.01 --size=1 --grow
volgroup vg_root pv.01
logvol / --fstype=xfs --name=lv_root --vgname=vg_root --size=50000
logvol /home --fstype=xfs --name=lv_home --vgname=vg_root --size=20000
logvol swap --fstype=swap --name=lv_swap --vgname=vg_root --size=16000
logvol /var --fstype=xfs --name=lv_var --vgname=vg_root --size=1 --grow

# Bootloader
bootloader --location=mbr --boot-drive=sda

# Security
selinux --enforcing
firewall --enabled --ssh

# No GUI
skipx
reboot

# Packages - COMPUTE NODE SPECIFIC
%packages
@^minimal-environment
@development-tools
kernel-devel
kernel-headers
gcc
make
%end

%post --log=/root/ks-post.log
echo "Compute node installation completed"
# Add compute-specific post-install steps
%end
EOF
```

**GPU Kickstart** (different from compute):
```bash
cat > /tftpboot/ks/rhel96-gpu.cfg << 'EOF'
#version=RHEL9

# Same base as compute, but different packages and post-install

url --url="http://10.141.255.254:8080/tftpboot/repos/rhel-9.6"

# ... same basic config ...

# Packages - GPU NODE SPECIFIC
%packages
@^minimal-environment
@development-tools
kernel-devel
kernel-headers
gcc
make
pciutils
%end

%post --log=/root/ks-post.log
echo "GPU node installation completed"

# Install NVIDIA drivers
# Configure CUDA
# GPU-specific setup
%end
EOF
```

## Complete PXE Setup Workflow

### Step 1: Prepare Installation Repository (One-Time)

```bash
# Mount ISO
mkdir -p /mnt/rhel96-iso
mount -o loop /root/rhel-9.6-x86_64-dvd.iso /mnt/rhel96-iso

# Copy to permanent location
mkdir -p /tftpboot/repos/rhel-9.6
rsync -av --progress /mnt/rhel96-iso/ /tftpboot/repos/rhel-9.6/

# Unmount and optionally remove ISO
umount /mnt/rhel96-iso
# rm /root/rhel-9.6-x86_64-dvd.iso  # Save space

# Verify
curl -I http://10.141.255.254:8080/tftpboot/repos/rhel-9.6/.treeinfo
```

### Step 2: Extract Boot Files (One-Time per OS Version)

```bash
# Create directory
mkdir -p /tftpboot/images/installer-rhel-9.6

# Extract from ISO (before unmounting)
cp /mnt/rhel96-iso/images/pxeboot/vmlinuz \
   /tftpboot/images/installer-rhel-9.6/vmlinuz
cp /mnt/rhel96-iso/images/pxeboot/initrd.img \
   /tftpboot/images/installer-rhel-9.6/initrd

# Set permissions
chmod 644 /tftpboot/images/installer-rhel-9.6/*

# Verify
ls -lh /tftpboot/images/installer-rhel-9.6/
```

### Step 3: Create Category-Specific Kickstart

```bash
mkdir -p /tftpboot/ks

cat > /tftpboot/ks/rhel96-compute.cfg << 'EOF'
# Your category-specific kickstart here
EOF

chmod 644 /tftpboot/ks/rhel96-compute.cfg

# Verify HTTP access
curl http://10.141.255.254:8080/tftpboot/ks/rhel96-compute.cfg
```

### Step 4: Create Symlink for Category Boot Files

```bash
# Link to shared installer boot files
ln -sf /tftpboot/images/installer-rhel-9.6 \
       /tftpboot/images/rhel96-compute

# Verify
ls -la /tftpboot/images/rhel96-compute/
```

### Step 5: Configure Category Using BCM Templating

```bash
cmsh << 'EOF'
category
add rhel96-compute
set bootloader syslinux
set bootloaderprotocol HTTP
set kernelparameters "inst.stage2=http://10.141.255.254:8080/tftpboot/repos/rhel-9.6 inst.ks=http://10.141.255.254:8080/tftpboot/ks/rhel96-compute.cfg"
set kerneloutputconsole tty0
set installmode AUTO
set newnodeinstallmode FULL
commit
EOF
```

**Note**: We reference the symlink name `rhel96-compute` which BCM will use as `images/rhel96-compute/vmlinuz`.

### Step 6: Verify Generated PXE Config

```bash
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

### Step 7: Create Additional Categories (Reusing Files)

```bash
# Create GPU category kickstart
cat > /tftpboot/ks/rhel96-gpu.cfg << 'EOF'
# GPU-specific kickstart
EOF

# Create symlink to same installer
ln -sf /tftpboot/images/installer-rhel-9.6 \
       /tftpboot/images/rhel96-gpu

# Configure GPU category
cmsh << 'EOF'
category
add rhel96-gpu
set bootloader syslinux
set bootloaderprotocol HTTP
set kernelparameters "inst.stage2=http://10.141.255.254:8080/tftpboot/repos/rhel-9.6 inst.ks=http://10.141.255.254:8080/tftpboot/ks/rhel96-gpu.cfg"
set kerneloutputconsole tty0
commit
EOF
```

## File Organization Summary

```
/tftpboot/
├── repos/                          # Installation repositories (copied from ISOs)
│   ├── rhel-9.6/                   # Shared by all RHEL 9.6 categories
│   │   ├── BaseOS/
│   │   ├── AppStream/
│   │   └── .treeinfo
│   └── rocky-9.5/
│       └── ...
│
├── images/                         # Boot files
│   ├── installer-rhel-9.6/         # Master installer boot files
│   │   ├── vmlinuz
│   │   └── initrd
│   ├── rhel96-compute -> installer-rhel-9.6/   # Symlink for compute category
│   ├── rhel96-gpu -> installer-rhel-9.6/       # Symlink for GPU category
│   └── default-image/              # BCM managed
│       └── ...
│
├── ks/                             # Kickstart files (category-specific)
│   ├── rhel96-compute.cfg          # Compute nodes configuration
│   ├── rhel96-gpu.cfg              # GPU nodes configuration
│   └── rhel96-storage.cfg          # Storage nodes configuration
│
├── pxelinux.cfg/                   # PXE configs (BCM generated)
│   ├── template                    # Template (DO NOT EDIT GENERATED FILES)
│   ├── category.rhel96-compute     # Auto-generated from template
│   ├── category.rhel96-gpu         # Auto-generated from template
│   └── default -> category.default
│
└── x86_64/bios/                    # Boot loaders and symlinks
    └── ...
```

## Ansible Playbook Best Practices

```yaml
---
- name: Setup RHEL 9.6 PXE Boot Infrastructure
  hosts: localhost
  become: yes

  vars:
    os_name: rhel
    os_version: "9.6"
    iso_path: "/root/rhel-9.6-x86_64-dvd.iso"
    bcm_server: "10.141.255.254"

    # Reusable paths
    repo_path: "/tftpboot/repos/{{ os_name }}-{{ os_version }}"
    installer_path: "/tftpboot/images/installer-{{ os_name }}-{{ os_version }}"

  tasks:
    # =========================================================================
    # PHASE 1: One-time OS setup (reusable across categories)
    # =========================================================================

    - name: Create repository directory
      ansible.builtin.file:
        path: "{{ repo_path }}"
        state: directory
        mode: '0755'

    - name: Mount ISO temporarily
      ansible.posix.mount:
        path: /mnt/temp-iso
        src: "{{ iso_path }}"
        fstype: iso9660
        opts: loop,ro
        state: mounted

    - name: Copy ISO content to repository (can take time)
      ansible.posix.synchronize:
        src: /mnt/temp-iso/
        dest: "{{ repo_path }}/"
        archive: yes
      delegate_to: "{{ inventory_hostname }}"

    - name: Unmount ISO
      ansible.posix.mount:
        path: /mnt/temp-iso
        state: unmounted

    - name: Create installer boot files directory
      ansible.builtin.file:
        path: "{{ installer_path }}"
        state: directory
        mode: '0755'

    - name: Extract kernel from repository
      ansible.builtin.copy:
        src: "{{ repo_path }}/images/pxeboot/vmlinuz"
        dest: "{{ installer_path }}/vmlinuz"
        remote_src: yes
        mode: '0644'

    - name: Extract initrd from repository
      ansible.builtin.copy:
        src: "{{ repo_path }}/images/pxeboot/initrd.img"
        dest: "{{ installer_path }}/initrd"
        remote_src: yes
        mode: '0644'

    # =========================================================================
    # PHASE 2: Category-specific setup (per node type)
    # =========================================================================

    - name: Create category-specific configurations
      include_tasks: setup_category.yml
      loop:
        - name: rhel96-compute
          packages: ['@development-tools', 'kernel-devel']
        - name: rhel96-gpu
          packages: ['@development-tools', 'kernel-devel', 'pciutils']
      loop_control:
        loop_var: category

# setup_category.yml
---
- name: Create symlink for category boot files
  ansible.builtin.file:
    src: "{{ installer_path }}"
    dest: "/tftpboot/images/{{ category.name }}"
    state: link

- name: Create category kickstart
  ansible.builtin.template:
    src: kickstart.cfg.j2
    dest: "/tftpboot/ks/{{ category.name }}.cfg"
    mode: '0644'

- name: Configure BCM category
  nvidia.bcm.bcm_category:
    name: "{{ category.name }}"
    state: present
    bootloader: syslinux
    bootloaderprotocol: HTTP
    kernelparameters: >-
      inst.stage2=http://{{ bcm_server }}:8080{{ repo_path }}
      inst.ks=http://{{ bcm_server }}:8080/tftpboot/ks/{{ category.name }}.cfg
    kerneloutputconsole: tty0
    installmode: AUTO
    newnodeinstallmode: FULL
```

## Key Advantages

1. **ISO Independence**: Copy files, then unmount/delete ISO
2. **File Reuse**: One installer serves multiple categories via symlinks
3. **Clear Separation**:
   - Repository: Shared OS files
   - Installer: Shared boot files
   - Kickstart: Category-specific configuration
4. **Easy Updates**: Update installer once, affects all categories
5. **Storage Efficient**: Symlinks prevent duplication
6. **BCM Native**: Use templating for PXE configs, minimal manual files

## Summary

**File Ownership**:
- Software Image → OS runtime (what runs after install)
- Category → Configuration (how to install and configure)
- Kickstart → Category-specific automation

**Best Practice**:
```
Repository (shared)  →  Multiple Categories
    ↓                        ↓
Installer (shared)   →  Category 1 → Kickstart 1
    ↓                   Category 2 → Kickstart 2
Symlinks             →  Category 3 → Kickstart 3
```
