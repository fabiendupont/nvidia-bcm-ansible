# RHEL 9.6 Deployment Guide - Updated for Installer Image Approach

## Overview

This guide explains how to use the updated Ansible playbooks to deploy RHEL 9.6 machines via PXE boot on NVIDIA BCM using the **installer image approach**.

## What Changed

### Previous Approach (Incorrect)
- Created BCM software images in `/cm/images/`
- Used `installmode AUTO/FULL` (BCM-managed)
- Mixed BCM image management with Kickstart
- Unnecessarily complex

### New Approach (Correct)
- Uses **installer images** only (no software images)
- Sets `installmode NEVER` (external Kickstart)
- BCM provides PXE boot, Kickstart handles installation
- Follows best practices from `BCM_PXE_INSTALLER_IMAGES.md`

### Files Modified

1. **`roles/rhel_cluster/tasks/main.yml`**
   - Removed software image creation tasks
   - Removed `set softwareimage` from category configuration
   - Now creates categories without BCM image management

2. **`roles/rhel_cluster/defaults/main.yml`**
   - Changed `install_mode: "NEVER"`
   - Changed `newnode_install_mode: "NEVER"`
   - Added comments explaining the approach

3. **`roles/rhel_cluster/README.md`**
   - Updated to explain installer image approach
   - Clarified that no BCM software images are created

4. **`inventory/test_rhel_vm.yml`**
   - Updated BCM IP to 192.168.122.204
   - Updated bcm_server to 10.141.255.254 (internal network)
   - Removed `installer_source` field (no longer needed)

## Prerequisites

### 1. RHEL ISO File

Ensure you have the RHEL 9.6 ISO file available:

**Option A**: Already on BCM head node
```bash
ssh root@192.168.122.204
ls -lh /root/rhel-9.6-x86_64-dvd.iso
```

**Option B**: Copy from local machine
```bash
scp /path/to/rhel-9.6-x86_64-dvd.iso root@192.168.122.204:/root/
```

### 2. Inventory Configuration

The inventory file defines:
- BCM head node connection details
- Cluster configuration
- Node roles (compute, GPU, storage, etc.)
- Nodes to deploy

See `inventory/test_rhel_vm.yml` for example.

### 3. VM MAC Addresses

You need the MAC addresses of VMs that will be deployed. Check your hypervisor configuration.

## Deployment Workflow

### Step 1: Prepare Inventory

Edit `inventory/test_rhel_vm.yml` or create your own:

```yaml
all:
  children:
    bcm_headnode:
      hosts:
        bcm-headnode:
          ansible_host: 192.168.122.204
          ansible_user: root

      vars:
        cluster_name: test-hpc
        rhel_version: "9.6"
        rhel_iso_path: "/root/rhel-9.6-x86_64-dvd.iso"
        root_password: "changeme123"
        bcm_server: "10.141.255.254"

        node_roles:
          - name: compute
            category: "slurm-{{ cluster_name }}-compute"
            packages:
              - "@^minimal-environment"
              - "@development-tools"
              - nfs-utils
            post_script: |
              echo "Compute node installed at $(date)" > /root/install.log

        cluster_nodes:
          - name: test-compute-01
            mac: "52:54:00:AA:01:01"
            ip: "10.141.100.101"
            category: "slurm-test-hpc-compute"
```

**Key Variables**:
- `rhel_iso_path`: Path to ISO on BCM head node
- `bcm_server`: BCM's internal network IP (10.141.255.254)
- `root_password`: Root password for installed systems
- `node_roles`: Define different node types
- `cluster_nodes`: Specific nodes to register

### Step 2: Run the Deployment Playbook

```bash
cd /home/fabiendupont/Work/NVIDIA/BCM/nvidia-bcm-ansible

# Test connectivity
ansible -i inventory/test_rhel_vm.yml bcm_headnode -m ping

# Run deployment (dry-run with --check first)
ansible-playbook -i inventory/test_rhel_vm.yml playbooks/deploy_rhel_cluster.yml --check

# Run actual deployment
ansible-playbook -i inventory/test_rhel_vm.yml playbooks/deploy_rhel_cluster.yml
```

### Step 3: What the Playbook Does

The playbook executes in two phases:

#### Phase 1: PXE Setup (pxe_setup role)
1. Creates `/tftpboot/repos/rhel-9.6/` directory
2. Mounts RHEL ISO temporarily
3. Copies ISO content to repository (can take 5-10 minutes)
4. Extracts boot files to `/tftpboot/images/installer-rhel-9.6/`
   - `vmlinuz` (kernel)
   - `initrd` (initramfs)
5. Unmounts ISO
6. Verifies HTTP access to repository

**Result**: Reusable installer infrastructure in `/tftpboot/`

#### Phase 2: RHEL Cluster Setup (rhel_cluster role)
1. Generates role-specific kickstart files
   - `/tftpboot/ks/slurm-test-hpc-compute.cfg`
