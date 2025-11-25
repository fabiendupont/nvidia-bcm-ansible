# BCM PXE Boot Templating Guide

## Overview

BCM uses a templating mechanism to automatically generate PXE boot configurations. This guide explains how to leverage this system to minimize manual filesystem manipulation.

## How BCM PXE Templating Works

### Template File
**Location**: `/tftpboot/pxelinux.cfg/template`

This template is used by CMDaemon to generate category-specific PXE configs automatically.

### Generated Files
**Location**: `/tftpboot/pxelinux.cfg/category.<category-name>`

These files are **automatically generated** by CMDaemon and should **not be edited manually**.

### Template Variables

CMDaemon substitutes these variables when generating PXE configs:

| Variable | Description | Example Value |
|----------|-------------|---------------|
| `${CMD_SERVER_IP}` | BCM server IP address | 10.141.255.254 |
| `${CMD_SERVER_HTTP_PORT}` | HTTP port for file serving | 8080 |
| `${CMD_SERVER_HTTPS_PORT}` | HTTPS port for REST API | 8081 |
| `${CMD_VMLINUZ}` | Path to kernel relative to TFTP root | images/default-image/vmlinuz |
| `${CMD_INITRD}` | Path to initrd relative to TFTP root | images/default-image/initrd |
| `${CMD_KERNPARAMS}` | Kernel parameters from category config | rd.driver.blacklist=nouveau |
| `${CMD_CONSOLE}` | Console device | tty0 |
| `${CMD_DEFAULT}` | Default boot menu handler | menu.c32 |
| `${CMD_PXE_LABEL}` | Default PXE label to boot | (empty) |
| `${CMD_SERIAL}` | Serial console configuration | (empty) |
| `${CMD_BOOTIF}` | Boot interface | (empty) |
| `${CMD_PROTOCOL}` | Boot protocol (HTTP/TFTP) | (empty) |

## Using the Templating System for Custom OS Installation

### Approach 1: Using Kernel Parameters (Recommended)

You can add kickstart URLs and other installer parameters via the category's `kernelparameters` setting.

#### Example: RHEL/Rocky Linux with Kickstart

```bash
# Create category
cmsh -c 'category; add rhel96-pxe; commit'

# Configure kernel parameters to include kickstart
cmsh << 'EOF'
category
use rhel96-pxe
set bootloader syslinux
set bootloaderprotocol HTTP
set softwareimage rhel96-image
set kernelparameters "inst.ks=http://10.141.255.254:8080/tftpboot/ks/rhel96.cfg console=tty0"
commit
EOF
```

**What this does**:
1. CMDaemon regenerates `/tftpboot/pxelinux.cfg/category.rhel96-pxe`
2. The kernel parameters are substituted into `${CMD_KERNPARAMS}`
3. All boot labels automatically include the kickstart URL

**Pros**:
- No manual PXE config file editing
- Parameters apply to all boot modes (AUTO, FULL, MAIN, etc.)
- CMDaemon manages the file automatically

**Cons**:
- Kickstart applies to ALL boots, including maintenance mode
- Cannot have different kickstarts for different boot labels

### Approach 2: Custom Software Image with Boot Files

Create a custom software image that points to your RHEL installation kernel/initrd.

#### Step 1: Extract Boot Files from ISO

```bash
# Mount ISO
mkdir -p /mnt/rhel96-iso
mount -o loop /root/rhel-9.6-x86_64-dvd.iso /mnt/rhel96-iso

# Create image directory (matches software image name)
mkdir -p /tftpboot/images/rhel96-image

# Extract kernel and initrd
cp /mnt/rhel96-iso/images/pxeboot/vmlinuz /tftpboot/images/rhel96-image/
cp /mnt/rhel96-iso/images/pxeboot/initrd.img /tftpboot/images/rhel96-image/initrd
chmod 644 /tftpboot/images/rhel96-image/*
```

#### Step 2: Create Software Image in BCM

```bash
cmsh << 'EOF'
softwareimage
clone default-image rhel96-image
use rhel96-image
set kernelversion custom-rhel96
set kernelparameters "inst.stage2=http://10.141.255.254:8080/tftpboot/rhel96/os inst.ks=http://10.141.255.254:8080/tftpboot/ks/rhel96.cfg"
commit
EOF
```

#### Step 3: Assign to Category

```bash
cmsh << 'EOF'
category
use rhel96-pxe
set softwareimage rhel96-image
commit
EOF
```

**Result**: CMDaemon automatically updates the category PXE config to use the new image's kernel/initrd.

### Approach 3: Hybrid - Template + Custom Boot Label

For advanced scenarios where you need custom boot options, you can modify the template and regenerate.

#### Step 1: Backup Original Template

```bash
cp /tftpboot/pxelinux.cfg/template /tftpboot/pxelinux.cfg/template.backup
```

#### Step 2: Add Custom Label to Template

