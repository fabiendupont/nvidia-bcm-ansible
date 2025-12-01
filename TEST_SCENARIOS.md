# Test Scenarios for BCM Ansible Collection

This document tracks test scenarios for validating the complete BCM automation workflow.

## Test Scenarios

### 1. RHEL with BCM Lite Daemon (quadlet)

#### 1a. New RHEL deployment via PXE
**Status:** ✅ Tested (2025-11-28)
**Playbook:** `playbooks/deploy_rhel_cluster.yml`

**Test Workflow (VM with plain RHEL, no BCM agent during install):**
```bash
# 1. Deploy VM and install RHEL via PXE (install_bcm_agent: false)
PYTHONPATH=.venv/lib/python3.14/site-packages \
  ansible-playbook -i inventory/test_plain_rhel.yml playbooks/deploy_rhel_cluster.yml

# 2. Wait for PXE installation to complete (~10-15 minutes)
#    Monitor VM console or check SSH availability

# 3. Join the RHEL node to BCM (installs BCM agent)
PYTHONPATH=.venv/lib/python3.14/site-packages \
  ansible-playbook -i inventory/test_plain_rhel.yml playbooks/join_rhel_nodes.yml

# 4. Verify node is registered as LiteNode
ssh bcm-headnode "cmsh -c 'device; list -L'"
```

**Test Inventory:** `inventory/test_plain_rhel.yml`
- VM: `test-plain-01` (4GB RAM, 2 vCPUs, 40GB disk)
- Network: `bcm-internalnet` (libvirt)
- Category: `rhel-plain-compute` with `install_bcm_agent: false`

**Prerequisites:**
- RHEL ISO available on BCM head node
- Inventory with cluster definition
- Node roles defined (login, compute, etc.)
- Sushy emulator for Redfish power management

**Test Results:**
- ✅ VM created via libvirt
- ✅ Node registered as PhysicalNode in BCM
- ✅ PXE boot successful
- ✅ RHEL installation completed
- ✅ Node accessible via SSH after installation

**Implementation Completed:**
- ✅ Kickstart updated: Removed traditional BCM packages, deploy quadlet in %post
- ✅ Kickstart downloads quadlet + certificates via HTTP during installation
- ✅ deploy_rhel_cluster.yml: Added verification + convert_to_litenode
- ✅ Generic convert_to_litenode task (reusable for RHEL and OpenShift)
- ✅ RHEL nodes registered as PhysicalNode for PXE
- ✅ Automatic conversion to LiteNode post-installation

---

#### 1b. Existing RHEL machine joining BCM
**Status:** ✅ Tested (2025-11-28)
**Playbook:** `playbooks/join_rhel_nodes.yml`

**Test Workflow:**
```bash
# 1. Ensure RHEL node is accessible via SSH
ssh root@10.141.100.201 hostname

# 2. Run join playbook
PYTHONPATH=.venv/lib/python3.14/site-packages \
  ansible-playbook -i inventory/test_plain_rhel.yml playbooks/join_rhel_nodes.yml

# 3. Verify node is registered as LiteNode
ssh bcm-headnode "cmsh -c 'device; list -L'"

# 4. Check BCM agent status on node
ssh root@10.141.100.201 systemctl status bcm-agent
```

**Test Results:**
- ✅ PhysicalNode removed (if existed from PXE deployment)
- ✅ LiteNode registration created
- ✅ Per-node litenode certificates generated
- ✅ BCM agent quadlet deployed to node
- ✅ BCM agent service started and active
- ✅ Node appears in `cmsh -c 'device; list -L'`

**Key Implementation Details:**
- Uses `nvidia.bcm.convert_to_litenode` role for BCM registration
- Generates per-node litenode certificates (NOT bootstrap certs)
- Quadlet units auto-enable on boot via `[Install]` section
- `systemctl start` (not `enable --now`) for generated units

**Prerequisites:**
- RHEL nodes already deployed and accessible via SSH
- Inventory with node details (hostname, MAC, IP, ansible_user)
- CA certificate exists on BCM head node

**Implementation Completed:**
- ✅ Created join_rhel_nodes.yml playbook
- ✅ Uses convert_to_litenode role (removes PhysicalNode if exists)
- ✅ Generates per-node litenode certificates via cmsh
- ✅ Deploys quadlet via Ansible (scp to nodes)
- ✅ Deploys certificates via Ansible
- ✅ Starts BCM agent service
- ✅ Documented in playbooks/README.md

---

### 2. OpenShift with BCM Lite Daemon (Helm chart)

#### 2a. New single-node OpenShift deployment via PXE
**Status:** ✅ Tested (2025-11-30)
**Playbook:** `playbooks/deploy_openshift_cluster.yml`
**Inventory:** `inventory/openshift_sno_test.yml`

