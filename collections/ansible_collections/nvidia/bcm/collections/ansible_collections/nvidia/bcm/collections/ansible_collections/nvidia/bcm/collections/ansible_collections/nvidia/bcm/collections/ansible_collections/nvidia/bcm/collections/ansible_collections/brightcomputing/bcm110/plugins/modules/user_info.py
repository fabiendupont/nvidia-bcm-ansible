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
module: user_info
description: Query cmdaemon for entity of type User
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
user:
  type: list
  description: User
  returned: success
  contains:
    uuid:
      type: str
      description: ''
      returned: success
    baseType:
      type: str
      description: ''
      returned: success
    childType:
      type: str
      description: ''
      returned: success
    revision:
      type: str
      description: ''
      returned: success
    modified:
      type: bool
      description: ''
      returned: success
    is_committed:
      type: bool
      description: ''
      returned: success
    to_be_removed:
      type: bool
      description: ''
      returned: success
    extra_values:
      type: json
      description: ''
      returned: success
    name:
      type: str
      description: User login (e.g. donald)
      returned: success
    ID:
      type: str
      description: User ID number
      returned: success
    commonName:
      type: str
      description: Full name (e.g. Donald Duck)
      returned: success
    surname:
      type: str
      description: Surname (e.g. Duck)
      returned: success
    groupID:
      type: str
      description: Base group of this user
      returned: success
    loginShell:
      type: str
      description: Login shell
      returned: success
    homeDirectory:
      type: str
      description: Home directory
      returned: success
    password:
      type: str
      description: Password
      returned: success
    homeDirOperation:
      type: bool
      description: Set to false to not create or move home directory
      returned: success
    shadowMin:
      type: int
      description: Minimum number of days required between password changes
      returned: success
    shadowMax:
      type: int
      description: Maximum number of days for which the user password remains valid.
      returned: success
    shadowWarning:
      type: int
      description: Number of days of advance warning given to the user before the
        user password expires
      returned: success
    shadowInactive:
      type: int
      description: Number of days of inactivity allowed for the user
      returned: success
    shadowLastChange:
      type: int
      description: Number of days between January 1, 1970 and the day when the user
        password was last changed
      returned: success
    shadowExpire:
      type: int
      description: Date on which the user login will be disabled
      returned: success
    email:
      type: str
      description: Email
      returned: success
    profile:
      type: str
      description: Profile for Authorization
      returned: success
    certSerialNumber:
      type: int
      description: Serial number of the certificate assigned to user
      returned: success
    projectManager:
      type: complex
      description: Project manager
      returned: success
    notes:
      type: str
      description: Administrator notes
      returned: success
    homePage:
      type: str
      description: Home page
      returned: success
    information:
      type: str
      description: Information added by CMDaemon
      returned: success
    writeSshProxyConfig:
      type: bool
      description: Write ssh proxy config
      returned: success
    createSshKey:
      type: bool
      description: Create ssh key for added users
      returned: success
    disablePasswordSsh:
      type: bool
      description: Disable password ssh
      returned: success
    authorizedSshKeys:
      type: str
      description: Authorized ssh keys
      returned: success
    allowGPUWorkloadPowerProfiles:
      type: bool
      description: Allow changing GPU workload power profiles from jobs
      returned: success

"""
############################
# Imports
############################

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import User
    from pythoncm.entity_to_json_encoder import EntityToJSONEncoder
except ImportError:
    HAS_PYTHONCM = False
    PYTHONCM_IMP_ERR = traceback.format_exc()
else:
    HAS_PYTHONCM = True
    PYTHONCM_IMP_ERR = None


from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.core import EntityQuery
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.utils import entity_to_dict

############################
# main
############################


def main():

    module = AnsibleModule(
        argument_spec={'format': {'choices': ['list', 'dict'], 'default': 'list', 'type': 'str'}, 'depth': {'default': 3, 'type': 'int'}, 'include_id': {'default': False, 'type': 'bool'}, 'for_update': {'default': False, 'type': 'bool'}},
        supports_check_mode=True,
    )

    if not HAS_PYTHONCM:
        module.fail_json(msg=missing_required_lib("cmdaemon-pythoncm"), exception=PYTHONCM_IMP_ERR)

    cluster = Cluster()  # TODO make this configurable

    entity_query = EntityQuery(cluster)

    results = entity_query.find(User)

    format = module.params["format"]

    depth = module.params["depth"]

    include_id = module.params["include_id"]

    for_update = module.params["for_update"]

    if format == "list":
        json_ready_result = [
            entity_to_dict(
                entity,
                depth=depth,
                for_update=for_update,
                include_id=include_id,
            )
            for entity in results
        ] if results else []

    if format == "dict":
        json_ready_result = {
            entity.resolve_name: entity_to_dict(
                entity,
                depth=depth,
                for_update=for_update,
                include_id=include_id,
            )
            for entity in results
        } if results else {}

    cluster.disconnect()

    json_ready_result = json.loads(json.dumps(json_ready_result, cls=EntityToJSONEncoder))

    module.exit_json(users=json_ready_result, changed=False)


if __name__ == '__main__':
    main()