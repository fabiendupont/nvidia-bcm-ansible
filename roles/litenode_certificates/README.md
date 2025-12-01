# Role: litenode_certificates

Generate per-node litenode certificates for BCM agent authentication.

## Purpose

Creates litenode certificates for each cluster node using BCM's certificate authority. Supports multiple directory structures to accommodate different deployment patterns (OpenShift Kubernetes secrets, RHEL kickstart downloads, manual node deployment).

## Requirements

- BCM head node with certificate authority configured
- cmsh command available

## Required Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `cluster_nodes` | Yes | List of nodes with `name` attribute (and `mac` if using per_mac structure) |

## Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `litenode_certs_dir` | `/tmp/litenode-certs` | Output directory |
| `litenode_cert_dir_structure` | `flat` | Directory structure: `flat`, `per_node`, or `per_mac` |
| `litenode_cert_bits` | `2048` | Certificate key size |
| `litenode_cert_org` | `NVIDIA Inc` | Certificate organization |
| `litenode_cert_validity_days` | `36500` | Certificate validity (~100 years) |

## Directory Structures

- **flat**: All certs in base dir - `{dir}/{node}.pem`, `{dir}/{node}.key`
  Use case: OpenShift (Kubernetes secrets)

- **per_node**: Each node gets subdir - `{dir}/{node}/cert.pem`, `{dir}/{node}/cert.key`
  Use case: RHEL manual node join

- **per_mac**: Organized by MAC - `{dir}/{mac}/cert.pem`, `{dir}/{mac}/cert.key`
  Use case: RHEL kickstart (downloads by MAC address)

## Example Usage

```yaml
# OpenShift deployment (flat structure)
- include_role:
    name: fabiendupont.bcm.litenode_certificates
  vars:
    cluster_nodes: "{{ cluster_nodes }}"
    litenode_certs_dir: "/openshift/clusters/{{ cluster_name }}/node_certs"
    litenode_cert_dir_structure: "flat"

# RHEL kickstart (per-MAC structure)
- include_role:
    name: fabiendupont.bcm.litenode_certificates
  vars:
    litenode_certs_dir: "/tftpboot/bcm-agent/certs"
    litenode_cert_dir_structure: "per_mac"
```

## Important Notes

- **Bootstrap certificates do NOT work** for LiteNode authentication
- Each LiteNode requires its own certificate with `profile=litenode`
- Certificates are automatically approved by BCM
- Generation is idempotent (uses `creates` parameter)