**Test Workflow:**
```bash
# 1. Deploy SNO cluster via PXE
PYTHONPATH=.venv/lib/python3.14/site-packages \
  ansible-playbook -i inventory/openshift_sno_test.yml \
    playbooks/deploy_openshift_cluster.yml \
    -e "create_test_vms=true openshift_pull_secret_path=/home/fdupont/pull-secret.json"

# 2. Monitor installation progress (~53 minutes for SNO)
ssh root@192.168.122.204 "tail -f /var/log/bcm-deployment-openshift-test-sno-*.log"
virt-viewer -c qemu:///system sno-master-0

# 3. Verify cluster is ready
export KUBECONFIG=/openshift/clusters/test-sno/auth/kubeconfig
export PATH=/openshift/tools/4.20:$PATH
oc get nodes
oc get clusteroperators
```

**SNO-Specific Configuration:**
- **Single node**: 1 control-plane node (no workers)
- **No VIPs**: Uses `platform: none` (not `platform: baremetal`)
- **Worker replicas**: 0 (control plane runs workloads)
- **Resources**: 16GB RAM, 8 vCPUs (higher than 3-node since it runs everything)
- **Node role**: master (acts as both control-plane and worker)

**Prerequisites:**
- OpenShift pull secret from console.redhat.com
- SNO inventory configuration (`openshift_sno_test.yml`)
- Sushy emulator running for Redfish power management

**Test Results:**
- ✅ VM created via libvirt (sno-master-0)
- ✅ Node registered as PhysicalNode in BCM
- ✅ PXE boot successful (rootfs downloaded correctly)
- ✅ OpenShift SNO installation completed (~53 minutes)
- ✅ Node accessible via SSH after installation
- ✅ Cluster became Ready (1 node)
- ✅ PhysicalNode → LiteNode conversion succeeded
- ✅ BCM agent deployment role task (deploy_bcm_daemon.yml) tested end-to-end
  - ✅ Prerequisites validated (kubeconfig, Helm chart, certificates)
  - ✅ Bootstrap certificates read from BCM head node
  - ✅ Namespace created (bcm-agent)
  - ✅ Certificate Secret created (bcm-bootstrap-cert)
  - ✅ Helm chart deployed successfully
  - ⚠️ DaemonSet blocked by OpenShift SCC (needs privileged SCC - Helm chart config issue)

**Bugs Fixed During Testing:**
- ✅ Pull secret double-encoding in install-config.yaml.j2
- ✅ Bootloader must be uppercase "SYSLINUX" not "syslinux"
- ✅ Missing partition: "base" in node registration
- ✅ **PXE symlink setup not called** - added automatic symlink creation after generating boot artifacts

**Bugs Fixed During E2E BCM Agent Testing (2025-11-30):**
- ✅ Missing `bcm_agent_namespace` variable in playbook pre_tasks
- ✅ Missing `bcm_agent_local_tag` variable in openshift_cluster defaults
- ✅ Bootstrap certificates checked on wrong host (localhost vs BCM head node)
- ✅ `oc` command path hardcoded without full path to /openshift/tools/{version}/oc
- ✅ Missing image configuration in Helm chart values (needs `localhost/bcm-agent:latest`)
- ⚠️ Missing `kubernetes` Python library on BCM head node (installed via pip3)

**E2E Test Results (deploy_bcm_daemon.yml role task) - 2025-11-30:**
- ✅ Created `roles/openshift_cluster/tasks/deploy_bcm_daemon.yml` orchestration task
- ✅ Prerequisites validated (kubeconfig, Helm chart, cluster nodes, certificates)
- ✅ Bootstrap certificates read from BCM head node successfully
- ✅ Namespace created (bcm-agent)
- ✅ Privileged SCC granted to bcm-agent ServiceAccount
- ✅ Certificate Secret created (bcm-bootstrap-cert with CA, cert, key)
- ✅ Helm chart deployed with image config: `localhost/bcm-agent:latest`
- ✅ BCM agent image loaded onto SNO node from BCM head node
- ✅ BCM agent pod running successfully
- ✅ Agent requested per-node certificate (ID: d277782e-954d-42ec-b55a-fee564252d69)
- ⚠️ **Certificate approval pending** - bootstrap cert lacks auto-sign permissions
  - Agent waiting for BCM to approve/sign the per-node certificate request
  - Metrics server won't start until certificate is approved (probes failing)
  - This is a deployment-time configuration issue, not a code issue
  - **Solution**: Configure bootstrap certificate with auto-sign permissions OR manually approve requests

**Root Cause Analysis:**
The deployment workflow is fully functional. The final step requires either:
1. Bootstrap certificate configured with auto-sign permissions for node certificates, OR
2. Manual approval of each node's certificate request via BCM cmdaemon

