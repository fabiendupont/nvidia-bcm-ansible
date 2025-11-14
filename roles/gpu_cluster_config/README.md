# GPU Cluster Configuration Role

Configure NVIDIA Base Command Manager for optimal GPU workload performance.

## Description

This role optimizes BCM configuration for GPU clusters by:
- Setting appropriate kernel parameters to disable nouveau and enable NVIDIA drivers
- Configuring network MTU for GPU Direct RDMA
- Updating category documentation

## Requirements

- NVIDIA BCM 11.0+
- nvidia.bcm collection installed
- Root or sudo access to BCM head node

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `gpu_image_name` | `default-image` | Software image to configure |
| `gpu_kernel_params` | `rd.driver.blacklist=nouveau nvidia-drm.modeset=1 quiet` | Kernel parameters for GPU nodes |
| `gpu_network_name` | `internalnet` | Network to configure |
| `gpu_network_mtu` | `9000` | MTU for GPU networking (jumbo frames) |
| `gpu_category_name` | `default` | Category to update |
| `gpu_category_notes` | `GPU compute nodes with NVIDIA drivers` | Category documentation |

## Dependencies

None

## Example Playbook

```yaml
---
- name: Configure GPU Cluster
  hosts: localhost
  gather_facts: false

  roles:
    - role: nvidia.bcm.gpu_cluster_config
      vars:
        gpu_image_name: rhel9-gpu
        gpu_network_mtu: 9000
```

## Example with Custom Variables

```yaml
---
- name: Configure GPU Cluster with Custom Settings
  hosts: localhost
  gather_facts: false

  roles:
    - role: nvidia.bcm.gpu_cluster_config
      vars:
        gpu_image_name: rhel9-cuda12
        gpu_kernel_params: "rd.driver.blacklist=nouveau nvidia-drm.modeset=1 nvidia.NVreg_EnableGpuFirmware=0"
        gpu_network_mtu: 9000
        gpu_category_name: a100_gpu
        gpu_category_notes: "NVIDIA A100 GPU nodes with CUDA 12"
```

## License

GPL-3.0-or-later

## Author

NVIDIA Corporation
