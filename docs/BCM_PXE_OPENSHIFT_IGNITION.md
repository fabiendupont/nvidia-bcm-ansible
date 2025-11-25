# BCM PXE Boot with OpenShift Agent-based Installer and Ignition

## Overview

OpenShift uses Ignition for node configuration instead of Kickstart. The Agent-based installer generates a custom ISO with embedded configuration. This guide explains how to integrate OpenShift deployment with BCM's PXE boot infrastructure.

## OpenShift Installation Methods

### 1. Agent-based Installer (Recommended for BCM)

**Process**:
1. Use `openshift-install` to generate agent ISO
2. ISO contains: CoreOS kernel/initrd + embedded Ignition config
3. Extract kernel/initrd from generated ISO
4. Serve Ignition config and rootfs via HTTP
5. PXE boot nodes with kernel parameters pointing to configs

**Advantages with BCM**:
- Can extract and PXE boot the agent installer
- Ignition config embedded in ISO or served via HTTP
- Works with BCM's templating system
- Multiple node roles via different Ignition configs

### 2. Network-based (PXE) Installation

**Process**:
1. Use standard CoreOS kernel/initrd
2. Serve Ignition configs via HTTP
3. Point nodes to Ignition config via kernel parameters
4. Nodes download and apply config on boot

## Architecture Comparison

### Kickstart (RHEL/Rocky)
```
PXE Boot → Anaconda Installer → Kickstart (scripted install) → Installed OS
```

### Ignition (OpenShift/CoreOS)
```
PXE Boot → CoreOS Live → Ignition (declarative config) → Configured System
```

**Key Differences**:
- **Kickstart**: Procedural script (do this, then that)
- **Ignition**: Declarative config (system should look like this)
- **Timing**: Ignition runs on first boot, not during install
- **Format**: Ignition uses JSON, Kickstart uses INI-style

## File Organization for OpenShift

```
/tftpboot/
├── repos/
│   └── openshift-4.16/                 # OpenShift installation assets
│       ├── agent.x86_64.iso            # Agent-based installer ISO
│       ├── rootfs.img                  # CoreOS root filesystem
│       └── release-images/             # Container images (optional)
│
├── images/
│   ├── installer-openshift-4.16/       # Master installer boot files
│   │   ├── vmlinuz                     # CoreOS kernel
│   │   └── initrd.img                  # CoreOS initramfs
│   ├── openshift-master -> installer-openshift-4.16/
│   ├── openshift-worker -> installer-openshift-4.16/
│   └── openshift-infra -> installer-openshift-4.16/
│
├── ignition/                           # Ignition configs (category-specific)
│   ├── master.ign                      # Master nodes config
│   ├── worker.ign                      # Worker nodes config
│   ├── infra.ign                       # Infrastructure nodes config
│   └── agent-config.yaml               # Agent installer config
│
└── ks/                                 # Kickstart (for RHEL nodes)
    └── ...
```

## OpenShift Agent-based Installer Workflow

### Step 1: Prepare Installation Assets

```bash
# Download OpenShift installer and CLI
OPENSHIFT_VERSION=4.16.0
wget https://mirror.openshift.com/pub/openshift-v4/clients/ocp/${OPENSHIFT_VERSION}/openshift-install-linux.tar.gz
wget https://mirror.openshift.com/pub/openshift-v4/clients/ocp/${OPENSHIFT_VERSION}/openshift-client-linux.tar.gz

tar xvf openshift-install-linux.tar.gz
tar xvf openshift-client-linux.tar.gz

sudo mv openshift-install oc kubectl /usr/local/bin/
```

### Step 2: Create Installation Configuration

