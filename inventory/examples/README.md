# Example Inventories

This directory contains example inventory files for deploying RHEL+Slurm and OpenShift clusters on BCM.

## Directory Structure

```
inventory/examples/
├── rhel_cluster/
│   └── hosts.yml              # RHEL+Slurm cluster example
├── openshift_cluster/
│   └── hosts.yml              # OpenShift cluster example
└── README.md                  # This file
```

## RHEL+Slurm Cluster Example

The `rhel_cluster/hosts.yml` file demonstrates:

- Multiple node roles (login, compute-cpu, compute-gpu, storage)
- Custom package lists per role
- Post-installation scripts for NFS mounts
- GPU-specific configuration (nouveau blacklisting)
- 7 nodes across 3 racks

### Quick Start

1. Copy the example and customize:
   ```bash
   cp inventory/examples/rhel_cluster/hosts.yml inventory/my_hpc_cluster.yml
   ```

2. Edit the file to match your environment:
   - Update `ansible_host`, `ansible_user`, `ansible_password`
   - Set `rhel_iso_path` to your RHEL ISO location
   - Modify `cluster_name` as needed
   - Adjust node MAC addresses and IP addresses
   - Customize `node_roles` packages and post-scripts
   - Add/remove nodes in `cluster_nodes`

3. Deploy the cluster:
   ```bash
   ansible-playbook -i inventory/my_hpc_cluster.yml playbooks/deploy_rhel_cluster.yml
   ```

## OpenShift Cluster Example

The `openshift_cluster/hosts.yml` file demonstrates:

- 3 master nodes
- 2 initial worker nodes
- Examples for expanding with additional workers
- Infrastructure nodes (commented out)
- MAC-based Ignition file configuration

### Quick Start

1. Generate OpenShift agent ISO:
   ```bash
   # Create install-config.yaml and agent-config.yaml
   openshift-install agent create image
   ```

2. Copy the example and customize:
   ```bash
   cp inventory/examples/openshift_cluster/hosts.yml inventory/my_openshift_cluster.yml
   ```

3. Edit the file to match your environment:
   - Update `ansible_host`, `ansible_user`, `ansible_password`
   - Set `openshift_iso_path` to your agent ISO location
   - Modify `cluster_name` as needed
   - Adjust node MAC addresses and IP addresses
   - **IMPORTANT**: Update `ignition_file` paths for each node
   - Add/remove nodes as needed

4. Deploy the cluster:
   ```bash
   ansible-playbook -i inventory/my_openshift_cluster.yml playbooks/deploy_openshift_cluster.yml
   ```

## Common Customization Tasks

### Changing the BCM Head Node

Update the `ansible_host` and credentials:

```yaml
bcm-headnode:
  ansible_host: YOUR_BCM_IP
  ansible_user: root
  ansible_password: YOUR_PASSWORD
  # Or use SSH key:
  # ansible_ssh_private_key_file: ~/.ssh/id_rsa
```

### Adding More Node Roles

For RHEL clusters, add to `node_roles`:

```yaml
node_roles:
  - name: my-custom-role
    category: "slurm-{{ cluster_name }}-my-custom-role"
    packages:
      - "@^minimal-environment"
      - custom-package-1
      - custom-package-2
    post_script: |
      # Custom post-installation tasks
      echo "Custom configuration"
```

For OpenShift clusters, add to `node_roles`:

```yaml
node_roles:
  - name: infra
    category: "openshift-{{ openshift_version | replace('.', '') }}-{{ cluster_name }}-infra"
```

### Modifying Network Configuration

Update these variables for RHEL clusters:

```yaml
network_bootproto: static  # or dhcp
network_device: ens3       # or link for first available
network_onboot: true
```

### Changing Disk Configuration

Update these variables for RHEL clusters:

```yaml
disk_device: sda
disk_clearpart: true
disk_autopart_type: lvm    # or plain, btrfs, etc.
```

## Expanding Existing Clusters

### RHEL Cluster Expansion

1. Open your inventory file
2. Add new nodes to `cluster_nodes` list
3. Use existing `category` values for the node role
4. Re-run the deployment playbook

### OpenShift Cluster Expansion

1. Generate Ignition for new worker:
   ```bash
   oc extract -n openshift-machine-api secret/worker-user-data \
     --keys=userData --to=/root/ignition/worker-new.ign
   ```

2. Add node to `cluster_nodes`:
   ```yaml
   - name: worker-5
     mac: "52:54:00:EE:FF:05"
     ip: "10.141.160.65"
     role: worker
     ignition_file: /root/ignition/worker-new.ign
   ```

3. Re-run the deployment playbook
4. Same category is reused - only Ignition URL differs

## Variable Reference

### Common Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `cluster_name` | Cluster identifier | `hpc01`, `prod` |
| `ansible_host` | BCM head node IP | `192.168.122.163` |
| `ansible_user` | SSH user | `root` |
| `ansible_password` | SSH password | `redhat` |

### RHEL-Specific Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `rhel_version` | RHEL version | `9.6` |
| `rhel_iso_path` | Path to RHEL ISO | Required |
| `root_password` | Root password for nodes | `changeme123` |
| `install_mode` | BCM install mode | `AUTO` |

### OpenShift-Specific Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `openshift_version` | OpenShift version | `4.16` |
| `openshift_iso_path` | Path to agent ISO | Required |
| `install_device` | CoreOS install device | `/dev/sda` |
| `install_mode` | BCM install mode | `NEVER` |

## Testing

Both examples include basic validation. To test without deploying:

```bash
# Syntax check
ansible-playbook -i inventory/examples/rhel_cluster/hosts.yml \
  playbooks/deploy_rhel_cluster.yml --syntax-check

# Dry-run (check mode)
ansible-playbook -i inventory/examples/rhel_cluster/hosts.yml \
  playbooks/deploy_rhel_cluster.yml --check
```

## Troubleshooting

### ISO Not Found

**Error**: `RHEL ISO not found at /path/to/iso`

**Solution**: Verify the ISO path and ensure it's accessible on the BCM head node

### Ignition File Not Found

**Error**: `Ignition file not found`

**Solution**: Verify `ignition_file` paths in inventory match actual file locations

### Connection Refused

**Error**: `Failed to connect to 192.168.122.163`

**Solution**: Check BCM head node IP, SSH credentials, and network connectivity

### Category Already Exists

**Warning**: Category already exists

**Solution**: This is normal if re-running the playbook. Existing categories will be updated.

## Next Steps

After deployment:

1. Verify deployment: Check `/root/deployment-summary-*.md` on BCM head node
2. Monitor nodes: `cmsh -c 'device; status'`
3. Power on nodes: See deployment summary for commands
4. Complete post-deployment configuration (Slurm, storage, etc.)
