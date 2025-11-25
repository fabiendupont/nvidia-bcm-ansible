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

class CertificateRequest_ArgSpec:
    argument_spec = {'CSR': {'type': 'str'},
                     'allowAutosign': {'default': False, 'type': 'bool'},
                     'clientType': {'default': 0, 'type': 'int'},
                     'cloneFrom': {'default': '', 'type': 'str'},
                     'commonName': {'type': 'str'},
                     'country': {'type': 'str'},
                     'hasEdgeSecret': {'default': False, 'type': 'bool'},
                     'locality': {'type': 'str'},
                     'organization': {'type': 'str'},
                     'organizationalUnit': {'type': 'str'},
                     'session_uuid': {'default': '00000000-0000-0000-0000-000000000000',
                                      'type': 'str'},
                     'state': {'type': 'str'},
                     'subjectAlternativeNames': {'type': 'list'}}