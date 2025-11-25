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
from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible_collections.brightcomputing.bcm110.plugins.module_utils.base_action_module import BaseActionModule

class ActionModule(BaseActionModule):

    """
    Action module association with brightcomputing.bcm110.monitoring_data_producer_aggregate_power_circuit.
    """
    MODULE_NAME = "brightcomputing.bcm110.monitoring_data_producer_aggregate_power_circuit"