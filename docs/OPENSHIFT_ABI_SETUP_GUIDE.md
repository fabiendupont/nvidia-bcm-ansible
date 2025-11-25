# OpenShift Agent-Based Installer with BCM - Setup Guide

This guide walks through deploying OpenShift using the Agent-Based Installer (ABI) with BCM's two-phase approach.

## Architecture Overview

### Two-Phase Deployment

**Phase 1: Installation (GenericDevice with PXE)**
1. Nodes registered as GenericDevice in BCM (enables PXE boot via categories)
2. PXE boot → CoreOS agent installer
3. Ignition deploys BCM SSH keys
4. OpenShift cluster installation completes
5. Categories persist for future node additions

**Phase 2: Agent Management (LiteNode)**
1. Wait for OpenShift installation to complete
2. Convert nodes from GenericDevice to LiteNode
3. Deploy bcm-agent via Helm chart (DaemonSet)
4. Agents connect to BCM for persistent management
5. Node labels applied with hardware inventory

## Prerequisites

### On Your Local Machine

1. **OpenShift Installer**
   ```bash
   # Download from https://console.redhat.com/openshift/downloads
   wget https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable-4.16/openshift-install-linux.tar.gz
   tar xvf openshift-install-linux.tar.gz
   sudo mv openshift-install /usr/local/bin/
   ```

2. **Red Hat Pull Secret**
   - Get from: https://console.redhat.com/openshift/install/pull-secret
   - Save to: `~/pull-secret.json`

3. **SSH Key**
   ```bash
   # Generate if you don't have one
   ssh-keygen -t ed25519 -N '' -f ~/.ssh/id_ed25519
   ```

### On BCM Head Node

1. **BCM Agent Helm Chart**
   - Located at: `/root/nvidia-bcm-lite-daemon/helm/bcm-agent`
   - Or clone from repository

2. **Bootstrap Certificate**
   - Create at: `/cm/local/apps/cmd/etc/bootstrap/cert.pem`
   - Used by agents to initially connect to BCM

## Step 1: Create OpenShift Installer Manifests

Create a directory for your cluster configuration:

```bash
mkdir -p ~/openshift/test-ocp
cd ~/openshift/test-ocp
```

### install-config.yaml

Create `install-config.yaml`:

```yaml
apiVersion: v1
baseDomain: test.local
metadata:
  name: test-ocp

compute:
- architecture: amd64
  hyperthreading: Enabled
  name: worker
  replicas: 0  # Compact cluster - control plane nodes also run workloads

controlPlane:
  architecture: amd64
  hyperthreading: Enabled
  name: master
  replicas: 3

networking:
  clusterNetwork:
  - cidr: 10.128.0.0/14
    hostPrefix: 23
  machineNetwork:
  - cidr: 10.141.0.0/16
  networkType: OVNKubernetes
  serviceNetwork:
  - 172.30.0.0/16

platform:
  none: {}

pullSecret: '<PASTE_YOUR_PULL_SECRET_HERE>'
sshKey: '<PASTE_YOUR_SSH_PUBLIC_KEY_HERE>'
```

### agent-config.yaml

Create `agent-config.yaml`:

```yaml
apiVersion: v1alpha1
kind: AgentConfig
metadata:
  name: test-ocp

rendezvousIP: 10.141.160.50  # First master node IP

hosts:
  - hostname: ocp-master-0
    role: master
    interfaces:
      - name: enp1s0
        macAddress: 52:54:00:0C:01:00
    networkConfig:
      interfaces:
        - name: enp1s0
          type: ethernet
          state: up
          ipv4:
            enabled: true
            address:
              - ip: 10.141.160.50
                prefix-length: 16
            dhcp: false
      dns-resolver:
        config:
          server:
            - 8.8.8.8
      routes:
        config:
          - destination: 0.0.0.0/0
            next-hop-address: 10.141.255.254
            next-hop-interface: enp1s0

  - hostname: ocp-master-1
    role: master
    interfaces:
      - name: enp1s0
        macAddress: 52:54:00:0C:01:01
    networkConfig:
      interfaces:
        - name: enp1s0
          type: ethernet
          state: up
          ipv4:
            enabled: true
            address:
              - ip: 10.141.160.51
                prefix-length: 16
            dhcp: false
      dns-resolver:
        config:
          server:
            - 8.8.8.8
      routes:
        config:
          - destination: 0.0.0.0/0
            next-hop-address: 10.141.255.254
            next-hop-interface: enp1s0

  - hostname: ocp-master-2
    role: master
    interfaces:
      - name: enp1s0
        macAddress: 52:54:00:0C:01:02
    networkConfig:
      interfaces:
        - name: enp1s0
          type: ethernet
          state: up
          ipv4:
            enabled: true
            address:
              - ip: 10.141.160.52
                prefix-length: 16
            dhcp: false
      dns-resolver:
        config:
          server:
            - 8.8.8.8
      routes:
        config:
          - destination: 0.0.0.0/0
            next-hop-address: 10.141.255.254
            next-hop-interface: enp1s0
```

## Step 2: Generate Agent ISO

```bash
cd ~/openshift/test-ocp
openshift-install agent create image
```

This creates `agent.x86_64.iso` containing:
- CoreOS boot image
- Agent installer
- Cluster-specific configuration
- Node-specific Ignition configs

## Step 3: Copy ISO to BCM Head Node

```bash
scp agent.x86_64.iso root@192.168.122.204:/root/
```

## Step 4: Create Test VMs (if not already created)

On your hypervisor host:

