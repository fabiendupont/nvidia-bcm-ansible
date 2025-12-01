# Role: registry_setup

Setup and manage container registry on BCM head node using systemd quadlets.

## Purpose

Deploys a Podman-based container registry as a systemd service using quadlets. Handles TLS certificate generation signed by BCM CA, ensuring cluster nodes trust the registry.

## Requirements

- Podman installed on BCM head node
- BCM certificate authority configured
- Systemd with quadlet support

## Required Variables

None - all variables have defaults.

## Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `registry_port` | `5000` | Registry listen port |
| `registry_hostname` | `{{ ansible_fqdn }}` | Registry hostname |
| `registry_data_dir` | `/var/lib/bcm-registry` | Persistent image storage |
| `bcm_ca_cert` | `/cm/local/apps/cmd/etc/temporary_cacert.pem` | BCM CA certificate |
| `bcm_ca_key` | `/cm/local/apps/cmd/etc/temporary_cacert.key` | BCM CA key |

## What It Does

1. Generates TLS certificate signed by BCM CA
2. Creates registry data directory
3. Deploys systemd quadlet configuration
4. Starts and enables registry service
5. Waits for registry to be ready
6. Verifies health endpoint

## Example Usage

```yaml
# Default configuration
- include_role:
    name: fabiendupont.bcm.registry_setup

# Custom port
- include_role:
    name: fabiendupont.bcm.registry_setup
  vars:
    registry_port: 8443
```

## Registry Access

After deployment:
- **URL**: `https://{{ registry_hostname }}:{{ registry_port }}`
- **Certificate**: Signed by BCM CA (trusted by cluster nodes)
- **Storage**: `/var/lib/bcm-registry` (persistent across restarts)

## Dependencies

- containers.podman collection

## Notes

- Uses systemd quadlets for reliable service management
- Automatic restart on failure
- Health check monitoring
- Certificate automatically includes FQDN and short hostname
