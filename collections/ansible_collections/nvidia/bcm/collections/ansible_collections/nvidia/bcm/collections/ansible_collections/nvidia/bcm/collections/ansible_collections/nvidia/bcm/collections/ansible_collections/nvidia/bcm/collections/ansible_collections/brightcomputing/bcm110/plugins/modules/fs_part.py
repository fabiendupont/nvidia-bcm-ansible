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
module: fs_part
description: ['Manages fs_parts']
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
    path:
      description:
      - Full source path of the filesystem part
      type: str
      required: true
    type:
      description:
      - The type of filesystem part
      type: str
      required: false
      default: CUSTOM
      choices:
      - IMAGE
      - BOOT
      - CM_SHARED
      - CM_NODE_INSTALLER
      - TFTPBOOT
      - CUSTOM
    watchDirectories:
      description:
      - Watch directories for changes on the active head node, filesystem part will be
        marked dirty when changed
      type: list
      required: false
      default: []
    dirtyAutoSyncDelay:
      description:
      - Time to wait before automatically syncing after the filesystem part became dirty,
        set 0 to disable
      type: int
      required: false
      default: 0
    autoDirtyDelay:
      description:
      - Time to wait before automatically marking an filesystem part as dirty, set 0 to
        disable
      type: int
      required: false
      default: 0
    preSyncScript:
      description:
      - Script to be executed before rsync runs
      type: str
      required: false
    postSyncScript:
      description:
      - Script to be executed after rsync runs
      type: str
      required: false
    abortOnPreSyncScriptFailure:
      description:
      - Do not rsync if the pre sync script exited with a non zero exit code
      type: bool
      required: false
      default: true
    runPostOnFailure:
      description:
      - Run the post rsync script even if the pre sync or sync ended with a non zero exit
        code
      type: bool
      required: false
      default: false
    syncScriptTimeout:
      description:
      - Script timeout
      type: int
      required: false
      default: 15
    rsyncAcls:
      description:
      - Rsync with --acls
      type: bool
      required: false
      default: true
    rsyncXattrs:
      description:
      - Rsync with --xattrs
      type: bool
      required: false
      default: true
    rsyncHardlinks:
      description:
      - Rsync with --hard-links
      type: bool
      required: false
      default: true
    rsyncSparse:
      description:
      - Rsync with --sparse
      type: bool
      required: false
      default: true
    rsyncNumericIds:
      description:
      - Rsync with --numeric-ids
      type: bool
      required: false
      default: true
    rsyncForce:
      description:
      - Rsync with --force
      type: bool
      required: false
      default: true
    rsyncPrune:
      description:
      - Rsync with --prune-empty-dirs
      type: bool
      required: false
      default: false
    rsyncDelta:
      description:
      - Rsync with --inplace --no-whole-file
      type: bool
      required: false
      default: false
    rsyncBlockSize:
      description:
      - Rsync with --block-size=<value> Max 128KB, 0 implies rsync default
      type: int
      required: false
      default: 0
    rsyncBandWidthLimit:
      description:
      - Rsync with --bwlimit=<value>
      type: int
      required: false
      default: 0
    rsyncCompress:
      description:
      - Rsync with --compress
      type: str
      required: false
      default: NEVER
      choices:
      - NEVER
      - ALWAYS
      - WHEN_SSH
      - WHEN_TUNNEL
      - WHEN_SSH_OR_TUNNEL
    rsyncCompressLevel:
      description:
      - Rsync compression at a specific level
      type: str
      required: false
      default: DEFAULT
      choices:
      - NONE
      - FAST
      - DEFAULT
      - BEST
      - SSH
    rsyncCheckNetworkMount:
      description:
      - 'Rsync check if file is on remote mount before delete and if so: skip it'
      type: bool
      required: false
      default: true
    extraRsyncArguments:
      description:
      - 'Extra rsync arguments. These can be made condition based on type=no-new-files|normal
        and mode=sync|update|full|sync. For example: --max-delete=0?type=normal&mode=update|sync'
      type: list
      required: false
      default: []
    excludeListSnippets:
      description: []
      type: list
      required: false
      default: []
      elements: dict
      options:
        name:
          description:
          - Name
          type: str
          required: true
        excludeList:
          description:
          - Excluded paths in the node image update
          type: list
          required: false
          default: []
        disabled:
          description:
          - Disabled
          type: bool
          required: false
          default: false
        noNewFiles:
          description:
          - No new files
          type: bool
          required: false
          default: false
        modeSync:
          description:
          - Include this snippet when mode is sync
          type: bool
          required: false
          default: true
        modeFull:
          description:
          - Include this snippet when mode is full
          type: bool
          required: false
          default: false
        modeUpdate:
          description:
          - Include this snippet when mode is update
          type: bool
          required: false
          default: true
        modeGrab:
          description:
          - Include this snippet when mode is grab
          type: bool
          required: false
          default: false
        modeGrabNew:
          description:
          - Include this snippet when mode is grab new
          type: bool
          required: false
          default: false

