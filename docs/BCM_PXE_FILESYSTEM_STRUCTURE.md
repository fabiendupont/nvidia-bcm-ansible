# BCM PXE Boot Filesystem Structure

## Overview

This document describes the filesystem structure for PXE boot configuration on NVIDIA Base Command Manager (BCM) 11.0, based on analysis of the BCM head node filesystem.

## TFTP Boot Directory Structure

### Root TFTP Directory: `/tftpboot/`

```
/tftpboot/
├── aarch64/              # ARM64 architecture boot files
├── category/             # Category-specific configurations (empty by default)
├── grub.cfg/             # GRUB configuration files
├── images/               # Boot images (kernel, initrd) per software image
│   └── default-image/
│       ├── boot -> /cm/images/default-image/boot
│       ├── initrd -> /cm/images/default-image/boot/initrd
│       └── vmlinuz -> /cm/images/default-image/boot/vmlinuz
├── mtu.conf              # MTU configuration
├── node/                 # Node-specific configurations (empty by default)
├── pxelinux.cfg/         # PXE Linux configuration files
│   ├── category.default  # Default category PXE config (generated)
│   ├── default -> /tftpboot/pxelinux.cfg/category.default
│   └── template          # Template for generating category configs
├── rescue -> /cm/local/rescue
├── unmanaged_images/     # Unmanaged boot images
└── x86_64/               # x86_64 architecture boot files
    ├── bios/             # BIOS boot files
    └── efi64/            # UEFI boot files
```

## x86_64 BIOS Boot Directory: `/tftpboot/x86_64/bios/`

```
/tftpboot/x86_64/bios/
├── arch.conf             # Architecture-specific configuration
├── bootlogo.jpg          # PXE menu background image
├── category -> ../../category        # Symlink to category configs
├── chain.c32             # Chain loading module
├── grub2.pxe             # GRUB2 PXE boot loader
├── grub_arch.conf        # GRUB architecture config
├── grub.cfg -> ../../grub.cfg/grub.cfg
├── images -> ../../images            # Symlink to boot images
├── ldlinux.c32           # SYSLINUX library
├── libcom32.c32          # COM32 library
├── libutil.c32           # Utility library
├── lpxelinux.0           # Lightweight PXE Linux boot loader
├── memtest -> memtest86_4.3.7        # Memory test utility
├── memtest86_4.3.7       # Memtest86 v4.3.7
├── memtest86+_7.20       # Memtest86+ v7.20
├── memtestplus -> memtest86+_7.20
├── menu.c32 -> vesamenu.c32          # PXE menu module
├── node -> ../../node                # Symlink to node-specific configs
├── nonvesamenu.c32       # Non-VESA menu module
├── pxelinux.0            # PXE Linux boot loader
├── pxelinux.cfg -> ../../pxelinux.cfg
├── rescue -> /cm/local/rescue
└── vesamenu.c32          # VESA menu module
```

## PXE Configuration File Structure

### Category PXE Config: `/tftpboot/pxelinux.cfg/category.default`

This file is **automatically generated** by the CMDaemon. The template is at `/tftpboot/pxelinux.cfg/template`.

**Template Variables** (substituted by CMDaemon):
- `${CMD_SERVER_IP}` → 10.141.255.254
- `${CMD_SERVER_HTTP_PORT}` → 8080
- `${CMD_SERVER_HTTPS_PORT}` → 8081
- `${CMD_SERIAL}` → Serial console configuration
- `${CMD_VMLINUZ}` → Path to kernel (e.g., images/default-image/vmlinuz)
- `${CMD_INITRD}` → Path to initrd (e.g., images/default-image/initrd)
- `${CMD_DEFAULT}` → Default boot option
- `${CMD_PXE_LABEL}` → PXE label configuration
- `${CMD_BOOTIF}` → Boot interface
- `${CMD_CONSOLE}` → Console device (e.g., tty0)
- `${CMD_PROTOCOL}` → Boot protocol
- `${CMD_KERNPARAMS}` → Kernel parameters