2. Creates symlinks for each category
   - `/tftpboot/images/slurm-test-hpc-compute -> installer-rhel-9.6/`
3. Creates BCM categories with:
   - `bootloader syslinux`
   - `bootloaderprotocol HTTP`
   - Kernel parameters pointing to Kickstart
   - **`installmode NEVER`** (external installer)
   - **No software image** reference
4. Registers nodes in BCM
   - MAC address
   - IP address
   - Category assignment

**Result**: BCM configured for PXE boot, ready to install nodes

### Step 4: Verify Deployment

After the playbook completes, verify the setup:

```bash
# SSH to BCM head node
ssh root@192.168.122.204

# Check categories
cmsh -c 'category; list'
# Should show: slurm-test-hpc-compute

# View category details
cmsh -c 'category; use slurm-test-hpc-compute; show'
# Verify:
#   - Install mode: NEVER
#   - Kernel parameters include: inst.ks=http://...

# Check registered nodes
cmsh -c 'device; list'
# Should show: test-compute-01, test-compute-02

# Verify kickstart file exists
cat /tftpboot/ks/slurm-test-hpc-compute.cfg
curl http://10.141.255.254:8080/tftpboot/ks/slurm-test-hpc-compute.cfg

# Verify boot files
ls -la /tftpboot/images/installer-rhel-9.6/
ls -la /tftpboot/images/slurm-test-hpc-compute/

# Check PXE config (auto-generated by BCM)
cat /tftpboot/pxelinux.cfg/category.slurm-test-hpc-compute
```

**Expected PXE config**:
```
LABEL linux
  KERNEL images/slurm-test-hpc-compute/vmlinuz
  IPAPPEND 3
  APPEND initrd=images/slurm-test-hpc-compute/initrd inst.stage2=http://10.141.255.254:8080/tftpboot/repos/rhel-9.6 inst.ks=http://10.141.255.254:8080/tftpboot/ks/slurm-test-hpc-compute.cfg console=tty0
```

### Step 5: Power On Nodes

Power on the VMs to start installation:

```bash
# Option A: Via BCM
cmsh -c 'device use test-compute-01; power on'
cmsh -c 'device use test-compute-02; power on'

# Option B: Via virsh (if using libvirt)
virsh start test-compute-01
virsh start test-compute-02
```

### Step 6: Monitor Installation

**Watch node console** (via virt-manager or virsh console):
1. PXE boot
2. Download vmlinuz and initrd
3. Anaconda installer starts
4. Download and execute kickstart
5. Install packages
6. Reboot

**Check BCM device status**:
```bash
watch -n 5 'cmsh -c "device; status"'
```

**Installation timeline**:
- PXE boot: 10-30 seconds
- Kickstart download and disk setup: 1-2 minutes
- Package installation: 5-15 minutes (depends on packages)
- Post-install scripts: 1-2 minutes
- Reboot: 1 minute
- **Total**: ~10-20 minutes per node

## File Organization After Deployment

```
/tftpboot/
├── repos/
│   └── rhel-9.6/                          # Copied from ISO (9-10 GB)
│       ├── BaseOS/
│       ├── AppStream/
│       └── .treeinfo
│
├── images/
│   ├── installer-rhel-9.6/                # Master boot files (~150 MB)
│   │   ├── vmlinuz
│   │   └── initrd
│   └── slurm-test-hpc-compute -> installer-rhel-9.6/  # Symlink
│
├── ks/
│   └── slurm-test-hpc-compute.cfg         # Generated kickstart
│
└── pxelinux.cfg/
    └── category.slurm-test-hpc-compute    # BCM auto-generated PXE config

/cm/images/                                 # NO software images created!
├── default-image/                          # BCM default (pre-existing)
└── slurm-rhel-9.6/                        # BCM software image (pre-existing)
    # NOTE: Our deployment does NOT create new software images here
```

## Troubleshooting

### Issue: ISO not found
```
TASK [nvidia.bcm.pxe_setup : Mount RHEL ISO] ****
fatal: [bcm-headnode]: FAILED! => {"msg": "No such file or directory"}
```

**Solution**: Verify ISO path
```bash
ssh root@192.168.122.204 ls -lh /root/rhel-9.6-x86_64-dvd.iso
```

### Issue: Category already exists
```
TASK [nvidia.bcm.rhel_cluster : Create BCM categories via cmsh] ****
changed: [bcm-headnode] => (item=slurm-test-hpc-compute)
```

**This is OK** - The playbook handles existing categories gracefully.

### Issue: Node fails to PXE boot
**Check**:
1. Node MAC address matches inventory
2. Node is on correct network (10.141.x.x)
3. DHCP is working
4. PXE config exists: `cat /tftpboot/pxelinux.cfg/category.<category-name>`

