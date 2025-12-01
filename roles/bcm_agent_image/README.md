# Role: bcm_agent_image

Build and optionally push the BCM agent container image to a registry.

## Purpose

Provides a reusable workflow for building the BCM agent container image from the nvidia-bcm-lite-daemon repository and optionally pushing it to a container registry. Used by both OpenShift and RHEL deployments.

## Requirements

- Podman installed on the BCM head node
- Access to git repository (nvidia-bcm-lite-daemon)
- Container registry running (if push enabled)

## Required Variables

None - all variables have defaults.

## Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `bcm_agent_local_image` | `localhost/bcm-agent` | Local image name |
| `bcm_agent_local_tag` | `latest` | Image tag |
| `bcm_agent_repo_url` | (see defaults) | Git repository URL |
| `bcm_agent_repo_path` | `/root/nvidia-bcm-lite-daemon` | Local clone path |
| `bcm_agent_repo_version` | `main` | Git branch/tag |
| `bcm_agent_force_rebuild` | `false` | Force rebuild even if image exists |
| `bcm_agent_push_to_registry` | `false` | Enable registry push |
| `bcm_agent_registry_host` | `""` | Registry host:port (if push enabled) |
| `bcm_agent_registry_image` | `""` | Image name in registry |
| `bcm_agent_registry_tag` | `{{ bcm_agent_local_tag }}` | Tag in registry |
| `bcm_agent_registry_validate_certs` | `false` | Validate registry TLS |

## Example Usage

```yaml
# Build only
- include_role:
    name: fabiendupont.bcm.bcm_agent_image

# Build and push to registry
- include_role:
    name: fabiendupont.bcm.bcm_agent_image
  vars:
    bcm_agent_push_to_registry: true
    bcm_agent_registry_host: "registry.example.com:5000"
    bcm_agent_registry_image: "bcm-agent"
```

## Dependencies

- containers.podman collection

## Notes

- Image build is idempotent - skips if image already exists (unless force_rebuild=true)
- Registry push includes automatic retries (3 attempts)
- Compatible with both OpenShift and RHEL deployment workflows
