# Role: convert_to_litenode

Convert PhysicalNode nodes to LiteNode after OS installation completes.

## Purpose

Converts nodes from PhysicalNode (PXE-provisioned) to LiteNode (agent-managed) registration in BCM. This enables PXE boot during installation, then switches to persistent agent-based management post-install. Required for BCM agent deployment.

## Requirements

- brightcomputing.bcm110 collection
- Nodes must be accessible via SSH
- OS installation must be complete

## Required Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `cluster_nodes` | Yes | List of nodes with `name`, `ip`, `mac`, `ansible_user` |

## Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `ssh_wait_timeout` | `300` | Seconds to wait for SSH accessibility |
| `install_complete_file` | None | File path to check for installation completion |
| `verify_service` | None | Service name to verify is running |
| `verify_openshift` | `false` | Perform OpenShift cluster readiness check |
| `openshift_version` | None | Required if `verify_openshift=true` |
| `cluster_name` | None | Required if `verify_openshift=true` |

## Workflow

1. Wait for nodes to be SSH accessible
2. Optionally verify installation completion (file check or service check)
3. Optionally verify OpenShift cluster readiness (if OpenShift deployment)
4. Delete existing PhysicalNode entries from BCM
5. Create new LiteNode entries with same MAC/IP
6. Wait for nodes to reboot and reconnect

## Example Usage

```yaml
# Basic conversion
- include_role:
    name: fabiendupont.bcm.convert_to_litenode
  vars:
    cluster_nodes: "{{ cluster_nodes }}"
    ssh_wait_timeout: 600

# OpenShift with cluster verification
- include_role:
    name: fabiendupont.bcm.convert_to_litenode
  vars:
    cluster_nodes: "{{ cluster_nodes }}"
    verify_openshift: true
    openshift_version: "1.33.5"
    cluster_name: "test-sno"

# RHEL with file-based verification
- include_role:
    name: fabiendupont.bcm.convert_to_litenode
  vars:
    install_complete_file: "/root/install-complete.txt"
```

## Dependencies

- brightcomputing.bcm110 collection

## Important Notes

- **Destructive operation**: Deletes PhysicalNode and creates LiteNode
- **Causes reboot**: Nodes will reboot after conversion
- **One-way**: Converting back to PhysicalNode requires manual intervention
- **Prerequisites**: Nodes must be fully installed and accessible via SSH
