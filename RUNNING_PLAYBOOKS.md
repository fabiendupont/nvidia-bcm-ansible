# Running Playbooks with BCM Dynamic Inventory

## The pythoncm Requirement

The brightcomputing.bcm110 dynamic inventory plugin requires the `pythoncm` module, which is only available from the BCM head node. This module is installed in a local virtual environment.

## How to Run Playbooks

Use the `PYTHONPATH` environment variable to make pythoncm available to Ansible:

```bash
PYTHONPATH=/home/fdupont/Work/NVIDIA/BCM/nvidia-bcm-ansible/.venv/lib/python3.14/site-packages \
  ansible-playbook -i inventory/your_inventory.yml playbooks/your_playbook.yml
```

### Why This Works

1. **System-wide Ansible**: Uses the regular `ansible-playbook` command from your system
2. **pythoncm in venv**: The pythoncm module is installed in `.venv/lib/python3.14/site-packages`
3. **PYTHONPATH**: Tells Python to look in the venv's site-packages for modules
4. **Dynamic inventory**: The bright_nodes plugin can now import pythoncm successfully

## Setup Steps (One-Time)

1. Install pythoncm dependencies locally and on BCM head node:
   ```bash
   ANSIBLE_INVENTORY_ENABLED=host_list,script,auto,yaml,ini,toml \
     ansible-playbook -i inventory/test_rhel_vm.yml playbooks/setup_pythoncm.yml
   ```

2. Build and install the nvidia.bcm collection:
   ```bash
   # Build from source (root directory contains galaxy.yml)
   ansible-galaxy collection build . --output-path /tmp/ --force

   # Install to local collections directory
   ansible-galaxy collection install /tmp/nvidia-bcm-*.tar.gz -p ./collections --force
   ```

   This automatically installs dependencies: ansible.posix, kubernetes.core, containers.podman, brightcomputing.bcm110

3. Verify pythoncm is installed:
   ```bash
   .venv/bin/python3 -c "import pythoncm; print('pythoncm loaded successfully')"
   ```

## Alternative: Disable Dynamic Inventory

If you don't need the bright_nodes dynamic inventory plugin, you can disable it:

```bash
ANSIBLE_INVENTORY_ENABLED=host_list,script,auto,yaml,ini,toml \
  ansible-playbook -i inventory/your_inventory.yml playbooks/your_playbook.yml
```

This approach:
- ✅ Works without pythoncm
- ✅ Faster startup (no inventory plugin loading)
- ❌ Can't use BCM dynamic inventory features

## Common Issues

### "No module named 'pythoncm'"
**Solution**: Make sure PYTHONPATH points to the venv's site-packages

### "Failed to load inventory plugin bright_nodes"
**Solution**: Either set PYTHONPATH or disable the plugin with ANSIBLE_INVENTORY_ENABLED

### Wrong Python interpreter on remote hosts
**Solution**: Don't set `interpreter_python` in ansible.cfg - let Ansible auto-discover on each host
