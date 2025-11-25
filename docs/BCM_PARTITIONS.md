# BCM Partitions - Design Considerations

## What are BCM Partitions?

A **partition** in Bright Cluster Manager (BCM) is a logical segmentation of cluster resources that creates independent virtual clusters within a single physical cluster infrastructure.

## Partition Characteristics

Each partition provides:

- **Isolated node groups** - Physically separate sets of compute nodes
- **Independent software images** - Different OS versions, configurations, and software stacks
- **Administrative boundaries** - Separate management policies and permissions
- **Resource isolation** - Quota management and scheduling policies
- **Network segmentation** - Optional network isolation between partitions

## Current Implementation

**Default Partition:** `base`

All nodes (both OpenShift and RHEL test clusters) are registered to the `base` partition.

### Why Use a Single Partition?

For testing and development environments:

1. **Ephemeral workloads** - Test clusters are temporary (deploy, test, cleanup)
2. **Simplified management** - No partition overhead for short-lived resources
3. **No isolation requirements** - Testing doesn't require security boundaries
4. **Automation focus** - Goal is testing deployment automation, not multi-tenancy

### Categories vs Partitions

**Categories are sufficient for:**
- Grouping nodes by cluster type (OpenShift vs RHEL)
- Grouping nodes by version (OpenShift 4.20 vs 4.21)
- Grouping nodes by role (master vs worker)
- Software image assignment
- Configuration management

**Current category naming:**
- Format: `{type}_{version}_{cluster_name}_{role}`
- Example: `openshift_420_test_ocp_master`
- Uses underscores (required for valid Ansible group names)

## When to Use Multiple Partitions

Consider creating separate partitions for:

### Production Environments

```yaml
partitions:
  - name: prod-openshift
    purpose: Production OpenShift clusters
    isolation: High

  - name: prod-hpc
    purpose: Production HPC workloads (RHEL)
    isolation: High

  - name: dev-testing
    purpose: Development and testing
    isolation: Low
```

### Multi-Tenancy

- Different teams/departments requiring complete isolation
- Customer-specific environments in managed service scenarios
- Compliance requirements mandating separation

### Different SLAs

- Critical workloads requiring guaranteed resources
- Best-effort workloads that can tolerate disruption
- Different backup/recovery policies

### Security Requirements

- Regulatory compliance (HIPAA, PCI-DSS, etc.)
- Different security zones (DMZ, internal, restricted)
- Separation of sensitive workloads

## Implementation Considerations

### Creating a Partition

```bash
# Via cmsh
cmsh -c "partition; add prod-openshift; commit"

# Via Ansible
- name: Create production OpenShift partition
  brightcomputing.bcm110.partition:
    name: prod-openshift
    state: present
```

### Registering Nodes to a Partition

```yaml
- name: Register nodes to specific partition
  brightcomputing.bcm110.physical_node:
    hostname: "{{ item.name }}"
    partition: "prod-openshift"  # Specify partition
    category: "{{ item.category }}"
    # ... other parameters
```

### Best Practices

1. **Plan partition strategy early** - Difficult to reorganize later
2. **Document partition purpose** - Clear naming and documentation
3. **Consistent naming** - Follow organization standards
4. **Minimal partitions** - Only create when truly needed
5. **Monitor resource usage** - Ensure partitions aren't resource-starved

## Migration Path

If you need to move from single partition to multiple partitions:

1. **Create new partition(s)** using `brightcomputing.bcm110.partition`
2. **Update node registration** to specify target partition
3. **Migrate existing nodes** (may require re-registration)
4. **Update cleanup playbooks** to handle partition-specific cleanup
5. **Update inventory files** to specify partition per cluster

### Example: Production Partitions

```yaml
# inventory/production.yml
all:
  children:
    bcm_headnode:
      vars:
        # OpenShift production
        openshift_partition: "prod-openshift"

        # RHEL HPC production
        rhel_partition: "prod-hpc"

        node_roles:
          - name: master
            category: "openshift_420_prod_master"
            partition: "{{ openshift_partition }}"
```

## References

- BCM Partition Documentation: BCM Administrator Manual Chapter 7
- Multi-tenancy Guide: BCM Advanced Topics
- Ansible Collection: `brightcomputing.bcm110.partition` module

## Notes

- **Current status:** Using `base` partition for all test clusters
- **Future consideration:** Create separate partitions when moving to production
- **Decision driver:** Complexity vs. isolation requirements