```bash
cat >> /tftpboot/pxelinux.cfg/template << 'EOF'

LABEL rhel_install
  KERNEL images/rhel96-image/vmlinuz
  IPAPPEND 3
  APPEND initrd=images/rhel96-image/initrd inst.stage2=http://${CMD_SERVER_IP}:${CMD_SERVER_HTTP_PORT}/tftpboot/rhel96/os inst.ks=http://${CMD_SERVER_IP}:${CMD_SERVER_HTTP_PORT}/tftpboot/ks/rhel96.cfg console=${CMD_CONSOLE}
  MENU LABEL ^RHEL Install - Custom RHEL 9.6 Installation
  MENU HIDE
EOF
```

#### Step 3: Regenerate Category Config

```bash
# Touch the category to trigger regeneration
cmsh -c 'category; use rhel96-pxe; set notes "Updated"; commit'
```

**Warning**: This modifies the global template and affects ALL categories. Use with caution.

## Complete Workflow: RHEL PXE Installation Using Templating

### Prerequisites
- RHEL 9.6 ISO available at `/root/rhel-9.6-x86_64-dvd.iso`
- Target node MAC address

### Step 1: Prepare HTTP Mirror

```bash
# Mount ISO
mkdir -p /mnt/rhel96-iso
mount -o loop /root/rhel-9.6-x86_64-dvd.iso /mnt/rhel96-iso

# Create mirror accessible via HTTP
mkdir -p /tftpboot/rhel96/os
mount --bind /mnt/rhel96-iso /tftpboot/rhel96/os

# Verify HTTP access
curl http://10.141.255.254:8080/tftpboot/rhel96/os/.treeinfo
```

### Step 2: Extract Boot Files

```bash
# Create image directory
mkdir -p /tftpboot/images/rhel96-image

# Copy kernel and initrd
cp /mnt/rhel96-iso/images/pxeboot/vmlinuz /tftpboot/images/rhel96-image/
cp /mnt/rhel96-iso/images/pxeboot/initrd.img /tftpboot/images/rhel96-image/initrd
chmod 644 /tftpboot/images/rhel96-image/*
```

### Step 3: Create Kickstart File

```bash
# Create kickstart directory
mkdir -p /tftpboot/ks

# Create kickstart
cat > /tftpboot/ks/rhel96-auto.cfg << 'EOF'
#version=RHEL9
auth --enableshadow --passalgo=sha512
url --url="http://10.141.255.254:8080/tftpboot/rhel96/os"
keyboard --vckeymap=us --xlayouts='us'
lang en_US.UTF-8
network --bootproto=dhcp --device=link --onboot=on --activate
rootpw --plaintext changeme123
timezone UTC --utc
ignoredisk --only-use=vda
clearpart --all --initlabel --drives=vda
autopart --type=lvm
bootloader --location=mbr --boot-drive=vda
selinux --enforcing
firewall --enabled --ssh
skipx
reboot

%packages
@^minimal-environment
@standard
%end
EOF

chmod 644 /tftpboot/ks/rhel96-auto.cfg

# Verify HTTP access
curl http://10.141.255.254:8080/tftpboot/ks/rhel96-auto.cfg
```

### Step 4: Create Category Using Template System

```bash
cmsh << 'EOF'
category
add rhel96-auto
set bootloader syslinux
set bootloaderprotocol HTTP
set kernelparameters "inst.stage2=http://10.141.255.254:8080/tftpboot/rhel96/os inst.ks=http://10.141.255.254:8080/tftpboot/ks/rhel96-auto.cfg"
set kerneloutputconsole tty0
set installmode FULL
set newnodeinstallmode FULL
commit
EOF
```

**Note**: We're NOT setting `softwareimage` yet. We'll create a minimal reference.

### Step 5: Configure Software Image Reference

Option A: Use existing image (simpler):
```bash
cmsh << 'EOF'
category
use rhel96-auto
set softwareimage default-image
commit
EOF
```

Option B: Create custom software image:
```bash
cmsh << 'EOF'
softwareimage
clone default-image rhel96-image
commit

category
use rhel96-auto
set softwareimage rhel96-image
commit
EOF
```

### Step 6: Override Kernel Path (If Needed)

The template uses `${CMD_VMLINUZ}` which points to `images/<softwareimage>/vmlinuz`. If you placed your files in `/tftpboot/images/rhel96-image/`, you need to either:

**Option A**: Make sure software image name matches directory name
**Option B**: Create symlinks

```bash
# Option B: Symlink approach
ln -sf /tftpboot/images/rhel96-image /tftpboot/images/default-image-rhel96
```

### Step 7: Verify Generated PXE Config

```bash
cat /tftpboot/pxelinux.cfg/category.rhel96-auto
```

You should see:
```
LABEL linux
  KERNEL images/default-image/vmlinuz
  IPAPPEND 3
  APPEND initrd=images/default-image/initrd inst.stage2=http://10.141.255.254:8080/tftpboot/rhel96/os inst.ks=http://10.141.255.254:8080/tftpboot/ks/rhel96-auto.cfg console=tty0
  MENU LABEL ^AUTO       - Normal node boot
  MENU DEFAULT
```

### Step 8: Register Node