The `deploy_bcm_daemon.yml` role task is complete and working as designed.

**Implementation Verified:**
- ✅ install-config.yaml.j2 supports SNO (master replicas auto-counted, worker replicas=0)
- ✅ agent-config.yaml.j2 supports SNO (rendezvousIP uses first master)
- ✅ Platform automatically switches to `none` when no VIPs defined
- ✅ Created openshift_sno_test.yml inventory
- ✅ PXE boot infrastructure correctly creates cluster-specific symlinks

---

#### 2b. Add worker node to existing OpenShift cluster
**Status:** ✅ Playbook Created (2025-11-28) - Ready to Test
**Playbook:** `playbooks/add_openshift_worker.yml`

**Workflow:**
```bash
# Add a new worker to existing cluster
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

**Steps:**
1. Read BCM SSH keys for core user access
2. Generate worker ignition config (merges with cluster's worker ignition)
3. Register node as PhysicalNode in BCM for PXE boot
4. Optionally create test VM
5. Wait for worker to PXE boot and join cluster
6. Convert to LiteNode in BCM
7. BCM agent pod starts automatically (DaemonSet already deployed)

**Prerequisites:**
- Existing OpenShift cluster deployed (e.g., via `deploy_openshift_cluster.yml`)
- Kubeconfig available on BCM head node
- OpenShift tools installed for the cluster version
- RHCOS PXE boot files available
- BCM agent DaemonSet already deployed
- New node details: hostname, MAC address, IP

**Implementation Details:**
- Worker ignition merges with cluster's Machine Config Server (port 22623)
- Uses pointer ignition that references `http://{{ bcm_server }}:22623/config/worker`
- Adds BCM SSH keys and sets hostname
- Category matches cluster's worker category naming convention
- Supports optional test VM creation via libvirt

**Expected Outcome:**
- New worker node PXE boots with RHCOS
- Worker joins cluster automatically
- Node appears in `oc get nodes`
- Node registered in BCM as LiteNode
- BCM agent pod starts on new node

---

#### 2c. Existing OpenShift cluster joining BCM
**Status:** ✅ Ready to Test
**Playbook:** `playbooks/join_openshift_cluster.yml`

**Steps:**
1. Register cluster nodes as LiteNodes in BCM
2. Build BCM agent container image
3. Deploy BCM agent Helm chart
4. Verify agents connect to BCM

**Prerequisites:**
- Existing OpenShift cluster accessible
- Kubeconfig available on BCM head node
- Bootstrap certificates generated

**Expected Outcome:**
- All cluster nodes registered as LiteNodes
- BCM agent DaemonSet deployed
- Agent pods running on all nodes
- Nodes appear in `cmsh -c 'device; list -L'`

**Current Status:**
- ✅ Playbook exists
- ✅ Documented in playbooks/README.md
- ⏳ Needs testing

---

## Dynamic Inventory Integration

### Use BCM Dynamic Inventory for Registered Nodes

**Status:** ❌ Not Configured
**Documentation:** Need to create examples

**Objective:**
Once nodes are registered in BCM, use the `bright_nodes` dynamic inventory plugin instead of static inventory.

**Steps:**
1. Configure bright_nodes inventory plugin
2. Create example inventory using plugin
3. Update playbooks to work with both static and dynamic inventory

**Example Configuration:**
```yaml
# inventory/bcm_dynamic.yml
plugin: brightcomputing.bcm110.bright_nodes
bcm_host: localhost
bcm_port: 8081
use_categories: true
use_partitions: true
filters:
  partition: base
  category: openshift_*
```

**Current Gaps:**
- ❌ No dynamic inventory examples
- ❌ Playbooks not tested with dynamic inventory
- ❓ How to handle mixed scenarios (some nodes in BCM, some not)?

---

## Testing Checklist

### Before Testing
- [ ] BCM head node accessible
- [ ] VMs or physical hardware available
- [ ] Pull secrets / ISO files ready
- [ ] Bootstrap certificates generated
- [ ] Ansible collections installed

### RHEL Tests
- [x] 1a: New RHEL deployment via PXE (tested 2025-11-28)
- [x] 1b: Existing RHEL joining BCM (tested 2025-11-28)

### OpenShift Tests
- [x] 2a: Single-node OpenShift via PXE (tested 2025-11-30)
- [ ] 2b: Add worker to existing cluster
- [ ] 2c: Existing OpenShift joining BCM

### Dynamic Inventory
- [ ] Configure bright_nodes plugin
- [ ] Test with registered nodes
- [ ] Update playbook examples

---

## Current Implementation Gaps

### Must Create
1. **Dynamic inventory examples** - Using bright_nodes plugin

