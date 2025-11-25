# Documentation

This directory contains architecture and reference documentation for the NVIDIA BCM Ansible collection.

## Documentation Index

### Usage Documentation
For playbook usage, workflows, and examples, see:
- **[playbooks/README.md](../playbooks/README.md)** - Main usage guide with playbook examples and workflows

### Architecture & Concepts

| Document | Purpose | Audience |
|----------|---------|----------|
| [BCM_PARTITIONS.md](BCM_PARTITIONS.md) | BCM partition strategy and when to use multiple partitions | Deployment planning |
| [BCM_CATEGORY_NAMING_STRATEGY.md](BCM_CATEGORY_NAMING_STRATEGY.md) | Category naming conventions (underscores for Ansible compatibility) | Implementation |
| [DNS_ARCHITECTURE.md](DNS_ARCHITECTURE.md) | DNS setup for OpenShift clusters on BCM | OpenShift deployment |

### BCM Reference

| Document | Purpose | Audience |
|----------|---------|----------|
| [BCM_PXE_FILESYSTEM_STRUCTURE.md](BCM_PXE_FILESYSTEM_STRUCTURE.md) | BCM's /tftpboot filesystem layout and structure | Understanding PXE internals |
| [BCM_PXE_INSTALLER_IMAGES.md](BCM_PXE_INSTALLER_IMAGES.md) | Difference between BCM software images vs installer images | PXE boot concepts |

### Setup Guides

| Document | Purpose | Audience |
|----------|---------|----------|
| [SUSHY_EMULATOR_SETUP.md](SUSHY_EMULATOR_SETUP.md) | Setting up Redfish emulator for VM management | Test environments |

## Quick Links

### I want to...

**Deploy a new OpenShift cluster**
→ See [playbooks/README.md](../playbooks/README.md#deploy_openshift_clusteryml)

**Join an existing OpenShift cluster to BCM**
→ See [playbooks/README.md](../playbooks/README.md#join_openshift_clusteryml)

**Deploy BCM agent to existing cluster**
→ See [playbooks/README.md](../playbooks/README.md#deploy_bcm_agentyml)

**Understand BCM partitions**
→ See [BCM_PARTITIONS.md](BCM_PARTITIONS.md)

**Set up DNS for OpenShift**
→ See [DNS_ARCHITECTURE.md](DNS_ARCHITECTURE.md)

**Understand category naming**
→ See [BCM_CATEGORY_NAMING_STRATEGY.md](BCM_CATEGORY_NAMING_STRATEGY.md)

**Set up Redfish emulator for testing**
→ See [SUSHY_EMULATOR_SETUP.md](SUSHY_EMULATOR_SETUP.md)

## Documentation Structure

```
docs/
├── README.md (this file)                    # Documentation index
├── BCM_PARTITIONS.md                        # Partition strategy
├── BCM_CATEGORY_NAMING_STRATEGY.md          # Naming conventions
├── DNS_ARCHITECTURE.md                      # DNS architecture
├── BCM_PXE_FILESYSTEM_STRUCTURE.md          # BCM filesystem reference
├── BCM_PXE_INSTALLER_IMAGES.md              # Image types explained
└── SUSHY_EMULATOR_SETUP.md                  # Redfish emulator setup
```

## Contributing

When adding new documentation:

1. **Check if it belongs in playbooks/README.md** - Usage instructions should go there
2. **Keep docs focused** - One topic per document
3. **Use examples** - Show, don't just tell
4. **Update this README** - Add new docs to the index
5. **Keep it current** - Remove outdated docs, don't orphan them

## Archive

Previously, this directory contained 17+ documents. Many were:
- References to deprecated custom modules (now use official `brightcomputing.bcm110` collection)
- Duplicative of playbook inline documentation
- Outdated manual processes (now automated)

We've consolidated to 6 focused documents covering architecture, concepts, and reference material.
