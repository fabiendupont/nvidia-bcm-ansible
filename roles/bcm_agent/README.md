# Ansible Role: bcm_agent

Deploy NVIDIA BCM Agent on RHEL systems using Podman Quadlet.

## Description

This role deploys the BCM Agent as a systemd service using Podman Quadlet. The BCM Agent integrates NVIDIA Base Command Manager (BCM) with standalone RHEL servers or OpenShift/Kubernetes nodes, providing:

- **Hardware monitoring** via cm-lite-daemon
- **Two-way BCM synchronization** via WebSocket
- **Prometheus metrics** export
- **Automatic service management** via systemd

## Requirements

- RHEL 9.0 or compatible
- Podman 4.4+ (for Quadlet support)
- Ansible 2.14+
- BCM head node accessible on the network
- BCM certificates for authentication

### Ansible Collections

- `containers.podman` (for container management)

Install with:
```bash
ansible-galaxy collection install containers.podman
```

## Role Variables

### Container Configuration

```yaml
# Container image
bcm_agent_image_repository: "quay.io/nvidia/bcm-agent"
bcm_agent_image_tag: "1.0.0"
bcm_agent_pull_policy: "always"  # Options: always, missing, never
```

### BCM Configuration

```yaml
# BCM head node
bcm_agent_bcm_host: "bcmhead"
bcm_agent_bcm_port: 8081
```

### Certificate Configuration

```yaml
# Certificate source and destination
bcm_agent_cert_source: "/cm/local/apps/cm-lite-daemon/etc"
bcm_agent_cert_dest: "/etc/bcm-agent/certs"
bcm_agent_cert_method: "symlink"  # Options: copy, symlink
```

**Note**: The certificate source must contain `cacert.pem`, `cert.pem`, and `cert.key`.

### Monitoring Configuration

```yaml
# Monitoring settings
bcm_agent_sync_interval: 300  # Label sync interval (seconds)
bcm_agent_label_prefix: "bcm.nvidia.com"
bcm_agent_metrics_port: 9100  # Prometheus metrics port
```

### Logging Configuration

```yaml
# Logging
bcm_agent_log_level: "info"  # Options: debug, info, warning, error
bcm_agent_log_dir: "/var/log/bcm-agent"
bcm_agent_debug: false
```

### Resource Limits

```yaml
# Resource constraints
bcm_agent_memory_high: "488M"
bcm_agent_memory_max: "512M"
bcm_agent_tasks_max: 128
```

### Service Configuration

```yaml
# Service state
bcm_agent_state: "present"  # Options: present, absent
bcm_agent_enabled: true
bcm_agent_started: true

# Service behavior
bcm_agent_restart_policy: "always"
bcm_agent_restart_sec: 10
bcm_agent_timeout_start_sec: 300
bcm_agent_timeout_stop_sec: 45
```

### Auto-Update Configuration

```yaml
# Podman auto-update
bcm_agent_auto_update: false  # Enable automatic image updates
```

When enabled, Podman will automatically check for and pull new image versions.

## Dependencies

None.

## Example Playbook

### Basic Deployment

```yaml
---
- name: Deploy BCM Agent
  hosts: compute_nodes
  become: true
  roles:
    - role: fabiendupont.bcm.bcm_agent
```

### Custom Configuration

```yaml
---
- name: Deploy BCM Agent with custom settings
  hosts: gpu_nodes
  become: true
  roles:
    - role: fabiendupont.bcm.bcm_agent
      vars:
        bcm_agent_image_tag: "1.0.1"
        bcm_agent_bcm_host: "bcm-primary.example.com"
        bcm_agent_bcm_port: 8081
        bcm_agent_cert_method: "copy"
        bcm_agent_debug: true
        bcm_agent_sync_interval: 60
```

### Deploy to BCM Compute Nodes

```yaml
---
- name: Deploy BCM Agent on managed nodes
  hosts: bcm_compute
  become: true
  roles:
    - role: fabiendupont.bcm.bcm_agent
      vars:
        bcm_agent_cert_source: "/cm/local/apps/cm-lite-daemon/etc"
        bcm_agent_cert_method: "symlink"
```

### Enable Auto-Update

```yaml
---
- name: Deploy BCM Agent with auto-updates
  hosts: all
  become: true
  roles:
    - role: fabiendupont.bcm.bcm_agent
      vars:
        bcm_agent_auto_update: true
```

### Remove BCM Agent

```yaml
---
- name: Remove BCM Agent
  hosts: old_nodes
  become: true
  roles:
    - role: fabiendupont.bcm.bcm_agent
      vars:
        bcm_agent_state: "absent"
```

## Usage

### Deploy to a Single Host

```bash
ansible-playbook -i inventory.yml deploy-bcm-agent.yml --limit node001
```

### Deploy to All Hosts

```bash
ansible-playbook -i inventory.yml deploy-bcm-agent.yml
```

### Check Status

```bash
ansible all -i inventory.yml -b -m shell -a "systemctl status bcm-agent.service"
```

### View Logs

```bash
ansible all -i inventory.yml -b -m shell -a "journalctl -u bcm-agent.service -n 50"
```

### Test Metrics

```bash
ansible all -i inventory.yml -b -m shell -a "curl -s http://localhost:9100/metrics | grep bcm_"
```

## Post-Deployment Verification

After deployment, verify the BCM Agent is running:

```bash
# Check service status
systemctl status bcm-agent.service

# View logs
journalctl -u bcm-agent.service -f

# Check container
podman ps | grep bcm-agent

# Verify BCM connection
tail -f /var/log/bcm-agent/cm-lite-daemon.log

# Test Prometheus metrics
curl http://localhost:9100/metrics
```

## Troubleshooting

### Service fails to start

```bash
# Check systemd unit
systemctl cat bcm-agent.service

# View detailed status
systemctl status bcm-agent.service -l

# Check container logs
podman logs bcm-agent
```

### Certificate errors

```bash
# Verify certificates exist
ls -l /etc/bcm-agent/certs/

# Check certificate validity
openssl x509 -in /etc/bcm-agent/certs/cert.pem -text -noout
```

### Cannot connect to BCM

```bash
# Test network connectivity
podman exec bcm-agent ping -c 3 bcmhead
podman exec bcm-agent nc -zv bcmhead 8081

# View cm-lite-daemon logs
tail -100 /var/log/bcm-agent/cm-lite-daemon.log
```

## Integration with Kubernetes/OpenShift

This role is designed for standalone RHEL deployments. For Kubernetes/OpenShift clusters, use the Helm chart instead:

```bash
helm install bcm-agent ./helm/bcm-agent \
  --namespace bcm-agent \
  --create-namespace
```

However, you can use both approaches together:
- **Ansible role** - Deploy on BCM head node and standalone servers
- **Helm chart** - Deploy on Kubernetes/OpenShift cluster nodes

## License

GPL-3.0-or-later

## Author Information

NVIDIA Corporation

## See Also

- [BCM Agent Main Documentation](../../bcm-agent/README.md)
- [Podman Quadlet Documentation](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html)
- [NVIDIA BCM Documentation](https://docs.nvidia.com/base-command-manager/)
