#
# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: LicenseRef-NvidiaProprietary
#
# NVIDIA CORPORATION, its affiliates and licensors retain all intellectual
# property and proprietary rights in and to this material, related
# documentation and any modifications thereto. Any use, reproduction,
# disclosure or distribution of this material and related documentation
# without an express license agreement from NVIDIA CORPORATION or
# its affiliates is strictly prohibited.
#

class EtcdCluster_ArgSpec:
    argument_spec = {'ca': {'default': '/etc/kubernetes/pki/default/etcd/ca.crt', 'type': 'str'},
                     'cakey': {'default': '/etc/kubernetes/pki/default/etcd/ca.key', 'type': 'str'},
                     'clientCA': {'default': '/etc/kubernetes/pki/default/etcd/ca.crt',
                                  'type': 'str'},
                     'clientCertificate': {'default': '/etc/kubernetes/pki/default/apiserver-etcd-client.crt',
                                           'type': 'str'},
                     'clientCertificateKey': {'default': '/etc/kubernetes/pki/default/apiserver-etcd-client.key',
                                              'type': 'str'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'electionTimeout': {'default': 1000, 'type': 'int'},
                     'heartBeatInterval': {'default': 100, 'type': 'int'},
                     'memberCertificate': {'default': '/etc/kubernetes/pki/default/etcd-member.crt',
                                           'type': 'str'},
                     'memberCertificateKey': {'default': '/etc/kubernetes/pki/default/etcd-member.key',
                                              'type': 'str'},
                     'moduleFileTemplate': {'type': 'str'},
                     'name': {'required': True, 'type': 'str'},
                     'notes': {'type': 'str'},
                     'state': {'choices': ['present', 'absent'],
                               'default': 'present',
                               'type': 'str'}}