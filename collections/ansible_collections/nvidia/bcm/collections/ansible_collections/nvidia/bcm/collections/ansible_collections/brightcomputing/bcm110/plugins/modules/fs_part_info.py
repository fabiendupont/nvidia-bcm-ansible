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
module: fs_part_info
description: Query cmdaemon for entity of type FSPart
options:
    
requirements: [cmdaemon-pythoncm]
author:
- iiiteam <iiiteam@brightcomputing.com>
"""

EXAMPLES = r"""

"""

RETURN = r"""
---
fs_part:
  type: list
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

import json
import traceback

try:
    from pythoncm.cluster import Cluster
    from pythoncm.entity import FSPart
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

    results = entity_query.find(FSPart)

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

    module.exit_json(fs_parts=json_ready_result, changed=False)


if __name__ == '__main__':
    main()