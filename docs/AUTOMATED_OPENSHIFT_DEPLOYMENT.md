# Fully Automated OpenShift Deployment with BCM

This document describes the fully automated OpenShift deployment process where Ansible handles everything from ISO generation to cluster deployment.

## Overview

The deployment is now fully automated:
1. **Ansible generates the OpenShift agent ISO** on the control node
2. **Copies it to BCM head node**
3. **Extracts boot files** (vmlinuz, initrd, rootfs.img)
4. **Generates Ignition configs** with BCM SSH keys
5. **Deploys via two-phase approach** (GenericDevice → LiteNode)

## Prerequisites

### On Ansible Control Node (this machine)

1. **Red Hat Pull Secret**
   ```bash
   # Download from https://console.redhat.com/openshift/install/pull-secret
   # Save to ~/pull-secret.json
   ```

2. **Ansible Collection**
   ```bash
   # Already installed via collections/ansible_collections/nvidia/bcm/
   ```

### On BCM Head Node

1. **BCM Agent Helm Chart**
   - Located at: `/root/nvidia-bcm-lite-daemon/helm/bcm-agent`

2. **Bootstrap Certificate**
   - Located at: `/cm/local/apps/cmd/etc/bootstrap/cert.pem`

## What Ansible Does Automatically

### Phase 0: ISO Generation (NEW!)

**On Ansible Control Node:**
1. Downloads and installs `openshift-install` client (if not present)
2. Reads BCM SSH keys from head node
3. Generates `install-config.yaml` with:
   - Cluster configuration
   - Network settings
   - Pull secret
   - BCM SSH keys
4. Generates `agent-config.yaml` with:
   - Node hostnames
   - MAC addresses
   - Static IP configuration
   - Network interfaces
5. Runs `openshift-install agent create image`
6. Copies generated ISO to BCM head node

**Files Created:**
- `~/openshift/test-ocp/install-config.yaml`
- `~/openshift/test-ocp/agent-config.yaml`
- `~/openshift/test-ocp/agent.x86_64.iso`

### Phase 1: PXE Installation

**On BCM Head Node:**
1. Extracts boot files from agent ISO
2. Creates PXE boot categories
3. Generates MAC-based Ignition files with BCM SSH keys
4. Registers nodes as GenericDevice
5. Powers on nodes via Redfish

**Nodes:**
- PXE boot from BCM
- Download CoreOS installer
- Apply Ignition configuration
- Install OpenShift

### Phase 2: Agent Management

**After Installation:**
1. Waits for nodes to be reachable via SSH
2. Converts nodes from GenericDevice to LiteNode
3. Creates Kubernetes Secret with BCM certificates
4. Deploys bcm-agent via Helm chart (DaemonSet)
5. Verifies agent connectivity

## Usage

### 1. Download Pull Secret

```bash
# Visit https://console.redhat.com/openshift/install/pull-secret
# Download and save to:
cp ~/Downloads/pull-secret.txt ~/pull-secret.json
```

### 2. Update Inventory (if needed)

The inventory at `inventory/openshift_test_cluster.yml` is already configured for the test VMs. Verify:

```yaml
# Pull secret path
openshift_pull_secret_path: "{{ lookup('env', 'HOME') }}/pull-secret.json"

# Nodes match your VMs
cluster_nodes:
  - name: ocp-master-0
    mac: "52:54:00:0C:01:00"
    ip: "10.141.160.50"
    role: master
  # ... etc
```

### 3. Run the Playbook

```bash
cd ~/Work/NVIDIA/BCM/nvidia-bcm-ansible

# Single command - everything is automated!
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/deploy_openshift_cluster.yml
```

## What Happens Behind the Scenes

```
┌─────────────────────────────────────────────────────────┐
│ Ansible Control Node (your machine)                     │
├─────────────────────────────────────────────────────────┤
│ 1. Install openshift-install tool                       │
│ 2. Generate install-config.yaml (with BCM SSH keys)     │
│ 3. Generate agent-config.yaml (with node network config)│
│ 4. Run: openshift-install agent create image            │
│ 5. Copy agent.x86_64.iso → BCM head node                │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ BCM Head Node                                            │
├─────────────────────────────────────────────────────────┤
│ 6. Extract boot files (vmlinuz, initrd, rootfs.img)     │
│ 7. Create PXE categories for master role                │
│ 8. Generate Ignition files with BCM SSH keys            │
│ 9. Register nodes as GenericDevice                      │
│ 10. Power on nodes via Redfish                          │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ OpenShift Nodes (VMs)                                    │
├─────────────────────────────────────────────────────────┤
│ 11. PXE boot from BCM                                    │
│ 12. Download CoreOS installer                           │
│ 13. Apply Ignition (SSH keys, hostname, network)        │
│ 14. Install OpenShift agent-based installer             │
│ 15. Bootstrap cluster                                    │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│ Back to BCM (Phase 2)                                    │
├─────────────────────────────────────────────────────────┤
│ 16. Wait for SSH reachability                           │
│ 17. Convert GenericDevice → LiteNode                    │
│ 18. Deploy bcm-agent Helm chart                         │
│ 19. Agents connect to BCM                               │
│ 20. Apply node labels with hardware inventory           │
└─────────────────────────────────────────────────────────┘
```

