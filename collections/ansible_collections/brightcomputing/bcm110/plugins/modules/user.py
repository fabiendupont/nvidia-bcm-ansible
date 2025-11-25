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
module: user
description: ['User']
options:
    state:
      type: str
      choices:
      - present
      - absent
      default: present
      description:
      - The state the resource should have
    cloneFrom:
      type: str
      default: ''
      description:
      - The id or name of the entity that the new entity will be cloned from.
      - ' (take effect only at entity creation)'
    name:
      description:
      - User login (e.g. donald)
      type: str
      required: true
    ID:
      description:
      - User ID number
      type: str
      required: false
    commonName:
      description:
      - Full name (e.g. Donald Duck)
      type: str
      required: false
    surname:
      description:
      - Surname (e.g. Duck)
      type: str
      required: false
    groupID:
      description:
      - Base group of this user
      type: str
      required: false
    loginShell:
      description:
      - Login shell
      type: str
      required: false
    homeDirectory:
      description:
      - Home directory
      type: str
      required: false
    password:
      description:
      - Password
      type: str
      required: false
    homeDirOperation:
      description:
      - Set to false to not create or move home directory
      type: bool
      required: false
      default: true
    shadowMin:
      description:
      - Minimum number of days required between password changes
      type: int
      required: false
      default: 0
    shadowMax:
      description:
      - Maximum number of days for which the user password remains valid.
      type: int
      required: false
      default: 999999
    shadowWarning:
      description:
      - Number of days of advance warning given to the user before the user password expires
      type: int
      required: false
      default: 7
    shadowInactive:
      description:
      - Number of days of inactivity allowed for the user
      type: int
      required: false
      default: 0
    shadowExpire:
      description:
      - Date on which the user login will be disabled
      type: int
      required: false
      default: 24837
    email:
      description:
      - Email
      type: str
      required: false
    profile:
      description:
      - Profile for Authorization
      type: str
      required: false
    projectManager:
      description:
      - Project manager
      type: dict
      required: false
      options:
        users:
          description:
          - List of users managed
          type: list
          required: false
          default: []
        accounts:
          description:
          - List of accounts managed
          type: list
          required: false
          default: []
        op:
          description:
          - Job needs to belong to one of the users and/or accounts
          type: str
          required: false
          default: OR
          choices:
          - AND
          - OR
    notes:
      description:
      - Administrator notes
      type: str
      required: false
    homePage:
      description:
      - Home page
      type: str
      required: false
    writeSshProxyConfig:
      description:
      - Write ssh proxy config
      type: bool
      required: false
      default: false
    createSshKey:
      description:
      - Create ssh key for added users
      type: bool
      required: false
      default: false
    disablePasswordSsh:
      description:
      - Disable password ssh
      type: bool
      required: false
      default: false
    authorizedSshKeys:
      description:
      - Authorized ssh keys
      type: str
      required: false
    allowGPUWorkloadPowerProfiles:
      description:
      - Allow changing GPU workload power profiles from jobs
      type: bool
      required: false
      default: false

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""
- name: create test-user
  brightcomputing.bcm110.user:
    name: test-user
    password: test-user-password
    profile: readonly
- name: remove test-user
  brightcomputing.bcm110.user:
    state: absent
    name: test-user

"""

RETURN = r"""
---
user:
  type: complex
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

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import User
except ImportError:
    HAS_PYTHONCM = False
    PYTHONCM_IMP_ERR = traceback.format_exc()
else:
    HAS_PYTHONCM = True
    PYTHONCM_IMP_ERR = None

try:
    import deepdiff
except ImportError:
    HAS_DEEPDIFF = False
    DEEPDIFF_IMP_ERR = traceback.format_exc()
else:
    HAS_DEEPDIFF = True
    DEEPDIFF_IMP_ERR = None

try:
    from box import Box
except ImportError:
    HAS_BOX = False
    BOX_IMP_ERR = traceback.format_exc()
else:
    HAS_BOX = True
    BOX_IMP_ERR = None

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.base_module import BaseModule
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.core import EntityManager
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.utils import json_encode_entity
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.user import User_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=User_ArgSpec.argument_spec,
        supports_check_mode=True,
    )

    if not HAS_PYTHONCM:
        module.fail_json(msg=missing_required_lib("cmdaemon-pythoncm"), exception=PYTHONCM_IMP_ERR)

    if not HAS_DEEPDIFF:
        module.fail_json(msg=missing_required_lib("deepdiff"), exception=DEEPDIFF_IMP_ERR)

    if not HAS_BOX:
        module.fail_json(msg=missing_required_lib("python-box"), exception=BOX_IMP_ERR)

    params =  module.bright_params

    cluster = Cluster()  # TODO make this configurable

    entity_manager = EntityManager(cluster, module.log)

    entity = entity_manager.lookup_entity(params, User)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(User, params, commit=not module.check_mode)
            changed = True
    else:

        if desired_state == "present":
            diff = entity_manager.check_diff(entity, params)
            if diff:
                entity, res = entity_manager.update_resource(entity, params, commit=not module.check_mode)
                changed = True

        if desired_state == "absent":
            entity, res = entity_manager.delete_resource(entity, params, commit=not module.check_mode)
            changed = True

    entity_as_dict = json_encode_entity(entity)

    cluster.disconnect()

    if not changed:
        module.exit_json(changed=changed, **entity_as_dict)

    if res.good:
        module.exit_json(changed=changed, diff=diff, **entity_as_dict)
    else:
        if hasattr(res, 'validation'):
            msg = "|".join(it.message for it in res.validation)
        else:
            msg = "Operation failed."
        module.fail_json(msg=msg, **entity_as_dict)


if __name__ == '__main__':
    main()