```bash
# Create VM disk images
sudo qemu-img create -f qcow2 /var/lib/libvirt/images/ocp-master-0.qcow2 120G
sudo qemu-img create -f qcow2 /var/lib/libvirt/images/ocp-master-1.qcow2 120G
sudo qemu-img create -f qcow2 /var/lib/libvirt/images/ocp-master-2.qcow2 120G

# Create VMs with specific MAC addresses
# (Script to be created - virt-install commands)
```

### VM Requirements

- **CPU**: 4 vCPUs minimum (8 recommended for control plane)
- **Memory**: 16 GB minimum (24 GB recommended for control plane)
- **Disk**: 120 GB minimum
- **Network**: PXE boot enabled, connected to BCM network

## Step 5: Run Ansible Playbook

From this repository:

```bash
cd ~/Work/NVIDIA/BCM/nvidia-bcm-ansible

# Test connectivity to BCM
ansible -i inventory/openshift_test_cluster.yml bcm_headnode -m ping

# Run the deployment playbook
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/deploy_openshift_cluster.yml
```

### What the Playbook Does

**Phase 1:**
1. Extracts boot files from agent ISO (vmlinuz, initrd, rootfs.img)
2. Creates PXE boot categories for master role
3. Generates Ignition configs with BCM SSH keys
4. Registers nodes as GenericDevice with MAC-based Ignition URLs
5. Powers on nodes via Redfish (sushy-emulator)

**Phase 2:**
6. Waits for OpenShift installation to complete (nodes reachable via SSH)
7. Converts nodes from GenericDevice to LiteNode
8. Creates Kubernetes Secret with BCM certificates
9. Deploys bcm-agent Helm chart as DaemonSet
10. Verifies agent connectivity to BCM

## Step 6: Monitor Installation

### From local machine

```bash
# Wait for bootstrap to complete (agent-based is faster)
cd ~/openshift/test-ocp
openshift-install agent wait-for bootstrap-complete

# Wait for installation to complete
openshift-install agent wait-for install-complete
```

### From BCM head node

```bash
# Watch nodes in BCM
cmsh -c 'device; list'

# Check node status
cmsh -c 'device; show ocp-master-0'
```

### Access the cluster

```bash
export KUBECONFIG=~/openshift/test-ocp/auth/kubeconfig

# Check nodes
oc get nodes

# Check cluster operators
oc get clusteroperators

# Check bcm-agent pods
oc get pods -n bcm-agent
```

## Step 7: Verify BCM Agent Integration

```bash
# Check DaemonSet
oc get daemonset -n bcm-agent

# Check logs
oc logs -n bcm-agent -l app.kubernetes.io/name=bcm-agent

# Check node labels from BCM
oc get nodes --show-labels | grep bcm.nvidia.com

# From BCM head node - check LiteNode status
cmsh -c 'device; list'
```

## Troubleshooting

### ISO Extraction Fails

```bash
# Verify ISO on BCM head node
ls -lh /root/agent.x86_64.iso

# Manual extraction test
mkdir -p /tmp/test-iso
mount -o loop /root/agent.x86_64.iso /tmp/test-iso
ls -la /tmp/test-iso/images/pxeboot/
umount /tmp/test-iso
```

### Nodes Won't PXE Boot

```bash
# Check category in BCM
cmsh -c 'category; list'
cmsh -c 'category use openshift-416-test-ocp-master; show'

# Verify HTTP access to boot files
curl http://10.141.255.254:8080/tftpboot/images/openshift-416-test-ocp-master/vmlinuz -I

# Check Ignition files
curl http://10.141.255.254:8080/tftpboot/ignition/openshift-4.16/test-ocp/master/52-54-00-0c-01-00.ign
```

### Installation Hangs

```bash
# Access node console (if using VMs)
virsh console ocp-master-0

# Check OpenShift installer logs
ssh core@10.141.160.50 'sudo journalctl -u bootkube.service'
ssh core@10.141.160.50 'sudo journalctl -u release-image.service'
```

### Agent Won't Connect to BCM

```bash
# Check Secret exists
oc get secret bcm-bootstrap-cert -n bcm-agent

# Check certificate content
oc get secret bcm-bootstrap-cert -n bcm-agent -o yaml

# Check agent logs
oc logs -n bcm-agent daemonset/bcm-agent --tail=100

# From BCM head node
cmsh -c 'device; show ocp-master-0'
```

## Adding Nodes Later

To add a new worker node to the cluster:

1. Update `inventory/openshift_test_cluster.yml`:
   ```yaml
   cluster_nodes:
     # ... existing nodes ...
     - name: ocp-worker-0
       mac: "52:54:00:0C:02:00"
       ip: "10.141.160.60"
       role: worker
   ```

2. Update `agent-config.yaml` and regenerate ISO (or use existing if network config compatible)

3. Re-run playbook (categories will be reused):
   ```bash
   ansible-playbook -i inventory/openshift_test_cluster.yml \
     playbooks/deploy_openshift_cluster.yml
   ```

4. The new node will:
   - Use existing PXE category
   - Boot and install OpenShift
   - Automatically convert to LiteNode
   - Join the cluster (agent already running)

## Architecture Benefits

- **Scalable**: PXE categories persist for future node additions
- **Clean Separation**: Installation (PXE) and management (agent) are decoupled
- **BCM Integration**: Nodes appear in BCM with full lifecycle management
- **Kubernetes-Native**: Agent runs as DaemonSet, integrates with OpenShift
- **Hardware Inventory**: BCM agent labels nodes with hardware details

## Next Steps

- Configure persistent storage
- Set up monitoring and logging
- Deploy workloads
- Configure Redfish BMC addresses in BCM for real hardware
- Test node scaling and lifecycle operations
