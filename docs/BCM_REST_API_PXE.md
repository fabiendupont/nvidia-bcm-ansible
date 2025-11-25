# BCM REST API - PXE Configuration Guide

## Overview

This document describes how to interact with NVIDIA Base Command Manager (BCM) REST API for PXE boot configuration and node management.

## API Connection Details

- **Base URL**: `https://192.168.122.163:8081/rest/v1`
- **Authentication**: HTTP Basic Auth (root:redhat)
- **Protocol**: HTTPS (self-signed certificate, use `-k` flag with curl)

## Available Endpoints

The BCM REST API v1 provides the following endpoints:

```
/rest/v1/monitoring
/rest/v1/chargeback
/rest/v1/firmware
/rest/v1/status
/rest/v1/session
/rest/v1/check
/rest/v1/version
/rest/v1/license
/rest/v1/sysinfo
/rest/v1/category      <- Primary endpoint for PXE configuration
/rest/v1/network
/rest/v1/device        <- Node/device management
/rest/v1/rack
/rest/v1/newdevice
/rest/v1/workload
/rest/v1/freeport
/rest/v1/power         <- Power management (on/off/reset/status/auxcycle)
/rest/v1/event
/rest/v1/lldp
```

## Category Endpoint (PXE Configuration)

### GET /rest/v1/category

List all categories with basic information.

**Example:**
```bash
curl -k -u root:redhat https://192.168.122.163:8081/rest/v1/category
```

**Response:**
```json
[
  {
    "image": "default-image",
    "name": "default",
    "nodes": ["node001"]
  }
]
```

### Query Specific Category

**Example:**
```bash
curl -k -u root:redhat 'https://192.168.122.163:8081/rest/v1/category?name=default'
```

**Note**: The REST API currently returns limited fields. For full category configuration including PXE settings, use the `cmsh` CLI or `pythoncm` library.

## Category PXE-Related Properties

The following properties are available for category configuration (via cmsh or pythoncm):

### Boot Configuration
- **bootloader**: Boot loader type (e.g., "syslinux", "grub")
- **bootloaderprotocol**: Protocol for retrieving boot files (e.g., "HTTP", "TFTP")
- **bootloaderfile**: Alternative boot loader file path
- **kernelversion**: Kernel version to use
- **kernelparameters**: Kernel parameters passed at boot time
- **kerneloutputconsole**: Kernel output console (e.g., "tty0")

### Installation Configuration
- **installmode**: Install mode (e.g., "AUTO", "MANUAL", "NEVER")
- **newnodeinstallmode**: Install mode for new nodes (e.g., "FULL", "SYNC")
- **softwareimage**: Software image to deploy (e.g., "default-image")
- **nodeinstallerdisk**: Whether node has its own installer disk (yes/no)
- **installbootrecord**: Install boot record on local disk (yes/no)

### Network Configuration
- **defaultgateway**: Default gateway for the category
- **defaultgatewaymetric**: Default gateway metric
- **nameservers**: List of name servers
- **timeservers**: List of time servers
- **searchdomain**: Search domains
- **managementnetwork**: Network for management traffic (e.g., "internalnet")

### Scripts and Customization
- **initializescript**: Initialize script for category
- **finalizescript**: Finalize script for category
- **excludelistfullinstall**: Exclude list for full install
- **excludelistsyncinstall**: Exclude list for sync install
- **excludelistupdate**: Exclude list for update

### Other Settings
- **notes**: Administrator notes
- **roles**: Roles assigned to nodes in this category
- **filesystemmounts**: Filesystem mounts configuration
- **staticroutes**: Static routes configuration
- **services**: Operating system services management
- **bmcsettings**: BMC (IPMI) configuration
- **selinuxsettings**: SELinux settings
- **gpusettings**: GPU configuration
- **dpusettings**: DPU settings

## Device Endpoint (Node Management)

### GET /rest/v1/device

List all devices/nodes with detailed information.

**Example:**
```bash
curl -k -u root:redhat https://192.168.122.163:8081/rest/v1/device
```

**Response:**
```json
[
  {
    "category": "default",
    "cluster": "BCM 11.0 Cluster",
    "hostname": "node001",
    "ip": "10.141.0.1",
    "mac": "00:00:00:00:00:00",
    "network": "internalnet",
    "roles": ["slurmclient", "slurmsubmit"],
    "type": "PhysicalNode",
    "uuid": "87002a80-f04f-4316-99db-c49c0eb72cc5"
  },
  {
    "cluster": "BCM 11.0 Cluster",
    "hostname": "bcm11-headnode",
    "ip": "10.141.255.254",
    "mac": "52:54:00:43:AD:E9",
    "network": "internalnet",
    "roles": [
      "backup", "storage", "headnode", "monitoring",
      "slurmserver", "slurmsubmit", "provisioning",
      "slurmaccounting", "boot"
    ],
    "type": "HeadNode",
    "uuid": "b54bba50-21d1-4e05-a355-c30f9dd6ba86"
  }
]
```

### Query Specific Device

**Example:**
```bash
curl -k -u root:redhat 'https://192.168.122.163:8081/rest/v1/device?hostname=node001'
```

## Power Management Endpoint

### Available Power Operations

The `/rest/v1/power` endpoint supports:
- **status**: Query power status
- **on**: Power on device
- **off**: Power off device
- **reset**: Reset/reboot device
- **auxcycle**: Auxiliary power cycle

## Network Endpoint

### GET /rest/v1/network

List network-related sub-endpoints.

**Response:**
```json
["topology", "nvdomain"]
```

