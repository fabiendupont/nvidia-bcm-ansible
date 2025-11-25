# DNS Setup Role

This role automatically configures DNS on the BCM head node for OpenShift clusters.

## Purpose

OpenShift clusters require DNS resolution for internal cluster domains:
- `api.<cluster-name>.<domain>` - Kubernetes API server
- `api-int.<cluster-name>.<domain>` - Internal API server
- `*.apps.<cluster-name>.<domain>` - Application ingress/routes

Public DNS servers (like 8.8.8.8) cannot resolve these internal domains, so the BCM head node must provide DNS services for the cluster.

## What It Does

1. **Creates DNS zone file** from template with cluster-specific records
2. **Configures BIND** to serve the zone
3. **Validates** zone file and BIND configuration
4. **Reloads named** service to activate changes
5. **Verifies** DNS resolution is working

## Zone File Structure

The generated zone file includes:
- **NS record**: BCM head node as nameserver
- **API endpoints**: Point to rendezvous host (first master node)
- **Apps wildcard**: Round-robin to all master nodes
- **Node records**: A records for each cluster node

## Usage

This role is automatically included in the `deploy_openshift_cluster.yml` playbook during Phase 1 (PXE Infrastructure Setup).

### Manual Usage

```yaml
- hosts: bcm_headnode
  roles:
    - role: dns_setup
      vars:
        dns_domain: "test.local"
        cluster_name: "test-ocp"
        cluster_nodes:
          - name: ocp-master-0
            ip: 10.141.160.50
            mac: "52:54:00:01:00:01"
            role: master
          - name: ocp-master-1
            ip: 10.141.160.51
            mac: "52:54:00:01:00:02"
            role: master
```

## Variables

See `defaults/main.yml` for all configurable variables.

### Required Variables (from inventory)
- `dns_domain` / `base_domain`: DNS domain for the cluster
- `cluster_name`: Name of the OpenShift cluster
- `cluster_nodes`: List of cluster nodes with IP addresses

### Optional Variables
- `bcm_internal_ip`: BCM head node internal IP (default: 10.141.255.254)
- `dns_zone_dir`: Zone file directory (default: /var/named)
- `dns_include_file`: BIND include file (default: /etc/named.conf.include)

## Node DNS Configuration

After nodes boot, they need to be configured to use the BCM head node as their DNS server. This can be done:

1. **During deployment** (recommended): Include the `configure_nodes.yml` tasks after nodes are booted
2. **Via DHCP**: Configure BCM DHCP to provide the BCM head node as DNS server
3. **Static configuration**: Set DNS in agent-config.yaml when generating PXE files

## Integration with OpenShift Deployment

The DNS setup role runs during Phase 1 of the deployment:

```
Phase 1: PXE Infrastructure Setup
  ├── Generate PXE boot files
  ├── Setup DNS for cluster domain  <-- THIS ROLE
  ├── Setup PXE infrastructure
  └── Register nodes in BCM
```

This ensures DNS is ready before the assisted-service starts validating cluster requirements.

## Troubleshooting

### DNS not resolving
```bash
# Check zone file
named-checkzone test.local /var/named/test.local.zone

# Check BIND configuration
named-checkconf

# Test resolution from BCM head node
dig @10.141.255.254 api.test-ocp.test.local

# Check named status
systemctl status named
journalctl -u named -f
```

### Nodes not using BCM DNS
```bash
# Check DNS config on node
ssh core@ocp-master-0 'cat /etc/resolv.conf'

# Test DNS from node
ssh core@ocp-master-0 'dig +short api.test-ocp.test.local'

# Update DNS manually
ssh core@ocp-master-0 'sudo nmcli con mod enp1s0 ipv4.dns "10.141.255.254" && sudo nmcli con up enp1s0'
```

## Files Generated

- `/var/named/<domain>.zone` - DNS zone file for the cluster domain
- `/etc/named.conf.include` - BIND include file with zone configuration

## Dependencies

- BIND (named) service running on BCM head node
- SSH access to BCM head node
- Ansible collections: ansible.builtin