**Boot Labels Available**:
1. **linux** (AUTO) - Normal node boot
2. **full** (FULL) - Force FULL install (cancels burn)
3. **main** (MAIN) - Drop to maintenance shell
4. **newburn** (NEWBURN) - Force a new burn
5. **manburn** (MANBURN) - Force a new burn (no menu timeout)
6. **cancelburn** (CANCELBURN) - Cancel the current burn
7. **RESCUE** - Start rescue environment

**Example Generated Config**:
```
LABEL linux
  KERNEL images/default-image/vmlinuz
  IPAPPEND 3
  APPEND initrd=images/default-image/initrd  rd.driver.blacklist=nouveau console=tty0
  MENU LABEL ^AUTO       - Normal node boot
  MENU DEFAULT

LABEL full
  KERNEL images/default-image/vmlinuz
  IPAPPEND 3
  APPEND initrd=images/default-image/initrd  rd.driver.blacklist=nouveau console=tty0 INSTALLMODE=FULL CANCELBURN=1
  MENU LABEL ^FULL       - Force FULL install (cancels burn)
  MENU HIDE

LABEL RESCUE
  KERNEL rescue/kernel.rescue
  MENU LABEL ^RESCUE     - Start rescue environment
  APPEND vga=normal initrd=rescue/rescue.rootfs.cgz console=tty0 root=/dev/ram0 rw nokeymap

DEFAULT menu.c32
PROMPT 0
TIMEOUT 50
MENU TITLE Cluster Manager PXE Environment
MENU BACKGROUND bootlogo.jpg
```

## BCM Software Structure

### Cluster Manager Directory: `/cm/`

```
/cm/
├── CLUSTERMANAGERID      # Cluster ID file
├── conf/                 # Cluster configuration
├── images/               # Software images
│   └── default-image/
│       └── boot/
│           ├── initrd
│           └── vmlinuz
├── local/                # Local BCM software
│   └── apps/
│       ├── cmd/          # CMDaemon
│       │   ├── bin/
│       │   ├── etc/      # CMDaemon configuration
│       │   │   ├── cmd.conf
│       │   │   └── htdocs/  # Web interface files
│       │   │       ├── api/          # API documentation UI
│       │   │       ├── base-view/    # Base View UI
│       │   │       ├── userportal/   # User Portal UI
│       │   │       └── ...
│       │   ├── pythoncm/ # Python CM library
│       │   │   └── lib/python3.12/site-packages/pythoncm/
│       │   │       └── entity/
│       │   │           ├── category.py
│       │   │           ├── device.py
│       │   │           └── ...
│       │   ├── scripts/
│       │   └── sbin/
│       ├── python312/    # Python 3.12
│       ├── slurm/        # Slurm workload manager
│       └── ...
├── node-installer/       # Node installer images
└── shared/               # Shared cluster resources
```

### pythoncm Entity Files

Location: `/cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages/pythoncm/entity/`

Key entity implementations:
- `category.py` - Category management
- `device.py` - Device/node management
- `computenode.py` - Compute node specific
- `softwareimage.py` - Software image management
- `bmcsettings.py` - BMC/IPMI configuration
- `role.py` - Role management
- `configurationoverlay.py` - Configuration overlays

## PXE Boot Workflow

### 1. PXE Boot Request
- Node sends DHCP request
- BCM DHCP server responds with:
  - IP address
  - Next-server (TFTP server IP)
  - Boot filename (e.g., `x86_64/bios/lpxelinux.0` or `x86_64/bios/pxelinux.0`)

### 2. TFTP Boot Loader Download
- Node downloads boot loader via TFTP
- Boot loader loads configuration from:
  - `/tftpboot/x86_64/bios/pxelinux.cfg/01-<mac-address>` (node-specific)
  - `/tftpboot/x86_64/bios/pxelinux.cfg/category.<category-name>` (category-specific)
  - `/tftpboot/x86_64/bios/pxelinux.cfg/default` (default fallback)

### 3. Boot Menu Display
- PXE menu is displayed with available boot options
- Default option auto-boots after timeout (5 seconds)

### 4. Kernel and Initrd Loading
- Kernel (vmlinuz) is loaded via HTTP or TFTP
- Initrd is loaded via HTTP or TFTP
- Kernel parameters are passed (including install mode, console, etc.)

### 5. OS Installation/Boot
- Based on install mode:
  - **AUTO**: Automatic installation decision
  - **FULL**: Full OS installation
  - **SYNC**: Sync installation (incremental)
  - **MAIN**: Drop to maintenance shell
  - **NEVER**: Skip installation

