# Sushy-Tools Redfish Emulator Setup

Sushy-tools provides a Redfish API emulator for libvirt VMs, allowing BCM to manage virtual machines via the standard Redfish protocol. This is useful for testing and development environments.

## Overview

Sushy-tools runs as a containerized service that:
- Exposes libvirt VMs as Redfish endpoints
- Provides standard Redfish API for power management
- Maps VM UUIDs to Redfish system endpoints
- Enables BCM to manage VMs without direct libvirt access

## Prerequisites

- Podman or Docker installed
- Libvirt running with VMs
- Access to quay.io/metal3-io/sushy-tools container image

## Automated Setup

Use the provided playbook for automated setup:

```bash
ansible-playbook -i inventory/openshift_test_cluster.yml \
  playbooks/setup_sushy_emulator.yml
```

The playbook will:
1. Pull the sushy-tools container image
2. Create systemd service unit
3. Configure libvirt access
4. Start and enable the service
5. Display VM to Redfish endpoint mappings

## Manual Setup

### 1. Create Sushy Configuration File

Create `/etc/sushy-emulator/sushy-emulator.conf`:

```python
SUSHY_EMULATOR_LISTEN_IP = "0.0.0.0"
SUSHY_EMULATOR_LISTEN_PORT = 8000
SUSHY_EMULATOR_LIBVIRT_URI = "qemu:///system"
```

```bash
sudo mkdir -p /etc/sushy-emulator
sudo cat > /etc/sushy-emulator/sushy-emulator.conf <<'EOF'
SUSHY_EMULATOR_LISTEN_IP = "0.0.0.0"
SUSHY_EMULATOR_LISTEN_PORT = 8000
SUSHY_EMULATOR_LIBVIRT_URI = "qemu:///system"
EOF
```

### 2. Create Systemd Service

Create `/etc/systemd/system/sushy-emulator.service`:

```ini
[Unit]
Description=Sushy Redfish Emulator for Libvirt
After=network-online.target libvirtd.service
Wants=network-online.target

[Service]
Type=simple
Restart=always
RestartSec=10
ExecStartPre=-/usr/bin/podman kill sushy-emulator
ExecStartPre=-/usr/bin/podman rm sushy-emulator
ExecStart=/usr/bin/podman run --rm --name sushy-emulator \
  --net=host \
  --privileged \
  -v /var/run/libvirt:/var/run/libvirt \
  -v /etc/sushy-emulator:/etc/sushy-emulator:ro \
  quay.io/metal3-io/sushy-tools:latest \
  sushy-emulator --config /etc/sushy-emulator/sushy-emulator.conf
ExecStop=/usr/bin/podman stop sushy-emulator

[Install]
WantedBy=multi-user.target
```

### 3. Configure Firewall

Allow port 8000 in the libvirt firewall zone:

```bash
sudo firewall-cmd --zone=libvirt --add-port=8000/tcp
sudo firewall-cmd --zone=libvirt --add-port=8000/tcp --permanent
```

### 4. Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable sushy-emulator
sudo systemctl start sushy-emulator
```

### 3. Verify Service

```bash
# Check service status
sudo systemctl status sushy-emulator

# View logs
sudo journalctl -u sushy-emulator -f

# Test Redfish API
curl http://localhost:8000/redfish/v1/ | python3 -m json.tool
```

## Usage

### List All Systems (VMs)

```bash
curl http://localhost:8000/redfish/v1/Systems | python3 -m json.tool
```

### Get VM UUID

Find your VM's UUID:

```bash
virsh list --all
virsh domuuid <vm-name>
```

### Get VM Details via Redfish

```bash
VM_UUID=$(virsh domuuid <vm-name>)
curl http://localhost:8000/redfish/v1/Systems/${VM_UUID} | python3 -m json.tool
```

### Power Operations

#### Power On

```bash
VM_UUID=$(virsh domuuid <vm-name>)
curl -X POST http://localhost:8000/redfish/v1/Systems/${VM_UUID}/Actions/ComputerSystem.Reset \
  -H "Content-Type: application/json" \
  -d '{"ResetType": "On"}'
```

#### Power Off

```bash
VM_UUID=$(virsh domuuid <vm-name>)
curl -X POST http://localhost:8000/redfish/v1/Systems/${VM_UUID}/Actions/ComputerSystem.Reset \
  -H "Content-Type: application/json" \
  -d '{"ResetType": "ForceOff"}'
