# Register bcm-rhel VM with BCM

This playbook registers the RHEL VM `bcm-rhel` (10.141.255.253) with BCM and deploys the BCM Agent.

## What it does

1. **Prepares the VM**
   - Installs Podman 4.4+ (required for Quadlet)
   - Installs hardware monitoring tools (ipmitool, dmidecode, etc.)

2. **Registers with BCM**
   - Creates node `bcm-rhel` in BCM
   - Sets MAC address: `52:54:00:08:db:92`
   - Sets IP address: `10.141.255.253`
   - Assigns to network: `internalnet`
   - Adds role: `compute`

3. **Deploys BCM Agent**
   - Pulls container image `quay.io/nvidia/bcm-agent:1.0.0`
   - Creates Quadlet systemd service
   - Configures certificates from `/cm/local/apps/cm-lite-daemon/etc`
   - Starts BCM Agent service

## Quick Start

### Option 1: Run the wrapper script

```bash
cd ansible_collections/fabiendupont/bcm/playbooks
./run-register-bcm-rhel.sh
```

### Option 2: Run ansible-playbook directly

```bash
cd ansible_collections/fabiendupont/bcm/playbooks

ansible-playbook \
  -i bcm-rhel-inventory.yml \
  register-bcm-rhel.yml
```

## Files

- **`bcm-rhel-inventory.yml`** - Ansible inventory with VM details
- **`register-bcm-rhel.yml`** - Main playbook
- **`run-register-bcm-rhel.sh`** - Wrapper script for easy execution

## Prerequisites

- SSH access to bcm-rhel (root@10.141.255.253)
- BCM head node accessible (runs cmsh commands via `delegate_to`)
- BCM certificates available at `/cm/local/apps/cm-lite-daemon/etc/`

## Verification

After deployment, verify:

### On BCM head node:

```bash
# Check node in BCM
cmsh -c "device; show bcm-rhel"

# Check roles
cmsh -c "device; use bcm-rhel; roles; list"
```

### On bcm-rhel VM:

```bash
# Check service status
ssh root@10.141.255.253 "systemctl status bcm-agent.service"

# Check logs
ssh root@10.141.255.253 "journalctl -u bcm-agent.service -n 50"

# Check container
ssh root@10.141.255.253 "podman ps | grep bcm-agent"

# Check metrics
ssh root@10.141.255.253 "curl -s http://localhost:9100/metrics | head -20"

# Check cm-lite-daemon connection
ssh root@10.141.255.253 "tail -f /var/log/bcm-agent/cm-lite-daemon.log"
```

## Customization

Edit `bcm-rhel-inventory.yml` to customize:

```yaml
# BCM node settings
bcm_node_category: "gpu"      # Change category
bcm_node_roles:               # Add more roles
  - compute
  - gpu
  - storage

# BCM Agent settings
bcm_agent_image_tag: "1.0.1"  # Use different image
bcm_agent_debug: true          # Enable debug logging
bcm_agent_sync_interval: 60    # More frequent sync
```

## Troubleshooting

### Podman installation fails

```bash
# Manually install Podman on bcm-rhel
ssh root@10.141.255.253 "dnf install -y podman"
```

### Node already exists in BCM

The playbook will update the existing node instead of creating a new one.

### BCM Agent fails to connect

```bash
# Check network connectivity
ssh root@10.141.255.253 "ping -c 3 bcmhead"

# Check certificates
ssh root@10.141.255.253 "ls -l /etc/bcm-agent/certs/"

# View detailed logs
ssh root@10.141.255.253 "journalctl -u bcm-agent.service -f"
```

### Certificate not found

Make sure BCM certificates exist on the BCM head node:

```bash
ls -l /cm/local/apps/cm-lite-daemon/etc/
# Should show: cacert.pem, cert.pem, cert.key
```

## Next Steps

After successful registration:

1. **Add to OpenShift cluster** - If bcm-rhel will be an OpenShift node
2. **Configure monitoring** - Set up Prometheus scraping
3. **Firmware management** - Use BCM to track and update firmware
4. **Deploy workloads** - Schedule pods using BCM-based node labels

## See Also

- [BCM Agent Role Documentation](../roles/bcm_agent/README.md)
- [BCM Agent Main README](/root/bcm/bcm-agent/README.md)
- [General Registration Playbook](register-and-deploy-bcm-agent.yml)
