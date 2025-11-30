# BCM Ansible Playbooks

This directory contains purpose-specific playbooks for different deployment scenarios. Each playbook is designed to be run independently for maximum flexibility.

## Quick Reference

| Playbook | Use Case | Prerequisites |
|----------|----------|---------------|
| **RHEL Deployments** |||
| `deploy_rhel_cluster.yml` | Deploy new RHEL cluster via PXE | RHEL ISO, inventory |
| `join_rhel_nodes.yml` | Join existing RHEL machines to BCM | SSH access, inventory |
| **OpenShift Deployments** |||
| `deploy_openshift_cluster.yml` | Deploy new OpenShift cluster from scratch | Pull secret, inventory |
| `add_openshift_worker.yml` | Add worker to existing OpenShift cluster | Running cluster, kubeconfig, worker details |
| `join_openshift_cluster.yml` | Integrate existing cluster with BCM | Running cluster, kubeconfig |
| `deploy_bcm_agent.yml` | Deploy/retry BCM agent only | Cluster deployed, LiteNodes registered |
| `build_bcm_agent_image.yml` | Build container image only | None |
| **Utilities** |||
| `cleanup_bcm_cluster.yml` | Remove cluster from BCM | None |
| `cleanup_test_vms.yml` | Remove local test VMs | None |
| `setup_bcm_bootstrap_certs.yml` | Generate bootstrap certificates | None |

## RHEL Deployment Playbooks

### deploy_rhel_cluster.yml
**Purpose:** Full RHEL cluster deployment via PXE with BCM Lite Daemon

**When to use:**
- Deploying new RHEL nodes via PXE
- Want automated RHEL installation with BCM integration
- Need BCM Lite Daemon deployed automatically

**What it does:**
1. Sets up PXE infrastructure for RHEL
2. Creates BCM categories for node roles
3. Registers nodes as PhysicalNode (for PXE boot)
4. Waits for RHEL installation to complete
5. Converts nodes to LiteNode
6. Verifies BCM Lite Daemon is running (deployed via kickstart)

**Usage:**
```bash
ansible-playbook -i inventory/rhel_cluster.yml \
  playbooks/deploy_rhel_cluster.yml
```

**Key features:**
- BCM Lite Daemon deployed via kickstart %post script
- Bootstrap certificates served via HTTP during installation
- Automatic conversion from PhysicalNode to LiteNode

---

### join_rhel_nodes.yml
**Purpose:** Join existing RHEL machines to BCM

**When to use:**
- RHEL nodes already deployed manually
- Want to add BCM management to existing RHEL systems
- Nodes don't need PXE installation

**What it does:**
1. Registers nodes as LiteNodes in BCM (directly, no PhysicalNode)
2. Deploys BCM Lite Daemon quadlet via Ansible
3. Deploys bootstrap certificates
4. Enables and starts BCM agent service

**Usage:**
```bash
ansible-playbook -i inventory/existing_rhel_nodes.yml \
  playbooks/join_rhel_nodes.yml
```

**Example inventory:**
```yaml
all:
  hosts:
    bcm_headnode:
      ansible_host: 192.168.122.204
  vars:
    cluster_name: "rhel-prod"
    rhel_nodes:
      - name: rhel-node-1
        mac: "52:54:00:AA:BB:01"
        ip: "10.141.160.50"
        role: compute
      - name: rhel-node-2
        mac: "52:54:00:AA:BB:02"
        ip: "10.141.160.51"
        role: compute"
```

---

## OpenShift Deployment Playbooks

### deploy_openshift_cluster.yml
**Purpose:** Full OpenShift cluster deployment via PXE

**When to use:**
- Deploying a brand new OpenShift cluster
- Need automated PXE boot setup
- Want full integration with BCM from start

**What it does:**
1. Sets up PXE infrastructure on BCM
2. Creates test VMs (optional)
3. Waits for OpenShift installation
4. Converts nodes to LiteNodes
5. Deploys BCM agent DaemonSet

**Usage:**
```bash
# With VM creation (testing):
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/deploy_openshift_cluster.yml \
  -e "create_test_vms=true openshift_pull_secret_path=/path/to/pull-secret.json"

# Physical hardware (no VMs):
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/deploy_openshift_cluster.yml \
  -e "openshift_pull_secret_path=/path/to/pull-secret.json"

# Skip BCM agent:
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/deploy_openshift_cluster.yml \
  -e "skip_bcm_agent=true"
```

---

### add_openshift_worker.yml
**Purpose:** Add a worker node to an existing OpenShift cluster via PXE

**When to use:**
- Expanding an existing OpenShift cluster with new workers
- Cluster was deployed via `deploy_openshift_cluster.yml` or manually
- Need to scale up worker capacity

