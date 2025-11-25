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
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

__metaclass__ = type

from ansible.errors import AnsibleAction
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display

display = Display()

CM_PYTHON3 = "/cm/local/apps/python3/bin/python"


class BaseActionModule(ActionBase):
    """
    Base action module association with all brightcomputing.bcm modules.
    This module will cary out any preparation needed such as setting up cm-python3 usage.
    """

    MODULE_NAME = None

    def run(self, tmp=None, task_vars=None):
        assert self.MODULE_NAME is not None, "MODULE_NAME should be set."

        if task_vars is None:
            task_vars = {}
        result = super(BaseActionModule, self).run(tmp, task_vars)
        del tmp

        try:

            new_task_vars = task_vars.copy()
            display.vvvv("Setting variable 'ansible_python_interpreter' to %s" % CM_PYTHON3)
            new_task_vars["ansible_python_interpreter"] = CM_PYTHON3

            display.vvvv("Running %s" % self.MODULE_NAME)
            result.update(
                self._execute_module(
                    module_name=self.MODULE_NAME,
                    module_args=self._task.args,
                    task_vars=new_task_vars,
                    wrap_async=self._task.async_val
                )
            )
        except AnsibleAction as e:
            result.update(e.result)
        finally:
            if not self._task.async_val:
                self._remove_tmp_path(self._connection._shell.tmpdir)
        return result