```bash
mkdir -p ~/openshift-install
cd ~/openshift-install

# Create install-config.yaml
cat > install-config.yaml << 'EOF'
apiVersion: v1
baseDomain: example.com
metadata:
  name: ocp-cluster
networking:
  networkType: OVNKubernetes
  clusterNetwork:
  - cidr: 10.128.0.0/14
    hostPrefix: 23
  serviceNetwork:
  - 172.30.0.0/16
  machineNetwork:
  - cidr: 10.141.0.0/16
compute:
- name: worker
  replicas: 2
controlPlane:
  name: master
  replicas: 3
platform:
  baremetal:
    apiVIPs:
    - 10.141.160.10
    ingressVIPs:
    - 10.141.160.11
pullSecret: '{"auths":...}'  # Get from console.redhat.com
sshKey: 'ssh-rsa AAAA...'    # Your SSH public key
EOF

# Create agent-config.yaml
cat > agent-config.yaml << 'EOF'
apiVersion: v1alpha1
kind: AgentConfig
metadata:
  name: ocp-cluster
rendezvousIP: 10.141.160.50  # First master node IP
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
        dhcp: false
    dns-resolver:
      config:
        server:
        - 10.141.255.254
    routes:
      config:
      - destination: 0.0.0.0/0
        next-hop-address: 10.141.255.254
        next-hop-interface: eno1

- hostname: master-1
  role: master
  interfaces:
  - name: eno1
    macAddress: 52:54:00:AA:BB:02
  # ... similar network config ...

- hostname: worker-0
  role: worker
  interfaces:
  - name: eno1
    macAddress: 52:54:00:AA:BB:10
  # ... network config ...
EOF
```

### Step 3: Generate Agent ISO

```bash
cd ~/openshift-install

# Generate agent ISO with embedded configs
openshift-install agent create image \
  --dir . \
  --log-level debug

# This creates: agent.x86_64.iso
```

### Step 4: Extract Boot Files from Agent ISO

```bash
# Create repository directory
mkdir -p /tftpboot/repos/openshift-4.16

# Copy agent ISO to repository
cp ~/openshift-install/agent.x86_64.iso /tftpboot/repos/openshift-4.16/

# Mount ISO to extract boot files
mkdir -p /mnt/agent-iso
mount -o loop /tftpboot/repos/openshift-4.16/agent.x86_64.iso /mnt/agent-iso

# Create installer directory
mkdir -p /tftpboot/images/installer-openshift-4.16

# Extract kernel and initrd
cp /mnt/agent-iso/images/pxeboot/vmlinuz \
   /tftpboot/images/installer-openshift-4.16/vmlinuz
cp /mnt/agent-iso/images/pxeboot/initrd.img \
   /tftpboot/images/installer-openshift-4.16/initrd

# Extract rootfs (important for OpenShift!)
cp /mnt/agent-iso/images/pxeboot/rootfs.img \
   /tftpboot/repos/openshift-4.16/rootfs.img

# Unmount
umount /mnt/agent-iso

# Set permissions
chmod 644 /tftpboot/images/installer-openshift-4.16/*
chmod 644 /tftpboot/repos/openshift-4.16/rootfs.img
```

### Step 5: Extract Ignition Configs from ISO

The agent ISO embeds Ignition configs. For PXE boot, we need to extract or regenerate them.

**Option A: Use Embedded Config**
```bash
# Mount ISO again
mount -o loop /tftpboot/repos/openshift-4.16/agent.x86_64.iso /mnt/agent-iso

# Look for embedded ignition
find /mnt/agent-iso -name "*.ign" -o -name "config.ign"

# Copy to ignition directory
mkdir -p /tftpboot/ignition
cp /mnt/agent-iso/config.ign /tftpboot/ignition/agent.ign

umount /mnt/agent-iso
```

**Option B: Generate Role-Specific Ignition Configs**

For more granular control, generate separate configs for master/worker:

```bash
# Create ignition directory structure
mkdir -p /tftpboot/ignition/{master,worker,bootstrap}

# Master ignition config (example - simplified)
cat > /tftpboot/ignition/master.ign << 'EOF'
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
          "source": "data:,master-node"
        }
      }
    ]
  },
  "systemd": {
    "units": [
      {
        "name": "install-openshift.service",
        "enabled": true,
        "contents": "[Service]\nType=oneshot\nExecStart=/usr/local/bin/install-openshift.sh\n[Install]\nWantedBy=multi-user.target"
      }
    ]
  }
}
EOF

# Worker ignition config
cat > /tftpboot/ignition/worker.ign << 'EOF'
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
          "source": "data:,worker-node"
        }
      }
    ]
  }
}
EOF

chmod 644 /tftpboot/ignition/*.ign
```

### Step 6: Create Symlinks for Categories

```bash
# Master nodes
ln -sf /tftpboot/images/installer-openshift-4.16 \
       /tftpboot/images/openshift-master

# Worker nodes
ln -sf /tftpboot/images/installer-openshift-4.16 \
       /tftpboot/images/openshift-worker

# Infrastructure nodes (if needed)
ln -sf /tftpboot/images/installer-openshift-4.16 \
       /tftpboot/images/openshift-infra
```

### Step 7: Configure BCM Categories