```

#### Graceful Shutdown

```bash
VM_UUID=$(virsh domuuid <vm-name>)
curl -X POST http://localhost:8000/redfish/v1/Systems/${VM_UUID}/Actions/ComputerSystem.Reset \
  -H "Content-Type: application/json" \
  -d '{"ResetType": "GracefulShutdown"}'
```

#### Power Cycle

```bash
VM_UUID=$(virsh domuuid <vm-name>)
curl -X POST http://localhost:8000/redfish/v1/Systems/${VM_UUID}/Actions/ComputerSystem.Reset \
  -H "Content-Type: application/json" \
  -d '{"ResetType": "ForceRestart"}'
```

## Integration with BCM

### Configure BCM to Use Redfish

In BCM, configure your VMs to use Redfish for power management:

1. **Get VM UUID**: `virsh domuuid <vm-name>`
2. **Redfish Endpoint**: `http://<host-ip>:8000/redfish/v1/Systems/<VM_UUID>`
3. **Configure in BCM**: Set up chassis/power management with Redfish endpoint

Example using BCM modules:

```yaml
- name: Configure VM chassis with Redfish
  brightcomputing.bcm110.chassis:
    name: "vm-chassis-{{ vm_name }}"
    state: present
    hostname: "<host-ip>"
    port: 8000
    protocol: "REDFISH"
    # Additional Redfish configuration
```

## Troubleshooting

### Service Won't Start

Check logs for errors:
```bash
sudo journalctl -u sushy-emulator -n 50
```

Common issues:
- **Libvirt not running**: `sudo systemctl status libvirtd`
- **Port 8000 in use**: `sudo ss -tlnp | grep 8000`
- **Container image pull failed**: `podman pull quay.io/metal3-io/sushy-tools:latest`

### SELinux

**WARNING**: Do NOT use the `:Z` flag when mounting `/var/run/libvirt`. This flag relabels libvirt sockets to `container_file_t`, breaking virtualization and preventing VMs from starting.

If you accidentally used `:Z` and libvirt is broken, restore the correct labels:
```bash
sudo restorecon -FRv /var/run/libvirt
sudo systemctl restart virtqemud.socket  # Fedora 35+ / modular daemons
```

The `--privileged` flag provides sufficient access for Sushy to communicate with libvirt.

### VMs Not Appearing

Verify libvirt connection:
```bash
# Test libvirt connection
virsh -c qemu:///system list --all

# Check if VMs are accessible to sushy
curl http://localhost:8000/redfish/v1/Systems
```

### Power Operations Not Working

Check VM state and libvirt permissions:
```bash
# Check VM state
virsh list --all

# Verify sushy container has libvirt access
podman exec sushy-emulator ls -la /var/run/libvirt/
```

## Configuration Options

### Change Port

Modify the systemd service to use a different port:

```ini
ExecStart=/usr/bin/podman run --rm --name sushy-emulator \
  --net=host \
  --privileged \
  -v /var/run/libvirt:/var/run/libvirt \
  quay.io/metal3-io/sushy-tools:latest \
  sushy-emulator --port 8080 --libvirt-uri qemu:///system
```

Then reload and restart:
```bash
sudo systemctl daemon-reload
sudo systemctl restart sushy-emulator
```

### Enable Authentication

For basic authentication, add environment variables:

```ini
ExecStart=/usr/bin/podman run --rm --name sushy-emulator \
  --net=host \
  --privileged \
  -v /var/run/libvirt:/var/run/libvirt \
  -e SUSHY_EMULATOR_AUTH_FILE=/etc/sushy/auth.conf \
  quay.io/metal3-io/sushy-tools:latest \
  sushy-emulator --port 8000 --libvirt-uri qemu:///system
```

## Service Management

### Check Status

```bash
sudo systemctl status sushy-emulator
```

### View Logs

```bash
# Follow logs in real-time
sudo journalctl -u sushy-emulator -f

# View recent logs
sudo journalctl -u sushy-emulator -n 100
```

### Restart Service

```bash
sudo systemctl restart sushy-emulator
```

### Stop Service

```bash
sudo systemctl stop sushy-emulator
```

### Disable Service

```bash
sudo systemctl disable sushy-emulator
```

## References

- [Sushy-tools Documentation](https://docs.openstack.org/sushy-tools/latest/)
- [Redfish API Specification](https://www.dmtf.org/standards/redfish)
- [Metal3 Sushy-tools Container](https://quay.io/repository/metal3-io/sushy-tools)
- [BCM Power Management Guide](https://support.nvidia.com/bcm)

## Related Playbooks

- `playbooks/setup_sushy_emulator.yml` - Automated setup
- `playbooks/deploy_openshift_cluster.yml` - Uses Redfish for VM management
