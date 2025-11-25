#!/bin/bash
#
# Create test VMs for OpenShift cluster deployment via BCM
#
# This script creates VMs with specific MAC addresses and network configuration
# for testing the OpenShift Agent-Based Installer with BCM's two-phase approach

set -euo pipefail

# Configuration
CLUSTER_NAME="test-ocp"
NETWORK_NAME="nvidia-bcm-internal"  # BCM internal network
STORAGE_POOL="/var/lib/libvirt/images"
OS_VARIANT="rhel9.0"  # CoreOS is RHEL-based

# Control plane nodes configuration
declare -A MASTERS=(
    ["ocp-master-0"]="52:54:00:0C:01:00"
    ["ocp-master-1"]="52:54:00:0C:01:01"
    ["ocp-master-2"]="52:54:00:0C:01:02"
)

# Resource allocation (for control plane nodes)
VCPUS=8
MEMORY=32768  # 32 GB in MB (required for Agent-Based Installer PXE boot)
DISK_SIZE=120  # GB

# Colors for output
RED='\033[0:31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    error "This script must be run as root (use sudo)"
fi

# Check if libvirt is running (modular daemons on Fedora 43+)
if ! systemctl is-active --quiet virtqemud.socket; then
    log "Starting virtqemud.socket..."
    systemctl start virtqemud.socket
fi

# Check if network exists
if ! virsh net-info "$NETWORK_NAME" &>/dev/null; then
    warn "Network $NETWORK_NAME not active, starting it..."
    virsh net-start "$NETWORK_NAME"
fi

log "Creating OpenShift test VMs for cluster: $CLUSTER_NAME"
log "========================================================"
log "VCPUs: $VCPUS"
log "Memory: $((MEMORY / 1024)) GB"
log "Disk: ${DISK_SIZE} GB"
log "Network: $NETWORK_NAME"
log "========================================================"

# Create VMs
for vm_name in "${!MASTERS[@]}"; do
    mac_addr="${MASTERS[$vm_name]}"
    disk_path="${STORAGE_POOL}/${vm_name}.qcow2"

    log "Creating VM: $vm_name (MAC: $mac_addr)"

    # Check if VM already exists
    if virsh list --all | grep -q " $vm_name "; then
        warn "VM $vm_name already exists, skipping..."
        continue
    fi

    # Check if disk already exists
    if [ -f "$disk_path" ]; then
        warn "Disk $disk_path already exists, removing..."
        rm -f "$disk_path"
    fi

    # Create disk image
    log "  Creating disk: $disk_path"
    qemu-img create -f qcow2 "$disk_path" "${DISK_SIZE}G" >/dev/null

    # Create VM
    log "  Creating VM definition..."
    virt-install \
        --name "$vm_name" \
        --memory "$MEMORY" \
        --vcpus "$VCPUS" \
        --disk path="$disk_path",format=qcow2,bus=virtio \
        --network network="$NETWORK_NAME",mac="$mac_addr",model=virtio \
        --os-variant "$OS_VARIANT" \
        --graphics spice,listen=127.0.0.1 \
        --video qxl \
        --channel spicevmc,target_type=virtio \
        --console pty,target_type=serial \
        --boot hd,network \
        --noautoconsole \
        --pxe \
        --wait=-1 &

    # Wait a bit to avoid overwhelming the system
    sleep 2
done

# Wait for all virt-install processes to complete
log "Waiting for VM creation to complete..."
wait

log ""
log "========================================================"
log "OpenShift VMs Created Successfully!"
log "========================================================"
log ""
log "VM List:"
virsh list --all | grep "$CLUSTER_NAME\|ocp-"

log ""
log "Next steps:"
log "1. Generate OpenShift agent ISO (see docs/OPENSHIFT_ABI_SETUP_GUIDE.md)"
log "2. Copy ISO to BCM head node"
log "3. Run deployment playbook:"
log "   ansible-playbook -i inventory/openshift_test_cluster.yml \\"
log "     playbooks/deploy_openshift_cluster.yml"
log ""
log "VM Management Commands:"
log "  List VMs:     virsh list --all"
log "  Start VM:     virsh start <vm-name>"
log "  Stop VM:      virsh destroy <vm-name>"
log "  Delete VM:    virsh undefine <vm-name> --remove-all-storage"
log "  Console:      virsh console <vm-name> (Ctrl+] to exit)"
log ""
log "Sushy Redfish Endpoints (for BCM power management):"
for vm_name in "${!MASTERS[@]}"; do
    uuid=$(virsh domuuid "$vm_name" 2>/dev/null || echo "NOT_CREATED")
    if [ "$uuid" != "NOT_CREATED" ]; then
        log "  $vm_name: http://192.168.1.51:8000/redfish/v1/Systems/$uuid"
    fi
done
log ""
log "Configure in BCM (from BCM head node):"
log "  cmsh -c \"device use <vm-name>; set bmc http://192.168.1.51:8000/redfish/v1/Systems/<vm-uuid>\""