**Master Nodes Category**:
```bash
cmsh << 'EOF'
category
add openshift-master
set bootloader syslinux
set bootloaderprotocol HTTP
set kernelparameters "coreos.inst.install_dev=/dev/sda coreos.inst.image_url=http://10.141.255.254:8080/tftpboot/repos/openshift-4.16/rootfs.img coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/master.ign coreos.live.rootfs_url=http://10.141.255.254:8080/tftpboot/repos/openshift-4.16/rootfs.img console=tty0"
set kerneloutputconsole tty0
set installmode NEVER
set newnodeinstallmode NEVER
commit
EOF
```

**Worker Nodes Category**:
```bash
cmsh << 'EOF'
category
add openshift-worker
set bootloader syslinux
set bootloaderprotocol HTTP
set kernelparameters "coreos.inst.install_dev=/dev/sda coreos.inst.image_url=http://10.141.255.254:8080/tftpboot/repos/openshift-4.16/rootfs.img coreos.inst.ignition_url=http://10.141.255.254:8080/tftpboot/ignition/worker.ign coreos.live.rootfs_url=http://10.141.255.254:8080/tftpboot/repos/openshift-4.16/rootfs.img console=tty0"
set kerneloutputconsole tty0
set installmode NEVER
set newnodeinstallmode NEVER
commit
EOF
```

**Important Kernel Parameters for CoreOS**:
- `coreos.inst.install_dev`: Target disk for installation
- `coreos.inst.image_url`: CoreOS image URL
- `coreos.inst.ignition_url`: Ignition config URL
- `coreos.live.rootfs_url`: Live rootfs for PXE boot

**Note**: `installmode=NEVER` because CoreOS handles its own installation via Ignition.

### Step 8: Verify Generated PXE Configs

```bash
# Check master category
cat /tftpboot/pxelinux.cfg/category.openshift-master

# Should see kernel parameters with Ignition URLs
# APPEND initrd=images/openshift-master/initrd coreos.inst.ignition_url=http://...
```

### Step 9: Register Nodes

```bash
# Master nodes
cmsh << 'EOF'
device
add genericdevice master-0
set mac 52:54:00:AA:BB:01
set ip 10.141.160.50
set category openshift-master
commit

device
add genericdevice master-1
set mac 52:54:00:AA:BB:02
set ip 10.141.160.51
set category openshift-master
commit
EOF

# Worker nodes
cmsh << 'EOF'
device
add genericdevice worker-0
set mac 52:54:00:AA:BB:10
set ip 10.141.160.60
set category openshift-worker
commit
EOF
```

## Ignition Config Generation Strategies

### Strategy 1: Static Ignition Files (Simple)

Pre-generate Ignition configs for each role and serve as static files.

**Pros**:
- Simple to manage
- Easy to version control
- Works with BCM templating

**Cons**:
- Less dynamic
- Need to regenerate for changes

### Strategy 2: Dynamic Ignition Generation (Advanced)

Generate Ignition configs dynamically based on node MAC/hostname.

```bash
# Create Ignition generator script
cat > /usr/local/bin/generate-ignition.sh << 'EOF'
#!/bin/bash
NODE_MAC=$1
NODE_ROLE=$2
NODE_HOSTNAME=$3

# Generate dynamic Ignition based on parameters
cat > /tftpboot/ignition/${NODE_MAC}.ign << IGNITION
{
  "ignition": {"version": "3.2.0"},
  "storage": {
    "files": [{
      "path": "/etc/hostname",
      "mode": 420,
      "contents": {"source": "data:,${NODE_HOSTNAME}"}
    }]
  }
}
IGNITION
EOF

chmod +x /usr/local/bin/generate-ignition.sh

# Generate per-node configs
/usr/local/bin/generate-ignition.sh 52:54:00:AA:BB:01 master master-0
/usr/local/bin/generate-ignition.sh 52:54:00:AA:BB:10 worker worker-0
```

### Strategy 3: Ignition Templates with Butane

Use Butane (YAML) to generate Ignition (JSON) configs.

