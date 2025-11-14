# BCM Certificate Management Module

## Overview

The `bcm_certificate` module provides management of X.509 certificates in NVIDIA Base Command Manager (BCM). BCM uses certificates for authentication and authorization of nodes, users, and services.

## Module: nvidia.bcm.bcm_certificate

### Features

- Query certificates by serial number, common name, or filters
- Save certificates to files with proper permissions
- Revoke and unrevoke certificates
- Remove certificates
- Support for all certificate profiles (node, admin, readonly, etc.)

### Operations Supported

✅ **Query** - Retrieve certificate information
✅ **Save** - Export certificates to PEM files
✅ **Revoke/Unrevoke** - Manage certificate revocation status
✅ **Remove** - Delete certificates
⚠️ **Create** - Limited by BCM pythoncm library (see Known Limitations)

### Quick Start

```yaml
# Query all certificates
- name: List all certificates
  nvidia.bcm.bcm_certificate:
    state: query
  register: all_certs

# Query node certificates only
- name: List node certificates
  nvidia.bcm.bcm_certificate:
    state: query
    filter_profile: node
  register: node_certs

# Get specific certificate by serial number
- name: Query certificate
  nvidia.bcm.bcm_certificate:
    serial_number: 26
    state: query
  register: cert_info

# Query by common name (e.g., MAC address for nodes)
- name: Find certificate by name
  nvidia.bcm.bcm_certificate:
    name: "52-54-00-a3-91-ae"
    state: query
  register: cert

# Save certificate to file
- name: Export certificate
  nvidia.bcm.bcm_certificate:
    serial_number: 26
    state: query
    cert_file: /tmp/node001.pem
    file_mode: '0600'

# Revoke a certificate
- name: Revoke certificate
  nvidia.bcm.bcm_certificate:
    serial_number: 100
    state: revoked

# Unrevoke a certificate
- name: Unrevoke certificate
  nvidia.bcm.bcm_certificate:
    serial_number: 100
    state: unrevoked

# Remove a certificate
- name: Delete certificate
  nvidia.bcm.bcm_certificate:
    serial_number: 100
    state: absent
```

## Certificate Types in BCM

### Certificate Profiles

- **node** - Certificates for compute nodes (CommonName = MAC address)
- **litenode** - Certificates for lite nodes
- **admin** - Administrator certificates
- **readonly** - Read-only access certificates
- **bootstrap** - Bootstrap certificates
- **prs** - Power Reservation Steering certificates
- **mqtt** - MQTT service certificates

### Certificate Attributes

Each certificate contains:
- **serial_number** - Unique identifier
- **common_name** - Certificate CN field
- **profile** - Certificate profile type
- **component** - Associated component
- **system_login** - System login name
- **revoked** - Revocation status
- **subject** - Full subject DN
- **issuer** - Issuer DN
- **start_time** - Valid from (Unix timestamp)
- **expire_time** - Expires at (Unix timestamp)
- **alternative_names** - Subject alternative names (SANs)

## Examples

### Query and Filter Certificates

```yaml
---
- name: Certificate Management Examples
  hosts: localhost
  tasks:
    # Get all certificates
    - name: Query all certificates
      nvidia.bcm.bcm_certificate:
        state: query
      register: result

    - debug:
        msg: "Found {{ result.count }} certificates"

    # Filter by profile
    - name: Get only admin certificates
      nvidia.bcm.bcm_certificate:
        state: query
        filter_profile: admin
      register: admin_certs

    # Filter by revocation status
    - name: Get active (non-revoked) certificates
      nvidia.bcm.bcm_certificate:
        state: query
        filter_revoked: false
      register: active_certs

    # Query specific certificate
    - name: Get certificate details
      nvidia.bcm.bcm_certificate:
        serial_number: 26
        state: query
      register: cert

    - debug:
        var: cert.certificate
```

### Export Certificates

```yaml
---
- name: Export Node Certificates
  hosts: localhost
  tasks:
    # Get all node certificates
    - name: Query node certificates
      nvidia.bcm.bcm_certificate:
        state: query
        filter_profile: node
      register: node_certs

    # Export each to a file
    - name: Save certificates to files
      nvidia.bcm.bcm_certificate:
        serial_number: "{{ item.serial_number }}"
        state: query
        cert_file: "/tmp/certs/{{ item.common_name }}.pem"
        file_mode: '0644'
        file_owner: 1000
        file_group: 1000
      loop: "{{ node_certs.certificates }}"
      loop_control:
        label: "{{ item.common_name }}"
```

### Manage Certificate Lifecycle

```yaml
---
- name: Certificate Lifecycle Management
  hosts: localhost
  tasks:
    # Revoke a compromised certificate
    - name: Revoke certificate
      nvidia.bcm.bcm_certificate:
        serial_number: 100
        state: revoked

    # Later, unrevoke if needed
    - name: Restore certificate
      nvidia.bcm.bcm_certificate:
        serial_number: 100
        state: unrevoked

    # Permanently remove old certificate
    - name: Delete certificate
      nvidia.bcm.bcm_certificate:
        serial_number: 99
        state: absent
```

