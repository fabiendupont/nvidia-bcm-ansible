# BCM Ansible Playbook Examples

This directory contains example playbooks demonstrating how to use the NVIDIA BCM Ansible Collection.

## Available Playbooks

### kickstart-deployment.yml

**Purpose**: Deploy RHEL/Rocky Linux using Kickstart + iPXE with BCM category-based PXE boot configuration.

**What it does**:
1. Creates BCM categories for different OS versions
2. Generates kickstart configuration files
3. Creates iPXE boot scripts
4. Configures category-specific PXE boot menus
5. Assigns nodes to appropriate categories

**Key Features**:
- ✅ Uses only BCM Ansible modules for BCM configuration
- ✅ Category-based PXE boot (no per-node pxelabel needed)
- ✅ Supports multiple OS versions simultaneously
- ✅ Fully automated deployment workflow
- ✅ Works with GenericDevice nodes

**Quick Start**:
```bash
# Edit variables in the playbook (mirror URLs, node names, etc.)
vim kickstart-deployment.yml

# Deploy everything
ansible-playbook kickstart-deployment.yml

# Verify deployment
ansible-playbook kickstart-deployment.yml --tags verify
```

**Architecture**:
```
Node → Assigned to Category → Category PXE Config → iPXE Script → Kickstart → OS Install
```

**Example**: Deploy RHEL 9.6 to node001 and node002:
1. Creates category `rhel96-kickstart`
2. Creates PXE config `/tftpboot/pxelinux.cfg/category.rhel96-kickstart`
3. PXE config loads iPXE script `/tftpboot/ipxe/rhel96-kickstart.ipxe`
4. iPXE script loads kernel and kickstart from mirror
5. Kickstart installs RHEL 9.6 automatically

**Prerequisites**:
- BCM head node with TFTP/HTTP services
- Access to RHEL/Rocky Linux mirrors (remote or local)
- Nodes must be able to PXE boot

**Customization Points**:
- `vars.deployments`: Define OS versions and node assignments
- `vars.os_mirror_url`: Set to local or remote mirror
- Kickstart templates: Customize package selection, partitioning, etc.
- iPXE scripts: Add custom boot parameters
- PXE menus: Customize boot options and timeouts

## Directory Structure

```
playbooks/
├── README.md                      # This file
├── kickstart-deployment.yml       # Kickstart deployment example
└── (future playbooks)
    ├── bcm-cluster-setup.yml      # Full cluster initialization
    ├── network-configuration.yml  # Network management
    └── node-provisioning.yml      # BCM native provisioning
```

## Common Tasks

### Deploy Single OS Version
```bash
# RHEL 9.6 only
ansible-playbook kickstart-deployment.yml --tags rhel96

# Rocky 9.5 only
ansible-playbook kickstart-deployment.yml --tags rocky95
```

### Update Configuration Files
```bash
# Update kickstart files only
ansible-playbook kickstart-deployment.yml --tags kickstart

# Update iPXE scripts only
ansible-playbook kickstart-deployment.yml --tags ipxe

# Update PXE configs only
ansible-playbook kickstart-deployment.yml --tags pxe
```

### Manage BCM Configuration
```bash
# Update BCM categories and node assignments
ansible-playbook kickstart-deployment.yml --tags bcm
```

## Integration with BCM Modules

The playbooks demonstrate how to use BCM Ansible modules alongside standard Ansible modules:

**BCM Modules Used**:
- `nvidia.bcm.bcm_category`: Create and manage categories
- `nvidia.bcm.bcm_node`: Assign nodes to categories
- `nvidia.bcm.bcm_network`: (future) Network configuration
- `nvidia.bcm.bcm_software_image`: (future) Manage OS images

**Standard Ansible Modules Used**:
- `ansible.builtin.file`: Create directories
- `ansible.builtin.copy`: Deploy kickstart and iPXE files
- `ansible.builtin.debug`: Display information

## Troubleshooting

### Nodes not PXE booting
```bash
# Check category assignment
ansible-playbook kickstart-deployment.yml --tags verify

# Check PXE config exists
ls -la /tftpboot/pxelinux.cfg/category.*

# Verify TFTP service
systemctl status tftpd.service
```

### Kickstart installation fails
```bash
# Check kickstart syntax
ksvalidator /var/www/html/ks/rhel96-minimal.cfg

# Verify mirror accessibility
curl -I http://mirror.rockylinux.org/pub/rocky/9.5/BaseOS/x86_64/os/images/pxeboot/vmlinuz

# Check kickstart file accessibility
curl http://10.141.255.254:8080/ks/rhel96-minimal.cfg
```

### iPXE boot fails
```bash
# Verify iPXE script syntax
cat /tftpboot/ipxe/rhel96-kickstart.ipxe

# Check undionly.kpxe exists
ls -la /tftpboot/undionly.kpxe

# Test iPXE script manually (from node console):
# iPXE> dhcp
# iPXE> chain tftp://10.141.255.254/ipxe/rhel96-kickstart.ipxe
```

## Contributing

When adding new playbooks:
1. Follow the existing structure and documentation style
2. Use BCM modules for all BCM-related configuration
3. Include comprehensive comments and examples
4. Add tags for granular execution
5. Include verification tasks
6. Update this README

## References

- [BCM Module Documentation](../docs/)
- [Kickstart Documentation](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/9/html/performing_an_advanced_rhel_9_installation/kickstart-commands-and-options-reference_installing-rhel-as-an-experienced-user)
- [iPXE Documentation](https://ipxe.org/docs)
- [Ansible Best Practices](https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html)
