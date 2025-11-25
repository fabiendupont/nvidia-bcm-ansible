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


def load_implementation_or_prototype():
    """
    Magic function to preload entity
    - implementation, if it exists
    - prototype, if no implementation exists
    """
    import os

    from pythoncm.entity import prototype

    base = os.path.dirname(os.path.realpath(__file__))
    entity_directory = 'pythoncm/entity'
    prototype_directory = entity_directory + '/prototype'
    for module_name, class_name in prototype.pythoncm_entity_hierarchy:
        filename = entity_directory + '/' + module_name + '.py'
        fullpath = base + '/' + module_name + '.py'
        if os.path.exists(fullpath):
            module_path = filename[:-3]
        else:
            module_path = prototype_directory + '.' + module_name
        module_path = module_path.replace('/', '.')
        module = __import__(
            module_path,
            None,
            None,
            [class_name],
            level=0,
        )  # Do not add globals() here, won't work
        # CM-18431: attempt to find way to load module, not class
        globals()[class_name] = getattr(module, class_name)


load_implementation_or_prototype()

# Clean up, so there are no leftovers, except the things we want
del load_implementation_or_prototype