## Deployment Timeline

| Step | Duration | What's Happening |
|------|----------|------------------|
| ISO Generation | 2-3 min | openshift-install creates agent ISO |
| ISO Copy | 1 min | ~1GB file transfer to BCM |
| PXE Setup | 1 min | Extract boot files, create categories |
| Node Boot | 5-10 min | PXE boot, CoreOS installation |
| OpenShift Install | 20-30 min | Agent-based installer runs |
| LiteNode Conversion | 1 min | Re-register in BCM |
| Agent Deployment | 2-3 min | Helm chart deployment |
| **Total** | **~30-45 min** | Fully automated |

## Monitoring Progress

### ISO Generation
```bash
# Watch Ansible output - you'll see:
# - openshift-install downloading
# - Configuration files being generated
# - ISO being created
# - ISO being copied to BCM
```

### OpenShift Installation
```bash
# From the control node after playbook completes Phase 1:
export KUBECONFIG=~/openshift/test-ocp/auth/kubeconfig

# Watch nodes join
oc get nodes -w

# Watch cluster operators
oc get clusteroperators -w
```

### BCM Agent
```bash
# SSH to BCM head node
ssh root@192.168.122.204

# Check LiteNode status
cmsh -c 'device; list'

# From control node - check agent pods
oc get pods -n bcm-agent -w
```

## Troubleshooting

### Pull Secret Missing
```
Error: OpenShift pull secret is required but not found
```
**Fix:** Download from https://console.redhat.com/openshift/install/pull-secret and save to `~/pull-secret.json`

### openshift-install Download Fails
```
Error: Failed to download openshift-install
```
**Fix:** Check internet connectivity and OpenShift mirror availability

### ISO Generation Fails
```
Error: Agent ISO was not created
```
**Fix:** Check `~/openshift/test-ocp/` for error logs from `openshift-install`

### Nodes Won't PXE Boot
```bash
# Check BCM categories
cmsh -c 'category; list'

# Verify boot files
ls -la /tftpboot/images/openshift-416-test-ocp-master/

# Test HTTP access
curl http://10.141.255.254:8080/tftpboot/images/openshift-416-test-ocp-master/vmlinuz -I
```

## Configuration Customization

### Different OpenShift Version
```yaml
# inventory/openshift_test_cluster.yml
openshift_version: "4.17"  # Change version
```

### Custom Network Configuration
```yaml
# inventory/openshift_test_cluster.yml
openshift_base_domain: "example.com"
openshift_cluster_network_cidr: "10.128.0.0/14"
openshift_machine_network_cidr: "192.168.1.0/24"
openshift_gateway: "192.168.1.1"
```

### Add Worker Nodes
```yaml
# inventory/openshift_test_cluster.yml
node_roles:
  - name: master
    category: "openshift-416-{{ cluster_name }}-master"
  - name: worker  # Add worker role
    category: "openshift-416-{{ cluster_name }}-worker"

cluster_nodes:
  # ... masters ...
  - name: ocp-worker-0
    mac: "52:54:00:0C:02:00"
    ip: "10.141.160.60"
    role: worker
```

## Benefits of Automated Workflow

1. **No Manual Steps**: Everything from ISO to deployment is automated
2. **Consistent**: Same configuration every time
3. **Version Controlled**: All configs in Git
4. **Repeatable**: Easy to deploy multiple clusters
5. **BCM Integrated**: SSH keys, categories, agent management all handled
6. **Scalable**: Add nodes by updating inventory and re-running

## Next Steps After Deployment

```bash
# Access the cluster
export KUBECONFIG=~/openshift/test-ocp/auth/kubeconfig

# Check cluster
oc get nodes
oc get clusteroperators

# Access web console
oc whoami --show-console

# Get kubeadmin password
cat ~/openshift/test-ocp/auth/kubeadmin-password
```

## Files Generated

**On Ansible Control Node:**
- `~/openshift/test-ocp/install-config.yaml` - Cluster configuration
- `~/openshift/test-ocp/agent-config.yaml` - Node network configuration
- `~/openshift/test-ocp/agent.x86_64.iso` - Generated agent ISO
- `~/openshift/test-ocp/auth/kubeconfig` - Cluster access credentials
- `~/openshift/test-ocp/auth/kubeadmin-password` - Admin password

**On BCM Head Node:**
- `/root/agent.x86_64.iso` - Copied agent ISO
- `/tftpboot/images/installer-openshift-4.16/` - Extracted boot files
- `/tftpboot/ignition/openshift-4.16/test-ocp/master/*.ign` - Generated Ignition files

**Summary:**
Everything is automated - just provide the pull secret and run the playbook!