```bash
cmsh << 'EOF'
device
add genericdevice rhel96-test
set mac 52:54:00:xx:xx:xx
set ip 10.141.160.100
set category rhel96-auto
commit
EOF
```

### Step 9: Boot Node

Power on the node. It will:
1. PXE boot from BCM
2. Load `/tftpboot/pxelinux.cfg/category.rhel96-auto`
3. Download kernel/initrd via HTTP
4. Boot with kickstart parameters
5. Install RHEL 9.6 automatically

## Ansible Implementation

### Playbook Structure Using Templating

```yaml
---
- name: PXE Boot Setup Using BCM Templating
  hosts: localhost
  become: yes

  vars:
    bcm_server: "10.141.255.254"
    category_name: "rhel96-auto"
    iso_path: "/root/rhel-9.6-x86_64-dvd.iso"

  tasks:
    # 1. Setup HTTP mirror (only filesystem operation needed)
    - name: Mount and serve ISO
      include_tasks: setup_http_mirror.yml

    # 2. Extract boot files (only filesystem operation needed)
    - name: Extract kernel and initrd
      include_tasks: extract_boot_files.yml

    # 3. Create kickstart (only filesystem operation needed)
    - name: Create kickstart file
      ansible.builtin.copy:
        dest: "/tftpboot/ks/{{ category_name }}.cfg"
        content: "{{ kickstart_content }}"

    # 4. Let BCM handle PXE config via templating
    - name: Create category with kernel parameters
      nvidia.bcm.bcm_category:
        name: "{{ category_name }}"
        state: present
        bootloader: syslinux
        bootloaderprotocol: HTTP
        kernelparameters: >-
          inst.stage2=http://{{ bcm_server }}:8080/tftpboot/rhel96/os
          inst.ks=http://{{ bcm_server }}:8080/tftpboot/ks/{{ category_name }}.cfg
        kerneloutputconsole: tty0
        installmode: FULL
        newnodeinstallmode: FULL

    # 5. Register node
    - name: Register node
      nvidia.bcm.bcm_node:
        name: "{{ node_name }}"
        mac: "{{ node_mac }}"
        ip: "{{ node_ip }}"
        category: "{{ category_name }}"
        state: present
```

## Benefits of Using BCM Templating

1. **No Manual PXE Config Editing**: CMDaemon manages all PXE config files
2. **Automatic Updates**: Category changes automatically regenerate PXE configs
3. **Consistency**: All boot labels (AUTO, FULL, MAIN, etc.) get consistent parameters
4. **Version Control Friendly**: Only track category settings, not generated files
5. **Disaster Recovery**: Easier to rebuild - just recreate categories

## Limitations

1. **Global Template**: Template modifications affect all categories
2. **Standard Boot Labels**: Limited to pre-defined boot labels (linux, full, main, etc.)
3. **Same Parameters for All Labels**: Cannot have different kickstarts for different boot modes
4. **Boot File Location**: Must match software image directory structure

## Best Practices

1. **Minimal Filesystem Operations**:
   - Only create: kickstart files, HTTP mirrors, and extracted boot files
   - Let BCM manage: PXE configs, category configs

2. **Use Kernel Parameters**:
   - Add installer-specific parameters via `kernelparameters`
   - Include: kickstart URL, installation source, console settings

3. **Software Image Organization**:
   - Match software image name to boot file directory
   - Use descriptive names: `rhel96-image`, `rocky9-image`, etc.

4. **Category Naming**:
   - Use clear, descriptive names: `rhel96-auto`, `ubuntu-kickstart`
   - Include version and purpose in name

5. **Kickstart Location**:
   - Store in `/tftpboot/ks/` for HTTP access
   - Match kickstart filename to category name

## Troubleshooting

### PXE Config Not Updated

```bash
# Force regeneration by updating category
cmsh -c 'category; use rhel96-auto; set notes "Force update"; commit'

# Check generated config
cat /tftpboot/pxelinux.cfg/category.rhel96-auto
```

### Wrong Kernel/Initrd Path

```bash
# Verify software image setting
cmsh -c 'category; use rhel96-auto; get softwareimage'

# Check actual file location
ls -la /tftpboot/images/default-image/vmlinuz
ls -la /tftpboot/images/default-image/initrd
```

### Kickstart Not Found

```bash
# Verify HTTP access
curl -I http://10.141.255.254:8080/tftpboot/ks/rhel96-auto.cfg

# Check file permissions
ls -la /tftpboot/ks/rhel96-auto.cfg
```

## Summary

The BCM templating system significantly reduces filesystem manipulation:

**Required Filesystem Operations**:
- Extract kernel/initrd from ISO → `/tftpboot/images/<name>/`
- Create kickstart file → `/tftpboot/ks/`
- Mount ISO for HTTP serving → `/tftpboot/<distro>/os/`

**NOT Required** (BCM Handles):
- ✅ PXE config file generation
- ✅ Template variable substitution
- ✅ Boot label configuration
- ✅ Category-specific configs

This approach is cleaner, more maintainable, and better suited for automation with Ansible.