### Issue: Kickstart download fails (404)
**Check**:
```bash
# From BCM head node
curl http://10.141.255.254:8080/tftpboot/ks/slurm-test-hpc-compute.cfg

# Check CMDaemon is running
systemctl status cmdaemon
```

### Issue: Package installation fails
**Check kickstart file**:
```bash
cat /tftpboot/ks/slurm-test-hpc-compute.cfg
```

Ensure:
- Repository URL is correct
- Packages exist in repository
- No syntax errors

## Adding More Nodes

### Same Role (Reuse Everything)

Add to `cluster_nodes` in inventory:
```yaml
cluster_nodes:
  - name: test-compute-03
    mac: "52:54:00:AA:01:03"
    ip: "10.141.100.103"
    category: "slurm-test-hpc-compute"  # Same category!
```

Run playbook again - only new node will be registered.

### New Role (New Category and Kickstart)

Add to `node_roles`:
```yaml
node_roles:
  - name: gpu
    category: "slurm-{{ cluster_name }}-gpu"
    packages:
      - "@^minimal-environment"
      - "@development-tools"
      - kernel-devel
      - pciutils
    post_script: |
      echo "blacklist nouveau" > /etc/modprobe.d/blacklist-nouveau.conf
```

Add nodes using new category:
```yaml
cluster_nodes:
  - name: test-gpu-01
    mac: "52:54:00:BB:01:01"
    ip: "10.141.101.101"
    category: "slurm-test-hpc-gpu"
```

Run playbook - new category and kickstart will be created.

## Customization

### Disk Partitioning

Edit kickstart template: `roles/rhel_cluster/templates/kickstart.cfg.j2`

Replace `autopart` with custom partitioning:
```jinja2
# Custom partitioning
part /boot --fstype=xfs --size=1024
part /boot/efi --fstype=efi --size=512
part pv.01 --size=1 --grow
volgroup vg_root pv.01
logvol / --fstype=xfs --name=lv_root --vgname=vg_root --size=50000
logvol /var --fstype=xfs --name=lv_var --vgname=vg_root --size=20000
logvol swap --fstype=swap --name=lv_swap --vgname=vg_root --size=16000
```

### Additional Packages

Add to inventory `node_roles`:
```yaml
packages:
  - "@^minimal-environment"
  - "@development-tools"
  - htop
  - iotop
  - sysstat
```

### Post-Install Configuration

Add to inventory `node_roles.post_script`:
```yaml
post_script: |
  # Configure NFS
  echo "bcm-headnode:/home /home nfs defaults 0 0" >> /etc/fstab

  # Configure Slurm
  mkdir -p /etc/slurm

  # Disable unnecessary services
  systemctl disable firewalld
  systemctl disable bluetooth

  # Custom configuration
  echo "export HISTTIMEFORMAT='%F %T '" >> /etc/profile.d/history.sh
```

## Best Practices

### 1. Version Control
Commit inventory changes:
```bash
git add inventory/
git commit -m "Add test-compute-03 node"
```

### 2. Test First
Use `--check` mode:
```bash
ansible-playbook -i inventory/test_rhel_vm.yml playbooks/deploy_rhel_cluster.yml --check
```

### 3. Backup Configurations
Before making changes:
```bash
ssh root@192.168.122.204
tar -czf /root/backup-$(date +%F).tar.gz /tftpboot/ks/ /tftpboot/images/
```

### 4. Incremental Deployment
Deploy role by role, verify each:
```bash
# Deploy only compute nodes first
# Test installation
# Then add GPU nodes
# Then add storage nodes
```

### 5. Log Everything
Playbook automatically creates:
- Deployment log: `/var/log/bcm-deployment-<cluster>-<timestamp>.log`
- Summary: `/root/deployment-summary-<cluster>.md`

## Summary

**What This Does**:
- ✅ Extracts RHEL ISO to `/tftpboot/repos/`
- ✅ Creates installer boot files in `/tftpboot/images/installer-rhel-9.6/`
- ✅ Generates role-specific kickstart files
- ✅ Creates BCM categories with `installmode NEVER`
- ✅ Registers nodes with MAC/IP/category
- ✅ Ready for PXE boot installation

**What This Does NOT Do**:
- ❌ Create BCM software images (uses installer images only)
- ❌ Use BCM install modes (AUTO/FULL/SYNC)
- ❌ Manage OS after installation (use yum/dnf)
- ❌ Power on nodes (manual step)
- ❌ Configure Slurm (separate step)

**Next Steps After Deployment**:
1. Power on nodes → Kickstart installs RHEL
2. Configure Slurm cluster
3. Set up shared storage (NFS/Lustre)
4. Install NVIDIA drivers (GPU nodes)
5. Configure user accounts
6. Set up monitoring

The playbook handles PXE infrastructure setup. Everything else is post-deployment configuration.
