#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) NVIDIA Corporation
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: bcm_certificate
short_description: Manage certificates in NVIDIA Base Command Manager
description:
    - Query, create, revoke, and remove certificates in NVIDIA Base Command Manager
    - Manage node certificates, user certificates, and service certificates
    - Save certificates and private keys to files
version_added: "1.2.0"
options:
    serial_number:
        description:
            - Serial number of the certificate to manage
            - Used to identify existing certificates for query, revoke, unrevoke, or remove operations
        type: int
    name:
        description:
            - Common name (CN) for the certificate
            - Required when creating a new certificate
            - Can be used to query certificates by common name
        type: str
    state:
        description:
            - Desired state of the certificate
            - C(query) retrieves certificate information
            - C(present) creates a new certificate if it doesn't exist
            - C(absent) removes the certificate
            - C(revoked) revokes the certificate
            - C(unrevoked) unrevokes a previously revoked certificate
        choices: [ query, present, absent, revoked, unrevoked ]
        default: query
        type: str
    profile:
        description:
            - Certificate profile to use
            - Common profiles: node, admin, readonly, bootstrap
            - Used when creating certificates or filtering queries
        type: str
    filter_profile:
        description:
            - Filter query results by profile
            - Only used with state=query when querying all certificates
        type: str
    filter_revoked:
        description:
            - Filter query results by revocation status
            - Only used with state=query
        type: bool
    client_type:
        description:
            - Client type for the certificate
            - NODE (3), CMSH (2), PYTHON (6), CMGUI (4), etc.
        type: int
        default: 6
    valid_for_days:
        description:
            - Number of days the certificate is valid
        type: int
        default: 36500
    private_key_bits:
        description:
            - Number of bits for the private key
        type: int
        default: 2048
    country:
        description:
            - Country (C) field for certificate subject
        type: str
    state_province:
        description:
            - State or province (ST) field for certificate subject
        type: str
    locality:
        description:
            - Locality (L) field for certificate subject
        type: str
    organization:
        description:
            - Organization (O) field for certificate subject
        type: str
    organizational_unit:
        description:
            - Organizational unit (OU) field for certificate subject
        type: str
    alternative_names:
        description:
            - Subject alternative names (SANs)
            - Can be list of DNS names or IP addresses
        type: list
        elements: str
    component:
        description:
            - Component name for the certificate
        type: str
    system_login_name:
        description:
            - System login name associated with the certificate
        type: str
    cert_file:
        description:
            - Path to save the certificate PEM file
            - Only used with state=present after creation or state=query
        type: path
    key_file:
        description:
            - Path to save the private key PEM file
            - Only used with state=present after creation
        type: path
    file_owner:
        description:
            - Owner (UID) for saved certificate/key files
        type: int
    file_group:
        description:
            - Group (GID) for saved certificate/key files
        type: int
    file_mode:
        description:
            - Permissions mode for saved certificate/key files
        type: str
        default: '0600'
    pythoncm_path:
        description:
            - Path to pythoncm library
        type: str
        default: /cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages
author:
    - NVIDIA Corporation
'''

EXAMPLES = r'''
- name: Query all certificates
  nvidia.bcm.bcm_certificate:
    state: query
  register: all_certs

- name: Query node certificates only
  nvidia.bcm.bcm_certificate:
    state: query
    filter_profile: node
  register: node_certs

- name: Query a specific certificate by serial number
  nvidia.bcm.bcm_certificate:
    serial_number: 26
    state: query
  register: cert_info

- name: Query certificate by common name
  nvidia.bcm.bcm_certificate:
    name: 52-54-00-a3-91-ae
    state: query
  register: cert_by_name

- name: Create a new certificate
  nvidia.bcm.bcm_certificate:
    name: testnode01
    state: present
    profile: node
    valid_for_days: 365
    country: US
    state_province: California
    locality: Santa Clara
    organization: NVIDIA Inc
    organizational_unit: Bright Licensing
    alternative_names:
      - testnode01.example.com
      - 10.0.0.100
  register: new_cert

- name: Create certificate and save to files
  nvidia.bcm.bcm_certificate:
    name: testservice
    state: present
    profile: admin
    cert_file: /tmp/testservice.crt
    key_file: /tmp/testservice.key
    file_mode: '0600'