## Return Values

### Query (single certificate)

```yaml
certificate:
  serial_number: 26
  common_name: "52-54-00-a3-91-ae"
  profile: "node"
  component: ""
  system_login: ""
  revoked: false
  subject: "/C=US/ST=California/L=Santa Clara/O=NVIDIA Inc/OU=Bright Licensing/CN=52-54-00-a3-91-ae"
  issuer: "/C=US/ST=California/L=Santa Clara/O=NVIDIA Inc/OU=Bright Licensing/CN=bcm11-headnode"
  country: "US"
  state: "California"
  locality: "Santa Clara"
  organization: "NVIDIA Inc"
  organizational_unit: "Bright Licensing"
  alternative_names: []
  start_time: 1762264571
  expire_time: 4915950971
  remaining_seconds: 3153686400
  is_ca: false
  has_edge_secret: false
changed: false
msg: "Certificate 26 found"
```

### Query (multiple certificates)

```yaml
certificates:
  - serial_number: 1
    common_name: "bcm11-headnode.cm.cluster"
    profile: "admin"
    ...
  - serial_number: 2
    common_name: "bcm11-headnode"
    profile: "admin"
    ...
count: 51
changed: false
msg: "Found 51 certificate(s)"
```

## Known Limitations

### Certificate Creation

⚠️ **Certificate creation is limited on systems with OpenSSL 3.x**

The BCM pythoncm library (as of BCM 11.0) hardcodes the deprecated SHA-1 algorithm for certificate signing requests. OpenSSL 3.x rejects SHA-1 for security reasons, causing certificate creation to fail with:

```
Failed to create certificate: [('digital envelope routines', '', 'invalid digest')]
```

**Workaround:** Create certificates via `cmsh`:

```bash
cmsh -c "cert; createcertificate -n mycert -p admin"
```

Then manage them with the Ansible module.

**Status:** This is a BCM library bug. The Ansible module correctly calls the pythoncm API; the underlying library needs updating to use SHA-256 instead of SHA-1.

### Protected Certificates

Some certificates (e.g., active admin certificates) are protected from revocation or removal for security reasons. Attempting to revoke protected certificates will fail with "Authorization Required" errors.

### Certificate Method Bugs in pythoncm

The BCM pythoncm library has bugs in `Certificate.revoke()`, `Certificate.unrevoke()`, and `Certificate.remove()` methods - they call a non-existent `get_serial_number()` method. The Ansible module works around this by calling the RPC layer directly.

## Architecture

### How BCM Uses Certificates

1. **Node Certificates** - Automatically created when nodes register
   - CommonName = Node MAC address
   - Used for node-to-head authentication
   - Profile = "node" or "litenode"

2. **User Certificates** - Created for cmsh/API users
   - CommonName = Username or service name
   - Stored in `~/.cm/<username>.pem`
   - Profile = "admin", "readonly", etc.

3. **Service Certificates** - Used by BCM internal services
   - Profile-specific (prs, mqtt, jupyterhub, etc.)
   - Component field identifies service

### Certificate Storage

- **BCM Database** - Certificate metadata and PEM data
- **File System** - User certificates in `~/.cm/`
- **RPC Service** - `cmcert` daemon manages certificates

### Module Implementation

The module uses:
- `pythoncm.Cluster.get_all_certificates()` - Query certificates
- `pythoncm.Certificate.save()` - Export to files
- Direct RPC calls to `cmcert` service for revoke/unrevoke/remove
- `bcm.get_rpc().call(service='cmcert', call='...')` pattern

## Testing

A comprehensive test playbook is provided:

```bash
ansible-playbook /root/bcm/ansible_collections/nvidia/bcm/playbooks/test-certificate.yml
```

Tests include:
- ✅ Query all certificates
- ✅ Query with filters (profile, revoked status)
- ✅ Query by serial number
- ✅ Query by common name
- ✅ Save certificate to file with permissions
- ✅ Revoke certificate
- ✅ Idempotency of revoke
- ✅ Unrevoke certificate
- ✅ Idempotency of unrevoke
- ✅ Check mode functionality

## Troubleshooting

### "Authorization Required" errors

Ensure the pythoncm client certificate is valid:
```bash
ls -la ~/.cm/*.pem
```

### "Certificate not found"

Verify the certificate exists:
```bash
cmsh -c "cert; listcertificates"
```

### "Failed to save certificate"

Check file permissions and directory existence:
```bash
mkdir -p /path/to/certs
chmod 755 /path/to/certs
```

## See Also

- [CLAUDE.md](/root/bcm/CLAUDE.md) - BCM operations reference
- [bcm_node](bcm_node.py) - Node management module
- [bcm_user](bcm_user.py) - User management module

## References

- BCM Documentation: https://docs.nvidia.com/base-command-manager/
- pythoncm API: `/cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages/pythoncm/`
- Certificate entity: `pythoncm/entity/certificate.py`
- Certificate metadata: `pythoncm/entity/metadata/certificate.py`
