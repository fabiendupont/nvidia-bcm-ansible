# PXE Setup Role

This role sets up the PXE boot infrastructure for NVIDIA Base Command Manager (BCM), supporting both RHEL+Slurm and OpenShift deployments.

## Features

- Extract and copy ISO contents to permanent storage
- Extract boot files (kernel, initrd, rootfs) for PXE boot
- Create symlinks for category boot files
- Verify HTTP accessibility of boot files
- Support for both RHEL and OpenShift deployments

## Requirements

- Ansible 2.15+
- BCM head node with `/tftpboot` filesystem
- ISO files for RHEL and/or OpenShift
- `ansible.posix` collection for mount and synchronize modules

## Role Variables

### Required Variables

- `rhel_iso_path`: Path to RHEL ISO file (if deploying RHEL)
- `openshift_iso_path`: Path to OpenShift agent ISO file (if deploying OpenShift)

### Optional Variables

See `defaults/main.yml` for all available variables:

- `bcm_server`: BCM server IP address (default: `ansible_default_ipv4.address`)
- `tftpboot_path`: Base TFTP path (default: `/tftpboot`)
- `http_port`: HTTP server port (default: `8080`)
- `rhel_version`: RHEL version (default: `9.6`)
- `openshift_version`: OpenShift version (default: `4.16`)
- `cleanup_iso_after_copy`: Remove ISO after copying (default: `false`)
- `verify_http_access`: Verify HTTP access to boot files (default: `true`)

### Category Symlinks

To create symlinks for categories, define `pxe_categories`:

```yaml
pxe_categories:
  - name: slurm-hpc01-compute
    installer_source: installer-rhel-9.6
  - name: openshift-416-prod-worker
    installer_source: installer-openshift-4.16
```

## Example Playbook

### RHEL Setup

```yaml
- hosts: bcm_headnode
  become: true
  roles:
    - role: nvidia.bcm.pxe_setup
      vars:
        rhel_iso_path: /root/rhel-9.6-x86_64-dvd.iso
        rhel_version: "9.6"
        pxe_categories:
          - name: slurm-hpc01-compute
            installer_source: installer-rhel-9.6
          - name: slurm-hpc01-gpu
            installer_source: installer-rhel-9.6
```

### OpenShift Setup

```yaml
- hosts: bcm_headnode
  become: true
  roles:
    - role: nvidia.bcm.pxe_setup
      vars:
        openshift_iso_path: /root/agent.x86_64.iso
        openshift_version: "4.16"
        pxe_categories:
          - name: openshift-416-prod-master
            installer_source: installer-openshift-4.16
          - name: openshift-416-prod-worker
            installer_source: installer-openshift-4.16
```

### Combined Setup

```yaml
- hosts: bcm_headnode
  become: true
  roles:
    - role: nvidia.bcm.pxe_setup
      vars:
        rhel_iso_path: /root/rhel-9.6-x86_64-dvd.iso
        openshift_iso_path: /root/agent.x86_64.iso
        rhel_version: "9.6"
        openshift_version: "4.16"
        pxe_categories:
          - name: slurm-hpc01-compute
            installer_source: installer-rhel-9.6
          - name: openshift-416-prod-worker
            installer_source: installer-openshift-4.16
```

## File Organization

After running this role, the following structure is created:

```
/tftpboot/
├── repos/
│   ├── rhel-9.6/                    # RHEL repository (copied from ISO)
│   └── openshift-4.16/              # OpenShift assets
│       ├── agent.x86_64.iso
│       └── rootfs.img
├── images/
│   ├── installer-rhel-9.6/          # Master RHEL boot files
│   │   ├── vmlinuz
│   │   └── initrd
│   ├── installer-openshift-4.16/    # Master OpenShift boot files
│   │   ├── vmlinuz
│   │   └── initrd
│   ├── slurm-hpc01-compute -> installer-rhel-9.6/        # Symlinks
│   └── openshift-416-prod-worker -> installer-openshift-4.16/
├── ks/                              # Kickstart files (managed by other roles)
└── ignition/                        # Ignition files (managed by other roles)
```

## License

GPL-3.0-or-later

## Author

NVIDIA Corporation