- name: Revoke a certificate
  nvidia.bcm.bcm_certificate:
    serial_number: 100
    state: revoked

- name: Unrevoke a certificate
  nvidia.bcm.bcm_certificate:
    serial_number: 100
    state: unrevoked

- name: Remove a certificate
  nvidia.bcm.bcm_certificate:
    serial_number: 100
    state: absent

- name: Query and save existing certificate to file
  nvidia.bcm.bcm_certificate:
    serial_number: 26
    state: query
    cert_file: /tmp/node001.crt
'''

RETURN = r'''
certificate:
    description: Certificate information
    returned: query, present
    type: dict
    sample:
        serial_number: 26
        common_name: 52-54-00-a3-91-ae
        profile: node
        revoked: false
        subject: /C=US/ST=California/L=Santa Clara/O=NVIDIA Inc/OU=Bright Licensing/CN=52-54-00-a3-91-ae
        issuer: /C=US/ST=California/L=Santa Clara/O=NVIDIA Inc/OU=Bright Licensing/CN=bcm11-headnode
        start_time: 2025-11-04T14:56:11
        expire_time: 2125-10-12T15:56:11
        remaining_days: 36491
certificates:
    description: List of certificates (when querying all)
    returned: query (without serial_number or name)
    type: list
    elements: dict
changed:
    description: Whether any change was made
    returned: always
    type: bool
msg:
    description: Human-readable message
    returned: always
    type: str