```bash
# Install Butane
wget https://github.com/coreos/butane/releases/download/v0.20.0/butane-x86_64-unknown-linux-gnu
chmod +x butane-x86_64-unknown-linux-gnu
sudo mv butane-x86_64-unknown-linux-gnu /usr/local/bin/butane

# Create Butane config (YAML - easier to read/write)
cat > /tmp/master.bu << 'EOF'
variant: fcos
version: 1.5.0
storage:
  files:
    - path: /etc/hostname
      mode: 0644
      contents:
        inline: master-node
    - path: /etc/NetworkManager/system-connections/eno1.nmconnection
      mode: 0600
      contents:
        inline: |
          [connection]
          id=eno1
          type=ethernet
          interface-name=eno1
          [ipv4]
          method=manual
          addresses=10.141.160.50/16
          gateway=10.141.255.254
          dns=10.141.255.254
systemd:
  units:
    - name: install-to-disk.service
      enabled: true
      contents: |
        [Unit]
        After=network-online.target
        [Service]
        Type=oneshot
        ExecStart=/usr/bin/coreos-installer install /dev/sda --ignition-url http://10.141.255.254:8080/tftpboot/ignition/master-post-install.ign
        [Install]
        WantedBy=multi-user.target
EOF

# Convert Butane (YAML) to Ignition (JSON)
butane -p -s < /tmp/master.bu > /tftpboot/ignition/master.ign
```

## Ansible Playbook for OpenShift PXE Setup