**What it does:**
1. Reads BCM SSH keys for core user access
2. Generates worker ignition config (merges with cluster's worker ignition)
3. Registers new worker as PhysicalNode in BCM for PXE boot
4. Optionally creates test VM
5. Waits for worker to PXE boot and join cluster
6. Converts worker to LiteNode in BCM
7. BCM agent pod starts automatically (DaemonSet already deployed)

**Usage:**
```bash
# Add worker with required details
PYTHONPATH=.venv/lib/python3.14/site-packages \
  ansible-playbook -i inventory/openshift_test_cluster.yml \
    playbooks/add_openshift_worker.yml \
    -e "worker_name=ocp-worker-3 worker_mac=52:54:00:0C:01:03 worker_ip=10.141.160.53"

# With VM creation for testing
PYTHONPATH=.venv/lib/python3.14/site-packages \
  ansible-playbook -i inventory/openshift_test_cluster.yml \
    playbooks/add_openshift_worker.yml \
    -e "worker_name=ocp-worker-3 worker_mac=52:54:00:0C:01:03 worker_ip=10.141.160.53 create_test_vm=true"
```

**Required variables:**
- `worker_name` - Hostname for the new worker
- `worker_mac` - MAC address for the new worker
- `worker_ip` - IP address for the new worker

**Prerequisites:**
- Existing OpenShift cluster deployed (e.g., via `deploy_openshift_cluster.yml`)
- Kubeconfig available on BCM head node
- OpenShift tools installed for the cluster version
- RHCOS PXE boot files available
- BCM agent DaemonSet already deployed
- Worker role defined in inventory `node_roles`

**Key features:**
- Worker ignition merges with cluster's Machine Config Server (port 22623)
- Uses pointer ignition that references cluster's worker config
- Adds BCM SSH keys and sets hostname
- Automatic PhysicalNode→LiteNode conversion after join

---

### join_openshift_cluster.yml
**Purpose:** Join an existing OpenShift cluster to BCM

**When to use:**
- Cluster deployed manually or via other automation
- OpenShift Installer deployed cluster
- Want to add BCM management to existing cluster

**What it does:**
1. Registers cluster nodes as LiteNodes in BCM
2. Builds BCM agent image (if needed)
3. Deploys BCM agent DaemonSet

**Usage:**
```bash
ansible-playbook -i inventory/existing_cluster.yml \
  playbooks/join_openshift_cluster.yml
```

**Example inventory:**
```yaml
all:
  hosts:
    bcm_headnode:
      ansible_host: 192.168.122.204
  vars:
    cluster_name: "prod-ocp"
    kubeconfig_path: "/root/prod-ocp/auth/kubeconfig"
    openshift_version: "4.20"
    cluster_nodes:
      - name: master-0
        mac: "52:54:00:AA:BB:01"
        ip: "10.141.160.50"
        role: master
```

---

### deploy_bcm_agent.yml
**Purpose:** Deploy or retry BCM agent deployment

**When to use:**
- BCM agent deployment failed during full deployment
- Want to update BCM agent version
- Cluster already has LiteNodes registered

**Usage:**
```bash
# Deploy with automatic build:
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/deploy_bcm_agent.yml

# Redeploy without rebuilding:
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/deploy_bcm_agent.yml \
  -e skip_build=true
```

---

### build_bcm_agent_image.yml
**Purpose:** Build BCM agent container image only

**When to use:**
- Pre-build image before deploying to clusters
- Update image after CVE fixes
- Repository updates available

**Usage:**
```bash
# Normal build (only if changes detected):
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/build_bcm_agent_image.yml

# Force rebuild:
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/build_bcm_agent_image.yml \
  -e bcm_agent_force_rebuild=true
```

---

## Common Workflows

### Fresh OpenShift Deployment with VMs
```bash
# 1. Generate bootstrap certificates
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/setup_bcm_bootstrap_certs.yml

# 2. Full deployment
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/deploy_openshift_cluster.yml \
  -e "create_test_vms=true openshift_pull_secret_path=/path/to/pull-secret.json"
```

### Join Existing Cluster
```bash
# 1. Generate bootstrap certificates
ansible-playbook -i inventory/existing_cluster.yml \
  playbooks/setup_bcm_bootstrap_certs.yml

# 2. Join cluster to BCM
ansible-playbook -i inventory/existing_cluster.yml \
  playbooks/join_openshift_cluster.yml
```

### Retry Failed BCM Agent Deployment
```bash
# Just redeploy agent (uses cached image)
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/deploy_bcm_agent.yml \
  -e skip_build=true
```

### Update BCM Agent Version
```bash
# 1. Build new image
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/build_bcm_agent_image.yml \
  -e bcm_agent_force_rebuild=true

# 2. Deploy to clusters
ansible-playbook -i inventory/cluster1.yml \
  playbooks/deploy_bcm_agent.yml -e skip_build=true
```

### Clean Up and Redeploy
```bash
# 1. Clean up VMs
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/cleanup_test_vms.yml

# 2. Clean up BCM
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/cleanup_bcm_cluster.yml

# 3. Fresh deployment
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/deploy_openshift_cluster.yml \
  -e "create_test_vms=true openshift_pull_secret_path=/path/to/pull-secret.json"
```

## Troubleshooting

### "Cannot access OpenShift cluster"
```bash
# Verify kubeconfig and accessibility
ssh root@bcm-headnode "export KUBECONFIG=/path/to/kubeconfig && oc get nodes"
```

### "Bootstrap certificate not found"
```bash
# Run bootstrap certificate setup
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/setup_bcm_bootstrap_certs.yml
```

### "BCM agent pods not starting"
```bash
# Check pod status and logs
ssh root@bcm-headnode "export KUBECONFIG=/path/to/kubeconfig && oc get pods -n nvidia-bcm-agent"
ssh root@bcm-headnode "export KUBECONFIG=/path/to/kubeconfig && oc logs -n nvidia-bcm-agent <pod-name>"
```

### "LiteNode not showing in BCM"
```bash
# Verify LiteNode registration
ssh root@bcm-headnode "cmsh -c 'device; list -L'"
```
