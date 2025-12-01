# Role: register_bcm_nodes

Register cluster nodes in BCM with automatic or provided category assignment.

## Purpose

Unified node registration supporting two modes: automatic category generation (for OpenShift) and provided categories (for RHEL). Eliminates code duplication across deployment types.

## Requirements

- brightcomputing.bcm110 collection
- BCM head node access

## Required Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `cluster_nodes` | Yes | List of nodes with `name`, `mac`, `ip` attributes |

## Mode-Specific Requirements

**Auto mode** (bcm_node_category_mode=auto):
- `cluster_name` - Required
- `bcm_node_category_prefix` - Required (e.g., "openshift_133")
- Nodes must have `role` attribute

**Provided mode** (bcm_node_category_mode=provided):
- Nodes must have `category` attribute

## Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `bcm_node_category_mode` | `provided` | Category mode: `auto` or `provided` |
| `bcm_node_category_prefix` | `""` | Prefix for auto-generated categories |
| `bcm_node_network` | `internalnet` | BCM network name |
| `bcm_node_partition` | `base` | BCM partition |
| `bcm_node_provisioning_interface` | `BOOTIF` | Provisioning interface name |

## Category Generation (Auto Mode)

Format: `{prefix}_{cluster_name}_{role}`

Example: `openshift_133_test_sno_master`

## Example Usage

```yaml
# OpenShift (auto mode)
- include_role:
    name: fabiendupont.bcm.register_bcm_nodes
  vars:
    bcm_node_category_mode: "auto"
    bcm_node_category_prefix: "openshift_{{ openshift_version | replace('.', '') }}"

# RHEL (provided mode)
- include_role:
    name: fabiendupont.bcm.register_bcm_nodes
  vars:
    bcm_node_category_mode: "provided"
    # Categories specified in cluster_nodes data structure
```

## Dependencies

- brightcomputing.bcm110 collection

## Notes

- Builds category mapping as facts before registration
- Single physical_node registration task (uses facts)
- Validates required fields based on mode