```yaml
---
- name: Setup OpenShift PXE Boot with Agent-based Installer
  hosts: localhost
  become: yes

  vars:
    openshift_version: "4.16.0"
    bcm_server: "10.141.255.254"
    install_dir: "/root/openshift-install"

    cluster_name: "ocp-cluster"
    base_domain: "example.com"

    # Repository and boot file paths
    repo_path: "/tftpboot/repos/openshift-{{ openshift_version }}"
    installer_path: "/tftpboot/images/installer-openshift-{{ openshift_version }}"
    ignition_path: "/tftpboot/ignition"

  tasks:
    # =========================================================================
    # PHASE 1: Download OpenShift Tools
    # =========================================================================

    - name: Download openshift-install
      ansible.builtin.get_url:
        url: "https://mirror.openshift.com/pub/openshift-v4/clients/ocp/{{ openshift_version }}/openshift-install-linux.tar.gz"
        dest: "/tmp/openshift-install.tar.gz"

    - name: Extract openshift-install
      ansible.builtin.unarchive:
        src: "/tmp/openshift-install.tar.gz"
        dest: "/usr/local/bin"
        remote_src: yes
        creates: "/usr/local/bin/openshift-install"

    # =========================================================================
    # PHASE 2: Generate Agent ISO
    # =========================================================================

    - name: Create installation directory
      ansible.builtin.file:
        path: "{{ install_dir }}"
        state: directory

    - name: Create install-config.yaml
      ansible.builtin.template:
        src: install-config.yaml.j2
        dest: "{{ install_dir }}/install-config.yaml"

    - name: Create agent-config.yaml
      ansible.builtin.template:
        src: agent-config.yaml.j2
        dest: "{{ install_dir }}/agent-config.yaml"

    - name: Generate agent ISO
      ansible.builtin.command:
        cmd: openshift-install agent create image --dir {{ install_dir }}
        creates: "{{ install_dir }}/agent.x86_64.iso"

    # =========================================================================
    # PHASE 3: Extract Boot Files
    # =========================================================================

    - name: Create repository directory
      ansible.builtin.file:
        path: "{{ repo_path }}"
        state: directory

    - name: Copy agent ISO to repository
      ansible.builtin.copy:
        src: "{{ install_dir }}/agent.x86_64.iso"
        dest: "{{ repo_path }}/agent.x86_64.iso"
        remote_src: yes

    - name: Mount agent ISO
      ansible.posix.mount:
        path: /mnt/agent-iso
        src: "{{ repo_path }}/agent.x86_64.iso"
        fstype: iso9660
        opts: loop,ro
        state: mounted

    - name: Create installer directory
      ansible.builtin.file:
        path: "{{ installer_path }}"
        state: directory

    - name: Extract kernel
      ansible.builtin.copy:
        src: /mnt/agent-iso/images/pxeboot/vmlinuz
        dest: "{{ installer_path }}/vmlinuz"
        remote_src: yes
        mode: '0644'

    - name: Extract initrd
      ansible.builtin.copy:
        src: /mnt/agent-iso/images/pxeboot/initrd.img
        dest: "{{ installer_path }}/initrd"
        remote_src: yes
        mode: '0644'

    - name: Extract rootfs
      ansible.builtin.copy:
        src: /mnt/agent-iso/images/pxeboot/rootfs.img
        dest: "{{ repo_path }}/rootfs.img"
        remote_src: yes
        mode: '0644'

    - name: Unmount agent ISO
      ansible.posix.mount:
        path: /mnt/agent-iso
        state: unmounted

    # =========================================================================
    # PHASE 4: Setup Ignition Configs
    # =========================================================================

    - name: Create ignition directory
      ansible.builtin.file:
        path: "{{ ignition_path }}"
        state: directory

    - name: Create master ignition config
      ansible.builtin.template:
        src: master.ign.j2
        dest: "{{ ignition_path }}/master.ign"
        mode: '0644'

    - name: Create worker ignition config
      ansible.builtin.template:
        src: worker.ign.j2
        dest: "{{ ignition_path }}/worker.ign"
        mode: '0644'

    # =========================================================================
    # PHASE 5: Create BCM Categories
    # =========================================================================

    - name: Create symlinks for categories
      ansible.builtin.file:
        src: "{{ installer_path }}"
        dest: "/tftpboot/images/openshift-{{ item }}"
        state: link
      loop:
        - master
        - worker

    - name: Configure OpenShift master category
      nvidia.bcm.bcm_category:
        name: openshift-master
        state: present
        bootloader: syslinux
        bootloaderprotocol: HTTP
        kernelparameters: >-
          coreos.inst.install_dev=/dev/sda
          coreos.inst.image_url=http://{{ bcm_server }}:8080{{ repo_path }}/rootfs.img
          coreos.inst.ignition_url=http://{{ bcm_server }}:8080{{ ignition_path }}/master.ign
          coreos.live.rootfs_url=http://{{ bcm_server }}:8080{{ repo_path }}/rootfs.img
        kerneloutputconsole: tty0
        installmode: NEVER
        newnodeinstallmode: NEVER

    - name: Configure OpenShift worker category
      nvidia.bcm.bcm_category:
        name: openshift-worker
        state: present
        bootloader: syslinux
        bootloaderprotocol: HTTP
        kernelparameters: >-
          coreos.inst.install_dev=/dev/sda
          coreos.inst.image_url=http://{{ bcm_server }}:8080{{ repo_path }}/rootfs.img
          coreos.inst.ignition_url=http://{{ bcm_server }}:8080{{ ignition_path }}/worker.ign
          coreos.live.rootfs_url=http://{{ bcm_server }}:8080{{ repo_path }}/rootfs.img
        kerneloutputconsole: tty0
        installmode: NEVER
        newnodeinstallmode: NEVER

    # =========================================================================
    # PHASE 6: Register Nodes
    # =========================================================================

    - name: Register master nodes
      nvidia.bcm.bcm_node:
        name: "{{ item.name }}"
        mac: "{{ item.mac }}"
        ip: "{{ item.ip }}"
        category: openshift-master
        state: present
      loop:
        - {name: master-0, mac: "52:54:00:AA:BB:01", ip: "10.141.160.50"}
        - {name: master-1, mac: "52:54:00:AA:BB:02", ip: "10.141.160.51"}
        - {name: master-2, mac: "52:54:00:AA:BB:03", ip: "10.141.160.52"}

    - name: Register worker nodes
      nvidia.bcm.bcm_node:
        name: "{{ item.name }}"
        mac: "{{ item.mac }}"
        ip: "{{ item.ip }}"
        category: openshift-worker
        state: present
      loop:
        - {name: worker-0, mac: "52:54:00:AA:BB:10", ip: "10.141.160.60"}
        - {name: worker-1, mac: "52:54:00:AA:BB:11", ip: "10.141.160.61"}
```

## Summary: Kickstart vs Ignition with BCM

| Aspect | Kickstart (RHEL) | Ignition (OpenShift) |
|--------|------------------|----------------------|
| **Config Format** | INI-style text | JSON |
| **Config Location** | `/tftpboot/ks/*.cfg` | `/tftpboot/ignition/*.ign` |
| **Kernel Parameter** | `inst.ks=http://...` | `coreos.inst.ignition_url=http://...` |
| **Install Mode** | AUTO/FULL/SYNC | NEVER (CoreOS handles install) |
| **Category Specific** | Yes (different kickstarts) | Yes (different ignition files) |
| **Reusable Boot Files** | Yes (via symlinks) | Yes (via symlinks) |
| **BCM Templating** | ✅ Full support | ✅ Full support |
| **Additional Files** | ISO repository | ISO + rootfs.img |

Both approaches leverage BCM's templating system identically - only the kernel parameters and config file format differ!
