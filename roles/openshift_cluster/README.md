# OpenShift Cluster Role

This role deploys OpenShift clusters on NVIDIA Base Command Manager (BCM) using PXE boot with Ignition configuration.

## Features

- Create ignition directory structure
- Copy MAC-based Ignition files to BCM
- Create BCM categories for different node roles
- Create symlinks for boot files
- Register nodes in BCM with per-node Ignition URLs
- Support for master, worker, and infra node roles

## Requirements

- Ansible 2.15+
- BCM head node with PXE infrastructure already set up (use `pxe_setup` role first)
- OpenShift agent ISO extracted (use `pxe_setup` role first)
- Ignition files generated (via `openshift-install agent create image`)
- `fabiendupont.bcm` collection modules

## Role Variables

### Required Variables

```yaml
node_roles:
  - name: master                                                    # Role name
    category: openshift-416-prod-master                            # BCM category name
  - name: worker
    category: openshift-416-prod-worker

cluster_nodes:
  - name: master-0                                                  # Node name
    mac: "52:54:00:AA:BB:01"                                       # MAC address
    ip: "10.141.160.50"                                            # IP address
    role: master                                                    # Role (matches node_roles)
    ignition_file: /path/to/master-0.ign                          # Path to Ignition file
```

### Optional Variables

See `defaults/main.yml` for all available variables:

- `cluster_name`: Cluster identifier (default: `prod`)
- `openshift_version`: OpenShift version (default: `4.16`)
- `install_device`: CoreOS install device (default: `/dev/sda`)
- `install_mode`: BCM install mode (default: `NEVER` for CoreOS)

## Dependencies

This role should be used after the `pxe_setup` role has configured the PXE infrastructure and extracted OpenShift boot files.

## Example Playbook

### Basic OpenShift Cluster

```yaml
- hosts: bcm_headnode
  become: true
  vars:
    cluster_name: prod
    openshift_version: "4.16"

    node_roles:
      - name: master
        category: "openshift-{{ openshift_version | replace('.', '') }}-{{ cluster_name }}-master"
      - name: worker
        category: "openshift-{{ openshift_version | replace('.', '') }}-{{ cluster_name }}-worker"

    cluster_nodes:
      # Master nodes
      - name: master-0
        mac: "52:54:00:AA:BB:01"
        ip: "10.141.160.50"
        role: master
        ignition_file: /root/openshift-install/ignition/master-0.ign

      - name: master-1
        mac: "52:54:00:AA:BB:02"
        ip: "10.141.160.51"
        role: master
        ignition_file: /root/openshift-install/ignition/master-1.ign

      # Worker nodes
      - name: worker-0
        mac: "52:54:00:CC:DD:01"
        ip: "10.141.160.60"
        role: worker
        ignition_file: /root/openshift-install/ignition/worker-0.ign

      - name: worker-1
        mac: "52:54:00:CC:DD:02"
        ip: "10.141.160.61"
        role: worker
        ignition_file: /root/openshift-install/ignition/worker-1.ign

  roles:
    - fabiendupont.bcm.openshift_cluster
```

### Multi-Cluster Environment