requirements: [cmdaemon-pythoncm, deepdiff, python-box]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
fs_part:
  type: complex
  description: ''
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
    path:
      type: str
      description: Full source path of the filesystem part
      returned: success
    type:
      type: str
      description: The type of filesystem part
      returned: success
    watchDirectories:
      type: str
      description: Watch directories for changes on the active head node, filesystem
        part will be marked dirty when changed
      returned: success
    dirtyAutoSyncDelay:
      type: int
      description: Time to wait before automatically syncing after the filesystem
        part became dirty, set 0 to disable
      returned: success
    autoDirtyDelay:
      type: int
      description: Time to wait before automatically marking an filesystem part as
        dirty, set 0 to disable
      returned: success
    preSyncScript:
      type: str
      description: Script to be executed before rsync runs
      returned: success
    postSyncScript:
      type: str
      description: Script to be executed after rsync runs
      returned: success
    abortOnPreSyncScriptFailure:
      type: bool
      description: Do not rsync if the pre sync script exited with a non zero exit
        code
      returned: success
    runPostOnFailure:
      type: bool
      description: Run the post rsync script even if the pre sync or sync ended with
        a non zero exit code
      returned: success
    syncScriptTimeout:
      type: int
      description: Script timeout
      returned: success
    rsyncAcls:
      type: bool
      description: Rsync with --acls
      returned: success
    rsyncXattrs:
      type: bool
      description: Rsync with --xattrs
      returned: success
    rsyncHardlinks:
      type: bool
      description: Rsync with --hard-links
      returned: success
    rsyncSparse:
      type: bool
      description: Rsync with --sparse
      returned: success
    rsyncNumericIds:
      type: bool
      description: Rsync with --numeric-ids
      returned: success
    rsyncForce:
      type: bool
      description: Rsync with --force
      returned: success
    rsyncPrune:
      type: bool
      description: Rsync with --prune-empty-dirs
      returned: success
    rsyncDelta:
      type: bool
      description: Rsync with --inplace --no-whole-file
      returned: success
    rsyncBlockSize:
      type: int
      description: Rsync with --block-size=<value> Max 128KB, 0 implies rsync default
      returned: success
    rsyncBandWidthLimit:
      type: int
      description: Rsync with --bwlimit=<value>
      returned: success
    rsyncCompress:
      type: str
      description: Rsync with --compress
      returned: success
    rsyncCompressLevel:
      type: str
      description: Rsync compression at a specific level
      returned: success
    rsyncCheckNetworkMount:
      type: bool
      description: 'Rsync check if file is on remote mount before delete and if so:
        skip it'
      returned: success
    extraRsyncArguments:
      type: str
      description: 'Extra rsync arguments. These can be made condition based on type=no-new-files|normal
        and mode=sync|update|full|sync. For example: --max-delete=0?type=normal&mode=update|sync'
      returned: success
    excludeListSnippets:
      type: list
      description: ''
      returned: success

"""
############################
# Imports
############################

from copy import deepcopy
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import FSPart
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
from ansible_collections.brightcomputing.bcm110.plugins.module_utils.argspecs.fs_part import FSPart_ArgSpec

############################
# main
############################

def main():

    module = BaseModule(
        argument_spec=FSPart_ArgSpec.argument_spec,
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

    entity = entity_manager.lookup_entity(params, FSPart)

    changed = False

    diff = None

    desired_state = params["state"]

    if not entity:
        if desired_state == "present":
            entity, res = entity_manager.create_resource(FSPart, params, commit=not module.check_mode)
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