'''

import sys
import os
from ansible.module_utils.basic import AnsibleModule


def cert_to_dict(cert):
    """Convert a Certificate object to a dictionary"""
    return {
        'serial_number': cert.serialNumber,
        'common_name': cert.commonName,
        'profile': cert.profile,
        'component': cert.component,
        'system_login': cert.sysLogin,
        'revoked': cert.revoked,
        'subject': cert.subjectName,
        'issuer': cert.issuerName,
        'country': cert.country,
        'state': cert.state,
        'locality': cert.locality,
        'organization': cert.organization,
        'organizational_unit': cert.organizationalUnit,
        'alternative_names': list(cert.subjectAlternativeNames) if cert.subjectAlternativeNames else [],
        'start_time': cert.startTime,
        'expire_time': cert.expireTime,
        'remaining_seconds': cert.remaining,
        'is_ca': cert.CA,
        'has_edge_secret': cert.hasEdgeSecret,
    }


def find_certificate(bcm, serial_number=None, name=None):
    """Find a certificate by serial number or common name"""
    certs = bcm.get_all_certificates()

    if serial_number is not None:
        matching = [c for c in certs if c.serialNumber == serial_number]
        return matching[0] if matching else None

    if name:
        matching = [c for c in certs if c.commonName == name]
        return matching[0] if matching else None

    return None


def query_certificates(module, bcm):
    """Query certificate(s)"""
    serial_number = module.params['serial_number']
    name = module.params['name']
    filter_profile = module.params['filter_profile']
    filter_revoked = module.params['filter_revoked']
    cert_file = module.params['cert_file']

    # Query specific certificate
    if serial_number is not None or name:
        cert = find_certificate(bcm, serial_number=serial_number, name=name)

        if not cert:
            identifier = f"serial {serial_number}" if serial_number else f"name '{name}'"
            module.fail_json(msg=f"Certificate not found: {identifier}")

        result = {
            'changed': False,
            'certificate': cert_to_dict(cert),
            'msg': f'Certificate {cert.serialNumber} found'
        }

        # Save certificate to file if requested
        if cert_file and not module.check_mode:
            try:
                uid = module.params.get('file_owner')
                gid = module.params.get('file_group')
                mode = int(module.params.get('file_mode', '0600'), 8)
                cert.save(cert_file, uid=uid, gid=gid, mode=mode)
                result['msg'] += f', saved to {cert_file}'
            except Exception as e:
                module.fail_json(msg=f"Failed to save certificate: {str(e)}")

        module.exit_json(**result)

    # Query all certificates with optional filters
    certs = bcm.get_all_certificates()

    if filter_profile:
        certs = [c for c in certs if c.profile == filter_profile]

    if filter_revoked is not None:
        certs = [c for c in certs if c.revoked == filter_revoked]

    module.exit_json(
        changed=False,
        certificates=[cert_to_dict(c) for c in certs],
        count=len(certs),
        msg=f'Found {len(certs)} certificate(s)'
    )


def create_certificate(module, bcm):
    """Create a new certificate"""
    name = module.params['name']
    profile = module.params['profile']

    if not name:
        module.fail_json(msg="'name' is required when creating a certificate")

    if not profile:
        module.fail_json(msg="'profile' is required when creating a certificate")

    # Check if certificate already exists
    existing = find_certificate(bcm, name=name)
    if existing:
        module.exit_json(
            changed=False,
            certificate=cert_to_dict(existing),
            msg=f'Certificate already exists with serial {existing.serialNumber}'
        )

    if module.check_mode:
        module.exit_json(
            changed=True,
            msg=f"Would create certificate '{name}' with profile '{profile}'"
        )

    # Create the certificate
    from pythoncm.entity.certificate import Certificate
    cert = Certificate(bcm)

    try:
        success = cert.create(
            name=name,
            profile=profile,
            system_login_name=module.params.get('system_login_name'),
            country=module.params.get('country'),
            state=module.params.get('state_province'),
            locality=module.params.get('locality'),
            organization=module.params.get('organization'),
            organizational_unit=module.params.get('organizational_unit'),
            client_type=module.params.get('client_type', 6),
            valid_for_days=module.params.get('valid_for_days', 36500),
            private_key_bits=module.params.get('private_key_bits', 2048),
            component=module.params.get('component'),
            alternative_names=module.params.get('alternative_names'),
            timeout=30.0,
        )

        if not success:
            module.fail_json(msg=f"Failed to create certificate '{name}'")

        result = {
            'changed': True,
            'certificate': cert_to_dict(cert),
            'msg': f"Certificate created with serial {cert.serialNumber}"
        }

        # Save to files if requested
        cert_file = module.params.get('cert_file')
        key_file = module.params.get('key_file')

        if cert_file or key_file:
            uid = module.params.get('file_owner')
            gid = module.params.get('file_group')
            mode = int(module.params.get('file_mode', '0600'), 8)

            cert.save(
                cert_file or '/dev/null',
                uid=uid,
                gid=gid,
                mode=mode,
                private_key_file=key_file
            )

            if cert_file:
                result['msg'] += f', certificate saved to {cert_file}'
            if key_file:
                result['msg'] += f', private key saved to {key_file}'

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=f"Failed to create certificate '{name}': {str(e)}")


def revoke_certificate(module, bcm):
    """Revoke a certificate"""
    serial_number = module.params['serial_number']

    if serial_number is None:
        module.fail_json(msg="'serial_number' is required for revoke operation")

    cert = find_certificate(bcm, serial_number=serial_number)
    if not cert:
        module.fail_json(msg=f"Certificate with serial {serial_number} not found")

    if cert.revoked:
        module.exit_json(
            changed=False,
            certificate=cert_to_dict(cert),
            msg=f'Certificate {serial_number} is already revoked'
        )

    if module.check_mode:
        module.exit_json(
            changed=True,
            msg=f'Would revoke certificate {serial_number}'
        )

    try:
        # Call RPC directly (cert.revoke() has a bug - calls non-existent get_serial_number())
        rpc = bcm.get_rpc()
        (code, out) = rpc.call(
            service='cmcert',
            call='revokeCertificate',
            args=[[serial_number]],
        )
        if code:
            raise OSError(out)

        # Refresh certificate to get updated status
        cert = find_certificate(bcm, serial_number=serial_number)

        module.exit_json(
            changed=True,
            certificate=cert_to_dict(cert),
            msg=f'Certificate {serial_number} revoked successfully'
        )
    except Exception as e:
        module.fail_json(msg=f"Failed to revoke certificate {serial_number}: {str(e)}")


def unrevoke_certificate(module, bcm):
    """Unrevoke a certificate"""
    serial_number = module.params['serial_number']

    if serial_number is None:
        module.fail_json(msg="'serial_number' is required for unrevoke operation")

    cert = find_certificate(bcm, serial_number=serial_number)
    if not cert:
        module.fail_json(msg=f"Certificate with serial {serial_number} not found")

    if not cert.revoked:
        module.exit_json(
            changed=False,
            certificate=cert_to_dict(cert),
            msg=f'Certificate {serial_number} is not revoked'
        )

    if module.check_mode:
        module.exit_json(
            changed=True,
            msg=f'Would unrevoke certificate {serial_number}'
        )

    try:
        # Call RPC directly (cert.unrevoke() has a bug - calls non-existent get_serial_number())
        rpc = bcm.get_rpc()
        (code, out) = rpc.call(
            service='cmcert',
            call='unrevokeCertificate',
            args=[[serial_number]],
        )
        if code:
            raise OSError(out)

        # Refresh certificate to get updated status
        cert = find_certificate(bcm, serial_number=serial_number)

        module.exit_json(
            changed=True,
            certificate=cert_to_dict(cert),
            msg=f'Certificate {serial_number} unrevoked successfully'
        )
    except Exception as e:
        module.fail_json(msg=f"Failed to unrevoke certificate {serial_number}: {str(e)}")


def remove_certificate(module, bcm):
    """Remove a certificate"""
    serial_number = module.params['serial_number']

    if serial_number is None:
        module.fail_json(msg="'serial_number' is required for remove operation")

    cert = find_certificate(bcm, serial_number=serial_number)
    if not cert:
        module.exit_json(
            changed=False,
            msg=f'Certificate {serial_number} does not exist'
        )

    if module.check_mode:
        module.exit_json(
            changed=True,
            msg=f'Would remove certificate {serial_number}'
        )

    try:
        # Call RPC directly (cert.remove() has a bug - calls non-existent get_serial_number())
        rpc = bcm.get_rpc()
        (code, out) = rpc.call(
            service='cmcert',
            call='removeCertificate',
            args=[[serial_number]],
        )
        if code:
            raise OSError(out)

        module.exit_json(
            changed=True,
            msg=f'Certificate {serial_number} removed successfully'
        )
    except Exception as e:
        module.fail_json(msg=f"Failed to remove certificate {serial_number}: {str(e)}")


def main():
    module = AnsibleModule(
        argument_spec=dict(
            serial_number=dict(type='int'),
            name=dict(type='str'),
            state=dict(type='str', default='query', choices=['query', 'present', 'absent', 'revoked', 'unrevoked']),
            profile=dict(type='str'),
            filter_profile=dict(type='str'),
            filter_revoked=dict(type='bool'),
            client_type=dict(type='int', default=6),
            valid_for_days=dict(type='int', default=36500),
            private_key_bits=dict(type='int', default=2048),
            country=dict(type='str'),
            state_province=dict(type='str'),
            locality=dict(type='str'),
            organization=dict(type='str'),
            organizational_unit=dict(type='str'),
            alternative_names=dict(type='list', elements='str'),
            component=dict(type='str'),
            system_login_name=dict(type='str'),
            cert_file=dict(type='path'),
            key_file=dict(type='path'),
            file_owner=dict(type='int'),
            file_group=dict(type='int'),
            file_mode=dict(type='str', default='0600'),
            pythoncm_path=dict(
                type='str',
                default='/cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages'
            ),
        ),
        supports_check_mode=True,
    )

    pythoncm_path = module.params['pythoncm_path']
    if pythoncm_path not in sys.path:
        sys.path.insert(0, pythoncm_path)

    try:
        from pythoncm.cluster import Cluster
    except ImportError as e:
        module.fail_json(msg=f"Failed to import pythoncm: {str(e)}")

    try:
        bcm = Cluster()
    except Exception as e:
        module.fail_json(msg=f"Failed to connect to BCM: {str(e)}")

    state = module.params['state']

    if state == 'query':
        query_certificates(module, bcm)
    elif state == 'present':
        create_certificate(module, bcm)
    elif state == 'revoked':
        revoke_certificate(module, bcm)
    elif state == 'unrevoked':
        unrevoke_certificate(module, bcm)
    elif state == 'absent':
        remove_certificate(module, bcm)


if __name__ == '__main__':
    main()