## HTTP File Serving

BCM serves files via HTTP on port 8080 (managed by CMDaemon):

**Base URL**: `http://<bcm-ip>:8080/`

**Available paths**:
- `/tftpboot/` → Serves `/tftpboot/` directory
  - `/tftpboot/images/` → Boot images
  - `/tftpboot/ks/` → Kickstart files (custom)
  - `/tftpboot/rhel96/os/` → OS mirrors (custom)

## Custom PXE Boot Configuration

### Adding a Custom Category

1. **Create Category** (via cmsh or pythoncm):
```bash
cmsh -c 'category; add my-custom-category; commit'
```

2. **Configure Boot Settings**:
```bash
cmsh -c '
category
use my-custom-category
set bootloader syslinux
set bootloaderprotocol HTTP
set kernelparameters "console=tty0 console=ttyS0,115200"
commit
'
```

3. **CMDaemon Generates PXE Config**:
   - File: `/tftpboot/pxelinux.cfg/category.my-custom-category`
   - Generated from template with variables substituted

### Adding Custom Boot Images

1. **Create Image Directory**:
```bash
mkdir -p /tftpboot/images/my-custom-image
```

2. **Copy Kernel and Initrd**:
```bash
cp /path/to/vmlinuz /tftpboot/images/my-custom-image/
cp /path/to/initrd.img /tftpboot/images/my-custom-image/initrd
chmod 644 /tftpboot/images/my-custom-image/*
```

3. **Update Category Software Image**:
```bash
cmsh -c '
category
use my-custom-category
set softwareimage my-custom-image
commit
'
```

### Adding Custom Kickstart

1. **Create Kickstart Directory**:
```bash
mkdir -p /tftpboot/ks
```

2. **Create Kickstart File**:
```bash
cat > /tftpboot/ks/my-category.cfg << 'EOF'
#version=RHEL9
url --url="http://10.141.255.254:8080/tftpboot/rhel96/os"
rootpw --plaintext changeme
autopart
reboot
EOF
chmod 644 /tftpboot/ks/my-category.cfg
```

3. **Customize Category PXE Config** (optional):
   - Edit `/tftpboot/pxelinux.cfg/category.my-category`
   - Add custom boot labels with kickstart reference

### Serving OS Installation Media

1. **Mount ISO**:
```bash
mkdir -p /mnt/rhel-iso
mount -o loop /path/to/rhel.iso /mnt/rhel-iso
```

2. **Create Mirror**:
```bash
mkdir -p /tftpboot/rhel96/os
mount --bind /mnt/rhel-iso /tftpboot/rhel96/os
```

3. **Verify HTTP Access**:
```bash
curl http://10.141.255.254:8080/tftpboot/rhel96/os/.treeinfo
```

## Important Notes

1. **Auto-Generated Files**: Do not manually edit files with "automatically generated by cmd" header
2. **Symlinks**: Many directories use symlinks - be careful when modifying
3. **HTTP vs TFTP**: Modern BCM prefers HTTP for boot file transfer (faster)
4. **Boot Loader Protocol**: Set via category `bootloaderprotocol` (HTTP or TFTP)
5. **IPAPPEND 3**: Required for all boot labels to pass network info to ramdisk

## Troubleshooting

### Check TFTP Service
```bash
systemctl status tftpd.service
journalctl -u tftpd.service -f
```

### Check HTTP Service (CMDaemon)
```bash
systemctl status cmdaemon
tail -f /var/log/cmd/cmdaemon.log
```

### Verify PXE Files
```bash
ls -la /tftpboot/x86_64/bios/pxelinux.cfg/category.*
cat /tftpboot/pxelinux.cfg/category.default
```

### Test HTTP File Access
```bash
curl http://10.141.255.254:8080/tftpboot/images/default-image/vmlinuz -I
curl http://10.141.255.254:8080/tftpboot/ks/test.cfg
```

## References

- Template File: `/tftpboot/pxelinux.cfg/template`
- CMDaemon Config: `/cm/local/apps/cmd/etc/cmd.conf`
- pythoncm Library: `/cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages/pythoncm/`
