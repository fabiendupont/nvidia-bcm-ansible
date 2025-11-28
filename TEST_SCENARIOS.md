# Test Scenarios for BCM Ansible Collection

This document tracks test scenarios for validating the complete BCM automation workflow.

## Test Scenarios

### 1. RHEL with BCM Lite Daemon (quadlet)

#### 1a. New RHEL deployment via PXE
**Status:** ✅ Ready to Test
**Playbook:** `playbooks/deploy_rhel_cluster.yml`

**Steps:**
1. Deploy RHEL nodes via PXE using deploy_rhel_cluster.yml
2. Verify nodes are registered as PhysicalNode
3. Verify PXE boot completes successfully
4. Verify BCM Lite Daemon quadlet is deployed
5. Verify nodes convert to LiteNode after installation
6. Verify agents connect to BCM

**Prerequisites:**
- RHEL ISO available on BCM head node
- Inventory with cluster definition
- Node roles defined (login, compute, etc.)
- Bootstrap certificates generated

**Expected Outcome:**
- Nodes PXE boot and install RHEL
- BCM Lite Daemon deployed via kickstart %post
- Nodes converted to LiteNodes post-installation
- BCM Lite Daemon running as systemd service (quadlet)
- Nodes appear in `cmsh -c 'device; list -L'`

**Implementation Completed:**
- ✅ Kickstart updated: Removed traditional BCM packages, deploy quadlet in %post
- ✅ Kickstart downloads quadlet + certificates via HTTP during installation
- ✅ deploy_rhel_cluster.yml: Added verification + convert_to_litenode
- ✅ Generic convert_to_litenode task (reusable for RHEL and OpenShift)
- ✅ RHEL nodes registered as PhysicalNode for PXE
- ✅ Automatic conversion to LiteNode post-installation

---

#### 1b. Existing RHEL machine joining BCM
**Status:** ✅ Ready to Test
**Playbook:** `playbooks/join_rhel_nodes.yml`

**Steps:**
1. Register existing RHEL nodes as LiteNodes in BCM
2. Deploy BCM Lite Daemon as quadlet via Ansible
3. Deploy bootstrap certificates
4. Verify agents connect to BCM

**Prerequisites:**
- RHEL nodes already deployed and accessible via SSH
- Inventory with node details (hostname, MAC, IP)
- Bootstrap certificates generated

**Expected Outcome:**
- Nodes registered in BCM as LiteNodes
- BCM Lite Daemon deployed and running via Ansible
- Nodes manageable from BCM
- Nodes appear in `cmsh -c 'device; list -L'`

**Implementation Completed:**
- ✅ Created join_rhel_nodes.yml playbook
- ✅ Registers nodes directly as LiteNodes (no PhysicalNode step)
- ✅ Deploys quadlet via Ansible (scp to nodes)
- ✅ Deploys bootstrap certificates via Ansible
- ✅ Enables and starts BCM agent service
- ✅ Documented in playbooks/README.md

---

### 2. OpenShift with BCM Lite Daemon (Helm chart)

#### 2a. New single-node OpenShift deployment via PXE
**Status:** ⏳ To Test (currently 3-node)
**Playbook:** `playbooks/deploy_openshift_cluster.yml`

**Steps:**
1. Deploy single-node OpenShift (SNO) via PXE
2. Verify node is registered as PhysicalNode
3. Verify PXE boot and OpenShift installation
4. Verify node converts to LiteNode
5. Verify BCM agent Helm chart deployment
6. Verify agent pods running

**Prerequisites:**
- OpenShift pull secret
- Single-node inventory configuration

**Expected Outcome:**
- Single control-plane node deployed
- Node runs as both control-plane and worker
- BCM agent DaemonSet deployed
- Node appears in BCM as LiteNode

**Current Gaps:**
- ❓ Does deploy_openshift_cluster.yml support single-node?
- ❓ Check if agent-config.yaml generation supports SNO
- ❓ Verify rendezvousIP works with single node

---

#### 2b. Add worker node to existing OpenShift cluster
**Status:** ❌ Playbook Missing
**Playbook:** `playbooks/add_openshift_worker.yml` (NEED TO CREATE)

**Steps:**
1. Generate Ignition for new worker node
2. Register node as PhysicalNode in BCM
3. PXE boot new worker node
4. Verify node joins OpenShift cluster
5. Convert to LiteNode
6. BCM agent already deployed via DaemonSet

**Prerequisites:**
- Existing OpenShift cluster deployed
- Kubeconfig available
- New node MAC address and IP

**Expected Outcome:**
- New worker node PXE boots
- Node joins cluster automatically
- Node registered in BCM as LiteNode
- BCM agent pod starts on new node

**Current Gaps:**
- ❌ Need to create add_openshift_worker.yml
- ❓ How to generate worker Ignition from existing cluster?
- ❓ Does OpenShift Agent-Based Installer support adding nodes?

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
- [ ] 1a: New RHEL deployment via PXE
- [ ] 1b: Existing RHEL joining BCM

### OpenShift Tests
- [ ] 2a: Single-node OpenShift via PXE
- [ ] 2b: Add worker to existing cluster
- [ ] 2c: Existing OpenShift joining BCM

### Dynamic Inventory
- [ ] Configure bright_nodes plugin
- [ ] Test with registered nodes
- [ ] Update playbook examples

---

## Current Implementation Gaps

### Must Create
1. **add_openshift_worker.yml** - Add worker to existing cluster
2. **Dynamic inventory examples** - Using bright_nodes plugin

### Must Verify
1. **deploy_openshift_cluster.yml** - Single-node OpenShift support?
2. **All playbooks** - Work with dynamic inventory?
3. **RHEL deployment** - Test PXE deployment with BCM Lite Daemon
4. **RHEL join** - Test join_rhel_nodes.yml with existing machines

### Completed
1. ✅ **join_rhel_nodes.yml** - Join existing RHEL to BCM (created)
2. ✅ **deploy_rhel_cluster.yml** - Updated to deploy BCM Lite Daemon quadlet
3. ✅ **Generic convert_to_litenode** - Reusable for RHEL and OpenShift
4. ✅ **Kickstart BCM Lite Daemon** - Deployed via %post script
5. ✅ **Ansible BCM Lite Daemon** - Deployed for existing nodes

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

---

## Progress Tracking

Last Updated: 2025-11-25

**Completed:**
- ✅ Core playbook structure
- ✅ OpenShift full deployment (3-node)
- ✅ OpenShift join existing cluster
- ✅ BCM agent build with intelligent rebuild
- ✅ Documentation cleanup
- ✅ Generic convert_to_litenode task (pure BCM operations)
- ✅ RHEL PXE deployment with BCM Lite Daemon (kickstart approach)
- ✅ RHEL join existing nodes (Ansible approach)
- ✅ join_rhel_nodes.yml playbook created
- ✅ Updated kickstart to deploy quadlet in %post
- ✅ Updated deploy_rhel_cluster.yml with verification and conversion

**In Progress:**
- ⏳ Testing RHEL scenarios (1a, 1b)
- ⏳ Creating add_openshift_worker.yml
- ⏳ Dynamic inventory setup

**Blocked:**
- None currently