```yaml
- hosts: bcm_headnode
  become: true
  vars:
    # Production cluster
    prod_cluster:
      name: prod
      version: "4.16"
      roles:
        - name: master
          category: "openshift-416-prod-master"
        - name: worker
          category: "openshift-416-prod-worker"
      nodes:
        - name: prod-master-0
          mac: "52:54:00:AA:BB:01"
          ip: "10.141.160.50"
          role: master
          ignition_file: /root/prod/master-0.ign

    # Test cluster
    test_cluster:
      name: test
      version: "4.16"
      roles:
        - name: master
          category: "openshift-416-test-master"
        - name: worker
          category: "openshift-416-test-worker"
      nodes:
        - name: test-master-0
          mac: "52:54:00:99:88:01"
          ip: "10.141.170.50"
          role: master
          ignition_file: /root/test/master-0.ign

  tasks:
    - name: Deploy production cluster
      ansible.builtin.include_role:
        name: fabiendupont.bcm.openshift_cluster
      vars:
        cluster_name: "{{ prod_cluster.name }}"
        openshift_version: "{{ prod_cluster.version }}"
        node_roles: "{{ prod_cluster.roles }}"
        cluster_nodes: "{{ prod_cluster.nodes }}"

    - name: Deploy test cluster
      ansible.builtin.include_role:
        name: fabiendupont.bcm.openshift_cluster
      vars:
        cluster_name: "{{ test_cluster.name }}"
        openshift_version: "{{ test_cluster.version }}"
        node_roles: "{{ test_cluster.roles }}"
        cluster_nodes: "{{ test_cluster.nodes }}"
```

## Workflow

1. **Directory Creation**: Creates ignition directory structure in `/tftpboot/ignition/openshift-<version>/<cluster>/<role>/`
2. **Ignition Copy**: Copies MAC-based Ignition files to appropriate directories
3. **Symlink Creation**: Links category names to installer boot files
4. **Category Creation**: Registers categories in BCM with CoreOS kernel parameters
5. **Node Registration**: Registers nodes with per-node Ignition URLs in kernel parameters

## File Organization

After running this role:

```
/tftpboot/
├── ignition/
│   └── openshift-4.16/
│       ├── prod/
│       │   ├── master/
│       │   │   ├── 52-54-00-aa-bb-01.ign    # MAC-based Ignition
│       │   │   └── 52-54-00-aa-bb-02.ign
│       │   └── worker/
│       │       ├── 52-54-00-cc-dd-01.ign
│       │       └── 52-54-00-cc-dd-02.ign
│       └── test/
│           └── ...
└── images/
    ├── installer-openshift-4.16/            # Master boot files (from pxe_setup)
    ├── openshift-416-prod-master -> installer-openshift-4.16/    # Symlinks
    ├── openshift-416-prod-worker -> installer-openshift-4.16/
    └── openshift-416-test-master -> installer-openshift-4.16/
```

## MAC-based Ignition Strategy

Each node gets a unique Ignition file named after its MAC address:

- **MAC Address**: `52:54:00:AA:BB:01`
- **Filename**: `52-54-00-aa-bb-01.ign` (lowercase, colons→hyphens)
- **Location**: `/tftpboot/ignition/openshift-4.16/prod/master/52-54-00-aa-bb-01.ign`

This approach:
- Avoids category proliferation (no need for `worker-init`, `worker-expand`, etc.)
- Allows same category to serve initial and expansion nodes
- Makes per-node customization easy
- Provides clear audit trail

## Generating Ignition Files

### Initial Cluster

```bash
# Create install-config.yaml and agent-config.yaml
openshift-install agent create image

# Extract Ignition files from generated ISO or use provided files
```

### Expanding Cluster

```bash
# Option A: Generate new agent ISO with new nodes
openshift-install agent create image

# Option B: Extract worker Ignition from running cluster
oc extract -n openshift-machine-api secret/worker-user-data \
  --keys=userData \
  --to=/root/ignition/worker-new.ign
```

## Deployment Process

After running this role:

1. Nodes are registered in BCM with MAC-based Ignition URLs
2. Power on nodes (or run `cmsh device use <node>; power on`)
3. Nodes PXE boot, download Ignition, and install CoreOS
4. Nodes boot into CoreOS and join OpenShift cluster
5. Verify cluster status with `oc get nodes`

## Adding Nodes Later

To add nodes to an existing cluster:

1. Generate new Ignition file for the new node
2. Add node definition to `cluster_nodes` with new MAC address
3. Run the playbook again
4. Same category is reused - only Ignition URL differs

## License

GPL-3.0-or-later

## Author

NVIDIA Corporation
