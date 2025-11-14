# Cluster Audit Role

Generate comprehensive audit reports for NVIDIA Base Command Manager clusters.

## Description

This role creates detailed audit reports covering:
- Head node configuration
- Category settings
- Software image details
- Network configuration
- Configuration overlays

Reports are saved to disk and can be used for:
- Compliance auditing
- Configuration documentation
- Change tracking
- Troubleshooting

## Requirements

- NVIDIA BCM 11.0+
- nvidia.bcm collection installed
- Write access to report directory

## Role Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `audit_report_dir` | `/tmp/bcm_audit` | Directory for audit reports |
| `audit_report_filename` | `bcm_audit_{{ ansible_date_time.date }}.txt` | Report filename |
| `audit_nodes` | `true` | Include node information |
| `audit_categories` | `true` | Include category information |
| `audit_images` | `true` | Include software image information |
| `audit_networks` | `true` | Include network information |
| `audit_overlays` | `true` | Include overlay information |

## Dependencies

None

## Example Playbook

```yaml
---
- name: Generate BCM Audit Report
  hosts: localhost
  gather_facts: true

  roles:
    - nvidia.bcm.cluster_audit
```

## Example with Custom Report Location

```yaml
---
- name: Generate BCM Audit Report
  hosts: localhost
  gather_facts: true

  roles:
    - role: nvidia.bcm.cluster_audit
      vars:
        audit_report_dir: /var/log/bcm_audits
        audit_report_filename: "cluster_audit_{{ ansible_date_time.epoch }}.txt"
```

## Example Output

```
================================================================================
NVIDIA Base Command Manager - Cluster Audit Report
Generated: 2025-01-15T10:30:00Z
================================================================================

HEAD NODE:
  Hostname: bcm11-headnode
  Type: HeadNode
  UUID: c7575ac1-2076-4833-b811-551e4f255381
  MAC: 52:54:00:65:74:3F
  IP: 10.141.255.254

DEFAULT CATEGORY:
  Name: default
  UUID: d05e44cd-eb62-4c3c-a1f0-bca9913c743d
  Software Image: f4632f43-b445-4bee-bf3b-177ec7243ce4
  Management Network: c48ff6fe-ee03-43ec-9dd5-9b5554a5d5f7

SOFTWARE IMAGE:
  Name: default-image
  UUID: f4632f43-b445-4bee-bf3b-177ec7243ce4
  Path: /cm/images/default-image
  Kernel Version: 5.14.0-503.14.1.el9_5.x86_64
  Kernel Parameters: rd.driver.blacklist=nouveau

...
```

## Scheduled Audits

To run audits on a schedule, create a cron job:

```bash
# Run audit daily at 2 AM
0 2 * * * ansible-playbook /path/to/audit_playbook.yml
```

Or use Ansible Automation Platform job scheduling.

## License

GPL-3.0-or-later

## Author

NVIDIA Corporation
