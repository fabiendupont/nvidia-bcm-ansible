# Changelog

All notable changes to the NVIDIA BCM Ansible Collection will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-01-16

### Added

#### Modules
- **bcm_user**: User management module
  - Query user information (UID, home, shell, email, groups)
  - Update user properties (home directory, shell, email, notes)
  - Remove users with proper validation
  - Idempotent operations with check mode support

- **bcm_group**: Group management module
  - Query group information (members, notes)
  - Update group properties
  - Remove groups with safety checks
  - Full integration with BCM user system

- **bcm_info**: Cluster facts gathering module
  - Gather comprehensive BCM cluster information
  - Flexible subset selection (counts, devices, users, networks)
  - Entity counts for all BCM object types
  - Summary information for devices, users, networks
  - Useful for inventory, reporting, and monitoring

- **bcm_power**: Power management module
  - Query power status of nodes
  - Power on/off operations
  - Hard reset (power cycle) capability
  - IPMI/Redfish integration
  - Conditional power state changes

#### Example Playbooks
- **user_management_example.yml**: User management workflows
- **group_management_example.yml**: Group management workflows
- **cluster_info_example.yml**: Cluster information gathering
- **power_management_example.yml**: Power management operations

### Updated
- **README.md**: Added documentation for new modules
- **bcm_common.py**: Added get_user() and get_group() helper methods
- Collection now includes 10 modules total

## [1.0.0] - 2025-01-15

### Added

#### Inventory Plugin
- **bcm_inventory**: Dynamic inventory plugin for auto-discovering BCM nodes
  - Groups nodes by device type
  - Provides comprehensive host variables
  - Certificate-based authentication
  - Customizable grouping with keyed_groups

#### Modules
- **bcm_node**: Manage cluster nodes
  - Query node information
  - Update node properties (hostname, MAC, rack, position)
  - Remove nodes with safety checks
  - Idempotent operations
  - Check mode support

- **bcm_category**: Manage node categories
  - Query category information
  - Update category properties
  - Remove categories with protection for 'default'
  - Prevents deletion of categories in use

- **bcm_software_image**: Manage software images
  - Query software image details
  - Update kernel parameters
  - Remove images with usage validation
  - Automatic dependency checking

- **bcm_network**: Manage cluster networks
  - Query network configuration
  - Update MTU and domain settings
  - Remove custom networks
  - Protection for system networks

- **bcm_overlay**: Query configuration overlays
  - View overlay assignments
  - Check category and role associations
  - Query-only (create/update/delete not yet implemented)

#### Roles
- **gpu_cluster_config**: Configure clusters for GPU workloads
  - Optimize kernel parameters for NVIDIA drivers
  - Configure network MTU for GPU Direct RDMA
  - Update category documentation

- **cluster_audit**: Generate cluster audit reports
  - Comprehensive configuration reporting
  - Saves reports to disk
  - Customizable audit scope

- **network_optimization**: Optimize network for HPC
  - Enable jumbo frames
  - Configure domain names
  - Performance recommendations

#### Documentation
- Comprehensive README with installation and usage
- QUICKSTART guide for new users
- INSTALL guide with detailed prerequisites
- DEVELOPMENT guide for contributors
- CONTRIBUTING guidelines
- Module documentation with examples
- Role documentation with use cases

### Changed
- Updated all references from Rocky Linux to Red Hat Enterprise Linux 9
- Standardized module patterns across all implementations
- Improved error handling and user messages

### Technical Details
- **Platform**: Red Hat Enterprise Linux 9
- **BCM Version**: 11.0+
- **Ansible**: 2.14+
- **Python**: 3.6+
- **Authentication**: Certificate-based (no passwords required)

### Known Limitations
- Entity creation not supported (must use cmsh/GUI)
- bcm_overlay is query-only
- Limited property updates (only basic attributes)

### Dependencies
- cmdaemon-pythoncm (from BCM repository)
- python3-lxml
- python3-passlib
- python3-tabulate
- python3-pyOpenSSL

---

## Future Releases

### Planned for 1.1.0
- Add bcm_user module for user management
- Add bcm_group module for group management
- Add bcm_info module for facts gathering
- Add bcm_power module for power management
- Implement entity creation in existing modules
- Add comprehensive unit tests
- Add integration test suite

### Planned for 1.2.0
- Add bcm_provision module for node provisioning
- Add bcm_job module for workload management
- Enhanced dynamic inventory with caching
- Batch operation support
- Performance optimizations

### Planned for 2.0.0
- Full CRUD support for all modules
- Advanced workflow automation
- Monitoring and health check modules
- Backup and restore capabilities
- Integration with Ansible Automation Platform

---

[1.0.0]: https://github.com/nvidia/ansible-bcm/releases/tag/v1.0.0
