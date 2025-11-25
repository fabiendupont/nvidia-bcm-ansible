## RHEL Cluster Role

This role deploys RHEL+Slurm clusters on NVIDIA Base Command Manager (BCM) using PXE boot with Kickstart installation.

## Approach: Installer Images (Not BCM Software Images)

This role uses the **installer image approach** for external OS installation:
- Boot files only (no BCM software images in `/cm/images/`)
- Kickstart handles the complete installation
- BCM provides PXE boot infrastructure only
- Install mode: `NEVER` (external Kickstart installer)
- OS managed via standard package management (yum/dnf)

See `docs/BCM_PXE_INSTALLER_IMAGES.md` for detailed explanation.

## Features

- Generate role-specific kickstart files from templates
- Create BCM categories for different node roles (with `installmode NEVER`)
- Create symlinks from category names to installer boot files
- Register nodes in BCM with proper categorization
- Support for multiple node roles (compute, login, GPU, storage, etc.)
- No BCM software image creation (uses installer images only)

## Requirements

- Ansible 2.15+
- BCM head node with PXE infrastructure already set up (use `pxe_setup` role first)
- `nvidia.bcm` collection modules

## Role Variables

### Required Variables

```yaml
node_roles:
  - name: compute                              # Role name
    category: slurm-hpc01-compute             # BCM category name
    packages:                                  # Packages to install
      - "@^minimal-environment"
      - "@development-tools"
      - slurm-slurmd
    post_script: |                            # Optional post-install script
      echo "Compute node configured"
```

### Optional Variables

See `defaults/main.yml` for all available variables:

- `cluster_name`: Cluster identifier (default: `hpc01`)
- `rhel_version`: RHEL version (default: `9.6`)
- `root_password`: Root password for installed systems (default: `changeme123`)
- `install_mode`: BCM install mode (default: `NEVER` - external Kickstart)
- `newnode_install_mode`: New node install mode (default: `NEVER`)
- `selinux_mode`: SELinux mode (default: `enforcing`)

### Node Registration

To register nodes, define `cluster_nodes`:

```yaml
cluster_nodes:
  - name: compute-01
    mac: "52:54:00:AA:01:01"
    ip: "10.141.100.1"
    category: slurm-hpc01-compute
    rack: "A1"                    # Optional
    rackposition: 10              # Optional
```

## Dependencies

This role should be used after the `pxe_setup` role has configured the PXE infrastructure.

## Example Playbook

### Basic RHEL Cluster

```yaml
- hosts: bcm_headnode
  become: true
  vars:
    cluster_name: hpc01
    rhel_version: "9.6"

    node_roles:
      - name: compute
        category: "slurm-{{ cluster_name }}-compute"
        packages:
          - "@^minimal-environment"
          - "@development-tools"
          - slurm-slurmd
          - nfs-utils
        post_script: |
          # Configure NFS mounts
          echo "bcm-headnode:/home /home nfs defaults 0 0" >> /etc/fstab
          mount -a

      - name: gpu
        category: "slurm-{{ cluster_name }}-gpu-a100"
        packages:
          - "@^minimal-environment"
          - "@development-tools"
          - slurm-slurmd
          - kernel-devel
          - pciutils
        post_script: |
          # Prepare for NVIDIA driver installation
          echo "blacklist nouveau" > /etc/modprobe.d/blacklist-nouveau.conf

    cluster_nodes:
      - name: compute-01
        mac: "52:54:00:AA:01:01"
        ip: "10.141.100.1"
        category: "slurm-{{ cluster_name }}-compute"

      - name: gpu-01
        mac: "52:54:00:BB:01:01"
        ip: "10.141.101.1"
        category: "slurm-{{ cluster_name }}-gpu-a100"

  roles:
    - nvidia.bcm.rhel_cluster
```

### Multi-Role Cluster

```yaml
- hosts: bcm_headnode
  become: true
  vars:
    cluster_name: hpc02

    node_roles:
      - name: login
        category: "slurm-{{ cluster_name }}-login"
        packages:
          - "@^minimal-environment"
          - slurm-slurmctld
          - slurm-slurmd

      - name: compute-cpu
        category: "slurm-{{ cluster_name }}-compute-cpu"
        packages:
          - "@^minimal-environment"
          - slurm-slurmd

      - name: compute-gpu
        category: "slurm-{{ cluster_name }}-compute-gpu"
        packages:
          - "@^minimal-environment"
          - slurm-slurmd
          - kernel-devel

      - name: storage
        category: "slurm-{{ cluster_name }}-storage"
        packages:
          - "@^minimal-environment"
          - nfs-utils
          - "@file-server"

  roles:
    - nvidia.bcm.rhel_cluster
```

## Workflow

1. **Kickstart Generation**: Creates role-specific kickstart files in `/tftpboot/ks/`
2. **Symlink Creation**: Links category names to installer boot files in `/tftpboot/images/installer-*/`
3. **Category Creation**: Registers categories in BCM with:
   - Kickstart URL in kernel parameters
   - `installmode NEVER` (no BCM image management)
   - No software image reference (external installation)
4. **Node Registration**: Registers nodes with their assigned categories

**Important**: This role does NOT create BCM software images. It uses installer images only. Nodes boot from local disk after Kickstart installation completes.

## File Organization

After running this role:

```
/tftpboot/
├── ks/
│   ├── slurm-hpc01-compute.cfg           # Generated kickstart
│   ├── slurm-hpc01-gpu-a100.cfg
│   └── slurm-hpc01-storage.cfg
└── images/
    ├── installer-rhel-9.6/               # Master boot files (from pxe_setup)
    ├── slurm-hpc01-compute -> installer-rhel-9.6/    # Symlinks
    ├── slurm-hpc01-gpu-a100 -> installer-rhel-9.6/
    └── slurm-hpc01-storage -> installer-rhel-9.6/
```

## Deployment Process

After running this role:

1. Nodes are registered in BCM with their categories
2. Power on nodes (or run `cmsh device use <node>; power on`)
3. Nodes PXE boot, download kickstart, and install RHEL
4. Nodes reboot into installed system
5. Complete Slurm configuration as needed

## License

GPL-3.0-or-later

## Author

NVIDIA Corporation