## Using cmsh for PXE Configuration

Since the REST API returns limited fields, use `cmsh` (Cluster Management Shell) for detailed configuration:

### View Category Configuration

```bash
ssh root@192.168.122.163 "cmsh -c 'category; use default; show'"
```

### Create Category with PXE Settings

```bash
ssh root@192.168.122.163 "cmsh << 'EOF'
category
add my-pxe-category
set bootloader syslinux
set bootloaderprotocol HTTP
set installmode AUTO
set newnodeinstallmode FULL
set softwareimage default-image
set kernelparameters 'console=tty0 console=ttyS0,115200'
commit
EOF
"
```

### Assign Node to Category

```bash
ssh root@192.168.122.163 "cmsh << 'EOF'
device
use node001
set category my-pxe-category
commit
EOF
"
```

## PXE Boot Workflow

1. **Create Category**: Define category with boot loader and install settings
2. **Configure Software Image**: Specify which OS image to deploy
3. **Setup PXE Files**: Place kernel (vmlinuz) and initrd in `/tftpboot/images/<category>/`
4. **Create PXE Config**: Create category-specific PXE config in `/tftpboot/x86_64/bios/pxelinux.cfg/category.<name>`
5. **Create Kickstart**: Place kickstart file in `/tftpboot/ks/<category>.cfg`
6. **Register Node**: Create device with MAC address and assign to category
7. **Boot Node**: Node will PXE boot and install OS automatically

## Example PXE Configuration File

Location: `/tftpboot/x86_64/bios/pxelinux.cfg/category.rhel96-test`

```
DEFAULT rhel96
PROMPT 0
TIMEOUT 10
MENU TITLE RHEL 9.6 PXE Boot

LABEL rhel96
  KERNEL images/rhel96-test/vmlinuz
  APPEND initrd=images/rhel96-test/initrd.img \
         inst.ks=http://10.141.255.254:8080/tftpboot/ks/rhel96-test.cfg \
         console=tty0
  MENU LABEL ^RHEL 9.6 - Kickstart Installation
  MENU DEFAULT
```

## HTTP Server Configuration

BCM serves files via HTTP on port 8080:
- **Base URL**: `http://10.141.255.254:8080`
- **TFTP Root**: `/tftpboot/` → `http://10.141.255.254:8080/tftpboot/`
- **PXE Images**: `/tftpboot/images/` → `http://10.141.255.254:8080/tftpboot/images/`
- **Kickstarts**: `/tftpboot/ks/` → `http://10.141.255.254:8080/tftpboot/ks/`
- **OS Mirror**: `/tftpboot/rhel96/os/` → `http://10.141.255.254:8080/tftpboot/rhel96/os/`

## pythoncm Library Usage

The `pythoncm` Python library provides programmatic access to BCM:

```python
import sys
sys.path.insert(0, '/cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages')
from pythoncm.cluster import Cluster

# Connect to cluster
cluster = Cluster()

# Get category
categories = cluster.get_by_type('Category')
for cat in categories:
    if cat.name == 'default':
        print(f"Category: {cat.name}")
        print(f"Bootloader: {cat.bootloader}")
        print(f"Protocol: {cat.bootloaderprotocol}")
        break

# Create new category
new_cat = cluster.create_by_type('Category')
new_cat.name = 'test-category'
new_cat.bootloader = 'syslinux'
new_cat.bootloaderprotocol = 'HTTP'
result = new_cat.commit()

# Get device
devices = cluster.get_by_type('Device')
for device in devices:
    print(f"Device: {device.hostname}, MAC: {device.mac}")
```

## API Documentation

BCM provides a web-based API documentation interface:
- **URL**: `https://192.168.122.163:8081/api`
- **Note**: This is a React-based web application requiring JavaScript

## Common Use Cases

### 1. List All Nodes and Their Categories

```bash
curl -k -u root:redhat https://192.168.122.163:8081/rest/v1/device | \
  python3 -c "import sys, json;
  devices = json.load(sys.stdin);
  for d in devices:
      print(f'{d[\"hostname\"]}: category={d.get(\"category\", \"none\")}, mac={d[\"mac\"]}')"
```

### 2. Check Power Status

```bash
curl -k -u root:redhat https://192.168.122.163:8081/rest/v1/power/status
```

### 3. Get Category List

```bash
curl -k -u root:redhat https://192.168.122.163:8081/rest/v1/category | \
  python3 -c "import sys, json;
  cats = json.load(sys.stdin);
  for c in cats:
      print(f'{c[\"name\"]}: image={c[\"image\"]}, nodes={len(c[\"nodes\"])}')"
```

## Limitations

The current REST API has some limitations:
1. Limited fields returned (only name, image, nodes for categories)
2. Some endpoints return 501 Not Implemented for certain operations
3. Full category configuration requires `cmsh` or `pythoncm`
4. No direct PXE configuration via REST API (must use file system + cmsh)

## Recommended Approach for Ansible

For Ansible automation:
1. Use `pythoncm` library for programmatic access (already implemented in modules)
2. Use `cmsh` commands via SSH for operations not supported by pythoncm
3. Use REST API for simple queries and monitoring
4. Use file system operations for PXE config files and kickstart templates

## References

- BCM Admin Manual: `https://support.brightcomputing.com/manuals/11.0/admin-manual.pdf`
- BCM User Manual: `https://support.brightcomputing.com/manuals/11.0/user-manual.pdf`
- Base View UI: `https://192.168.122.163:8081/base-view`
- API Docs: `https://192.168.122.163:8081/api`
