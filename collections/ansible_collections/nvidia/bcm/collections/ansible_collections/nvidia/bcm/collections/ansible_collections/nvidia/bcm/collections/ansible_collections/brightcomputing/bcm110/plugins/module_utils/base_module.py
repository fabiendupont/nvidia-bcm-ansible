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

from copy import deepcopy

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import _load_params


def filter_params(params, module_params):
    """
    Filter out the parameters set to a default of None by the ansible module,
    but keep those explicitly set to None in the playbook.
    """
    filtered = {}
    for param, value in params.items():
        if isinstance(value, dict):
            filtered[param] = filter_params(value, module_params[param])
        elif isinstance(value, list) and value and isinstance(value[0], dict):
            filtered[param] = [filter_params(x, module_params[param][value.index(x)]) for x in value]
        elif value is not None or param in module_params:
            filtered[param] = value

    return filtered


class BaseModule(AnsibleModule):
    # Override _load_params so we can track the provided parameters vs. those
    # set to a default of None by the ansible module.
    def _load_params(self):
        self._raw_params = _load_params()
        self.params = deepcopy(self._raw_params)

    # Filter out the parameters set to a default of None by the ansible module.
    @property
    def bright_params(self):
        return filter_params(self.params, self._raw_params)