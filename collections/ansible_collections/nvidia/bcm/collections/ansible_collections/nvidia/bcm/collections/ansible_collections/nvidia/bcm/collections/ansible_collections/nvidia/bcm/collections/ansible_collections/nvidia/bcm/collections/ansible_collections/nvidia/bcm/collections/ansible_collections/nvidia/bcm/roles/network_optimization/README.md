# Network Optimization Role

Optimize NVIDIA Base Command Manager network configuration for HPC and GPU workloads.

## Description

This role optimizes BCM network settings by:
- Enabling jumbo frames (MTU 9000) for improved throughput
- Configuring appropriate domain names
- Providing performance recommendations
- Validating network configuration changes

## Requirements

- NVIDIA BCM 11.0+
- nvidia.bcm collection installed
- Network infrastructure supporting desired MTU

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `network_name` | `internalnet` | Network to optimize |
| `network_mtu` | `9000` | Target MTU (jumbo frames) |
| `network_domain` | `cluster.local` | Domain name for the network |
| `enable_jumbo_frames` | `true` | Whether to enable jumbo frames |
| `optimize_for_hpc` | `true` | Apply HPC-specific optimizations |

## Dependencies

None

## Example Playbook

```yaml
---
- name: Optimize Cluster Network
  hosts: localhost
  gather_facts: false

  roles:
    - nvidia.bcm.network_optimization
```

## Example with Custom MTU

```yaml
---
- name: Optimize Network with Custom Settings
  hosts: localhost
  gather_facts: false

  roles:
    - role: nvidia.bcm.network_optimization
      vars:
        network_name: internalnet
        network_mtu: 9000
        network_domain: hpc.example.com
```

## Example for Multiple Networks

```yaml
---
- name: Optimize Multiple Networks
  hosts: localhost
  gather_facts: false

  tasks:
    - name: Optimize internal network
      include_role:
        name: nvidia.bcm.network_optimization
      vars:
        network_name: internalnet
        network_mtu: 9000

    - name: Optimize external network
      include_role:
        name: nvidia.bcm.network_optimization
      vars:
        network_name: externalnet
        network_mtu: 1500  # Standard MTU for external
        enable_jumbo_frames: false
```

## Performance Benefits

### Jumbo Frames (MTU 9000)

Benefits:
- **Reduced CPU overhead**: Fewer packets to process
- **Improved throughput**: Better bandwidth utilization
- **Lower latency**: Fewer packet processing cycles
- **Better for GPU workloads**: Optimal for GPU Direct RDMA

Typical performance improvements:
- **Network throughput**: 10-30% increase
- **CPU utilization**: 5-15% reduction
- **MPI performance**: 5-20% improvement for large messages

### Prerequisites

Ensure your network infrastructure supports jumbo frames:
1. All switches must support MTU 9000 or higher
2. All network interfaces must be configured consistently
3. End-to-end path must support the MTU

## Verification

After running the role, verify the changes:

```bash
# On compute nodes
ip link show | grep mtu

# Expected output should show MTU 9000
```

## Troubleshooting

### MTU Mismatch Issues

If you experience connectivity issues after enabling jumbo frames:

1. Check switch configuration
2. Verify all nodes have consistent MTU
3. Test with ping:
   ```bash
   ping -M do -s 8972 node001  # 8972 + 28 bytes overhead = 9000
   ```

### Reverting Changes

To revert to standard MTU:

```yaml
- role: nvidia.bcm.network_optimization
  vars:
    network_mtu: 1500
    enable_jumbo_frames: false
```

## License

GPL-3.0-or-later

## Author

NVIDIA Corporation
