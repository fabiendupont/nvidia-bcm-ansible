# Testing BCM Deployments with Virtual Machines

This document describes the common infrastructure for testing BCM deployments using libvirt VMs and Sushy Emulator for Redfish power management.

## Overview

This testing approach works for:
- RHEL deployment with kickstart
- OpenShift cluster deployment
- Any PXE-based node provisioning

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│ Hypervisor Host (Fedora/RHEL with libvirt)                      │
│                                                                 │
│  ┌──────────────────┐    ┌──────────────────┐                   │
│  │ BCM Head Node VM │    │ Test Node VMs    │                   │
│  │ (192.168.122.204)│    │ (PXE boot)       │                   │
│  └────────┬─────────┘    └────────┬─────────┘                   │
│           │                       │                             │
│           └───────────┬───────────┘                             │
│                       │                                         │
│              ┌────────┴────────┐                                │
│              │ bcm-internalnet │                                │
│              │ (10.141.0.0/16) │                                │
│              └─────────────────┘                                │
│                                                                 │
│  ┌─────────────────────────────────────────┐                    │
│  │ Sushy Emulator (HTTPS on 192.168.122.1) │                    │
│  │ Provides Redfish API for VM power mgmt  │                    │
│  └─────────────────────────────────────────┘                    │
└─────────────────────────────────────────────────────────────────┘
```

## Sushy Emulator Setup

### Create SSL Certificate

```bash
sudo mkdir -p /etc/sushy-emulator/ssl
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/sushy-emulator/ssl/sushy.key \
  -out /etc/sushy-emulator/ssl/sushy.crt \
  -subj "/C=US/ST=CA/L=SantaClara/O=Lab/CN=192.168.122.1"
```

### Create Configuration

```bash
sudo cat > /etc/sushy-emulator/sushy-emulator.conf <<'EOF'
SUSHY_EMULATOR_LISTEN_IP = "0.0.0.0"
SUSHY_EMULATOR_LISTEN_PORT = 443
SUSHY_EMULATOR_SSL_CERT = "/etc/sushy-emulator/ssl/sushy.crt"
SUSHY_EMULATOR_SSL_KEY = "/etc/sushy-emulator/ssl/sushy.key"
SUSHY_EMULATOR_LIBVIRT_URI = "qemu:///system"
EOF
```

### Create Systemd Service

**IMPORTANT**: Do NOT use `:Z` flag for volume mounts - it relabels libvirt sockets and breaks virtualization!

```bash
sudo cat > /etc/systemd/system/sushy-emulator.service <<'EOF'
[Unit]
Description=Sushy Redfish Emulator for Libvirt
After=network-online.target virtqemud.socket
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
EOF
```

### Start Service

```bash
sudo firewall-cmd --zone=libvirt --add-port=443/tcp --permanent
sudo firewall-cmd --reload
sudo systemctl daemon-reload
sudo systemctl enable --now sushy-emulator
```

### Verify

```bash
curl -sk https://192.168.122.1/redfish/v1/Systems | python3 -m json.tool
```

## Creating Test VMs

### VM Configuration Rules

| Setting | Value | Reason |
|---------|-------|--------|
| Boot order | `hd,network` | Disk first prevents installer loop after installation |
| Graphics | `spice` | Visual console for monitoring |
| Network | `bcm-internalnet` | BCM provisioning network |
| MAC address | Fixed, known | Must match BCM node configuration |

### Create VM

```bash
virt-install \
  --connect qemu:///system \
  --name <vm-name> \
  --ram 4096 \
  --vcpus 2 \
  --disk size=20 \
  --network network=bcm-internalnet,mac=<mac-address> \
  --pxe \
  --graphics spice \
  --noautoconsole \
  --boot hd,network \
  --osinfo rhel9.0
```

### Get VM UUID

```bash
virsh -c qemu:///system domuuid <vm-name>
```

## BCM Node Configuration

### Set MAC Address

```bash
cmsh -c "device use <node-name>; set mac <mac-address>; commit"
```

### Set Install Mode

```bash
cmsh -c "device use <node-name>; set installmode FULL; commit"
```

### Create MAC-Specific PXE Config

BCM uses category PXE configs by default. For testing, create MAC-specific symlink:

```bash
# MAC format: 01-<mac-with-dashes-lowercase>
# Example: 52:54:00:11:11:01 -> 01-52-54-00-11-11-01
ln -sf category.<category-name> /tftpboot/pxelinux.cfg/01-<mac-address>
```

## Power Management via Redfish

### Power On

```bash
curl -sk -X POST "https://192.168.122.1/redfish/v1/Systems/<vm-uuid>/Actions/ComputerSystem.Reset" \
  -H "Content-Type: application/json" \
  -d '{"ResetType": "On"}'
```

### Power Off

```bash
curl -sk -X POST "https://192.168.122.1/redfish/v1/Systems/<vm-uuid>/Actions/ComputerSystem.Reset" \
  -H "Content-Type: application/json" \
  -d '{"ResetType": "ForceOff"}'
```

### Check Power State

```bash
curl -sk "https://192.168.122.1/redfish/v1/Systems/<vm-uuid>" | grep PowerState
```

## Monitoring

### VM Console

```bash
virt-viewer -c qemu:///system <vm-name>
```

### DHCP Logs

```bash
ssh root@<bcm-headnode> 'tail -f /var/log/messages | grep -i dhcp'
```

### Node Status

```bash
ssh root@<bcm-headnode> 'cmsh -c "device use <node-name>; status"'
```

## Cleanup

```bash
# Stop and delete VM
virsh -c qemu:///system destroy <vm-name>
virsh -c qemu:///system undefine <vm-name> --remove-all-storage

# Remove PXE config
ssh root@<bcm-headnode> 'rm -f /tftpboot/pxelinux.cfg/01-<mac-address>'

# Reset install mode
ssh root@<bcm-headnode> 'cmsh -c "device use <node-name>; set installmode NOSYNC; commit"'
```

## Troubleshooting

### Node Boots Wrong Image

1. Check MAC address matches: `cmsh -c "device use <node>; get mac"`
2. Check PXE config exists: `ls /tftpboot/pxelinux.cfg/01-<mac>`
3. Check install mode: `cmsh -c "device use <node>; get installmode"`

### Installer Loops

Boot order wrong. Fix with:
```bash
virt-xml <vm-name> -c qemu:///system --edit --boot hd,network
```

### Sushy "client socket is closed"

Restart libvirt and Sushy:
```bash
sudo systemctl restart virtqemud.socket
sudo systemctl restart sushy-emulator
```

### SELinux Issues After Sushy

If Sushy was started with `:Z` flags:
```bash
sudo restorecon -FRv /var/run/libvirt
sudo systemctl restart virtqemud.socket
```

## Platform Notes

### Fedora 35+

Uses modular libvirt daemons (`virtqemud`, `virtnetworkd`, etc.) instead of monolithic `libvirtd`. The Sushy service file should depend on `virtqemud.socket`.

### SELinux

Never use `:Z` flag when mounting `/var/run/libvirt` in containers - it relabels sockets and breaks virtualization.