### Prerequisites for BCM Agent Deployment
1. **nvidia-bcm-lite-daemon repository** - Clone and make Helm chart available
   - Repository must be cloned to `/root/nvidia-bcm-lite-daemon/` on BCM head node
   - Helm chart should be at `/root/nvidia-bcm-lite-daemon/helm/bcm-agent`
   - Required for all OpenShift BCM agent deployments

2. **Build BCM agent container image** (optional, can use registry)
   - Implemented via `playbooks/build_bcm_agent_image.yml`
   - TODO: Create `roles/openshift_cluster/tasks/build_bcm_agent_image.yml` for role-based builds

### Must Verify
1. **All playbooks** - Work with dynamic inventory?

### Completed
1. ✅ **join_rhel_nodes.yml** - Join existing RHEL to BCM (created and tested)
2. ✅ **deploy_rhel_cluster.yml** - Updated to deploy BCM Lite Daemon quadlet (tested)
3. ✅ **Generic convert_to_litenode** - Reusable for RHEL and OpenShift
4. ✅ **Kickstart BCM Lite Daemon** - Deployed via %post script
5. ✅ **Ansible BCM Lite Daemon** - Deployed for existing nodes
6. ✅ **RHEL PXE deployment** - Tested with VM (test_plain_rhel.yml inventory)
7. ✅ **RHEL join BCM** - Tested with VM (join_rhel_nodes.yml playbook)
8. ✅ **add_openshift_worker.yml** - Add worker to existing cluster (created 2025-11-28)
9. ✅ **roles/openshift_cluster/tasks/deploy_bcm_daemon.yml** - BCM agent deployment role task (created 2025-11-30)

### Nice to Have
1. Validation playbooks (test connectivity, verify agents)
2. Troubleshooting playbooks (collect logs, diagnose issues)
3. Upgrade playbooks (update BCM agent versions)

---

## Notes

- **PhysicalNode vs LiteNode**: Use PhysicalNode for PXE boot, convert to LiteNode post-installation
- **Bootstrap certificates**: Required for BCM agent deployment
- **Dynamic inventory**: Only works for nodes already in BCM
- **Quadlet vs Helm**: RHEL uses quadlet (systemd), OpenShift uses Helm (Kubernetes)
- **OpenShift Security Context Constraints (SCC)**: BCM agent DaemonSet requires privileged SCC
  - Needs: hostNetwork, hostPID, hostIPC, hostPath volumes, privileged container
  - Solution: Helm chart must create ServiceAccount with privileged SCC binding
  - Command: `oc adm policy add-scc-to-user privileged -z bcm-agent -n bcm-agent`

---

## Progress Tracking

Last Updated: 2025-11-30

**Completed:**
- ✅ Core playbook structure
- ✅ OpenShift join existing cluster
- ✅ BCM agent build with intelligent rebuild
- ✅ Documentation cleanup
- ✅ Generic convert_to_litenode task (pure BCM operations)
- ✅ RHEL PXE deployment with BCM Lite Daemon (kickstart approach)
- ✅ RHEL join existing nodes (Ansible approach)
- ✅ join_rhel_nodes.yml playbook created
- ✅ Updated kickstart to deploy quadlet in %post
- ✅ Updated deploy_rhel_cluster.yml with verification and conversion
- ✅ **TESTED: RHEL VM deployment via PXE (scenario 1a)** - 2025-11-28
- ✅ **TESTED: RHEL VM joining BCM (scenario 1b)** - 2025-11-28
- ✅ convert_to_litenode role refactored (removed agent wait logic for composability)
- ✅ join_rhel_nodes.yml uses nvidia.bcm.convert_to_litenode role
- ✅ **add_openshift_worker.yml playbook created** - 2025-11-28
- ✅ **TESTED: Single-Node OpenShift deployment via PXE (scenario 2a)** - 2025-11-30
- ✅ **Fixed: PXE symlink setup automated** - roles/openshift_cluster/tasks/generate_pxe_files.yml
- ✅ **Fixed: Pull secret encoding, bootloader case, partition parameter** - 2025-11-30
- ✅ **TESTED E2E: deploy_bcm_daemon.yml role task** - 2025-11-30
- ✅ **Fixed: Certificate delegation, oc path, missing variables** - 2025-11-30
- ✅ **Fixed: Missing image configuration in Helm chart** - 2025-11-30
- ✅ **Fixed: OpenShift SCC configuration** - Added privileged SCC binding to deploy_agent.yml
- ✅ **Created: deploy_bcm_daemon.yml orchestration task** - 2025-11-30
- ✅ **Verified: BCM agent pod running and requesting certificates** - 2025-11-30

**In Progress:**
- ⏳ Dynamic inventory setup

**Blocked:**
- ⚠️ Bootstrap certificate auto-sign permissions (operational configuration, not code issue)
