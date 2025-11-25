#!/cm/local/apps/python3/bin/python
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

from __future__ import annotations

############################
# Docs
############################

DOCUMENTATION = r"""
---
module: cluster_info
description: returns general information about the cluster
options:
    {}
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""
- name: register cluster info
  register: result
  brightcomputing.bcm110.cluster_info: {}

"""

RETURN = r"""
---
cluster:
  type: complex
  description: ''
  returned: success
  contains:
    name:
      type: str
      description: ''
      returned: success
    overview:
      type: complex
      description: ''
      returned: success
    license_info:
      type: complex
      description: ''
      returned: success
    version_info:
      type: complex
      description: ''
      returned: success
    server_status:
      type: complex
      description: ''
      returned: success

"""
############################
# Imports
############################

import traceback

try:
    from pythoncm.cluster import Cluster
except ImportError:
    HAS_PYTHONCM = False
    PYTHONCM_IMP_ERR = traceback.format_exc()
else:
    HAS_PYTHONCM = True
    PYTHONCM_IMP_ERR = None


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import missing_required_lib
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.utils import json_encode_entity

############################
# main
############################


def main():

    module = AnsibleModule(
        argument_spec={}
    )

    if not HAS_PYTHONCM:
        module.fail_json(msg=missing_required_lib("cmdaemon-pythoncm"), exception=PYTHONCM_IMP_ERR)

    cluster = Cluster()  # TODO make this configurable

    json_ready_result = {
        "name": cluster.name,
        "version_info": json_encode_entity(cluster.version_info()),
        "license_info": json_encode_entity(cluster.license_info()),
        "server_status": json_encode_entity(cluster.server_status()),
        "overview": json_encode_entity(cluster.overview()),
    }

    cluster.disconnect()

    module.exit_json(cluster=json_ready_result, changed=False)


if __name__ == '__main__':
    main()