# Role: pythoncm_setup

Setup pythoncm library from BCM head node for dynamic inventory plugin usage.

## Purpose

Builds a Python wheel from the BCM head node's pythoncm installation and installs it in the local Python environment. This enables the `brightcomputing.bcm110.bright_nodes` dynamic inventory plugin to query BCM for node information.

## Requirements

- BCM head node with pythoncm installed
- Python 3.x with pip and virtualenv
- Build tools (python3-devel, gcc)

## Why This Role Exists

The `pythoncm` library is proprietary NVIDIA software only available on BCM head nodes. To use Ansible's dynamic inventory plugin from a remote control node, we need to package and install pythoncm locally.

## Workflow

1. Checks if pythoncm exists on BCM head node
2. Copies pythoncm source code to temporary directory
3. Creates setup.py for wheel building
4. Builds wheel package
5. Fetches wheel to local machine
6. Installs wheel in local Python environment

## Required Variables

None - all variables have defaults.

## Optional Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `bcm_python_path` | `/cm/local/apps/python3/bin/python3` | Python path on BCM |
| `pythoncm_site_packages` | `/cm/local/apps/python3/lib/python3.9/site-packages` | pythoncm location on BCM |
| `temp_wheel_dir` | `/tmp/pythoncm_wheel` | Temporary build directory |
| `local_wheel_dest` | `.` | Local wheel download destination |
| `local_python` | `python3` | Local Python executable |

## Example Usage

```yaml
# From playbooks/setup_pythoncm.yml
- name: Setup pythoncm for dynamic inventory
  hosts: bcm_headnode
  roles:
    - fabiendupont.bcm.pythoncm_setup
```

## After Setup

Enable dynamic inventory in ansible.cfg:
```ini
[inventory]
enable_plugins = brightcomputing.bcm110.bright_nodes
```

Use inventory plugin:
```yaml
# inventory/bcm_dynamic.yml
plugin: brightcomputing.bcm110.bright_nodes
```

## Dependencies

- brightcomputing.bcm110 collection

## Notes

- One-time setup per control node
- Wheel is version-specific to BCM installation
- Rebuild if BCM is upgraded
