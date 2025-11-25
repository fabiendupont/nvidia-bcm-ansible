# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
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

import importlib
import os
import pkgutil
import sys
import typing

_ENTITY_USING_EXTRA_VALUES_INITIALIZED = False

_LOAD_ALL_METADATA_ENTITY_CLASSES_CALLED = False

# Only top level entities are here.
ENTITY_USING_EXTRA_VALUES = [
    "BootRole",
    "Category",
    "CloudSettings",
    "Device",
    "EC2VPC",
    "EdgeSite",
    "FSExport",
    "FSMount",
    "FirewallPolicy",
    "MonitoringAction",
    "MonitoringDataProducer",
    "Network",
    "NetworkInterface",
    "Node",
    "PowerDistributionUnit",
    "Profile",
    "PrometheusQuery",
    "SNMPSettings",
    "Switch",
    "ZTPSettings",
]

SKIP_LIST_ENTITIES = [
    "MonitoringDataProducerAggregateNode",
    "MonitoringDataProducerAggregatePdu",
    "MonitoringDataProducerAlertLevel",
    "MonitoringDataProducerClusterTotal",
    "MonitoringDataProducerCmDaemonState",
    "MonitoringDataProducerDeviceState",
    "MonitoringDataProducerEc2SpotPrices",
    "MonitoringDataProducerSwitch",
    "MonitoringDataProducerGpu",
    "MonitoringDataProducerJob",
    "MonitoringDataProducerJobMetadata",
    "MonitoringDataProducerJobQueue",
    "MonitoringDataProducerLua",
    "MonitoringDataProducerMonitoringSystem",
    "MonitoringDataProducerPerpetual",
    "MonitoringDataProducerPowerDistributionUnit",
    "MonitoringDataProducerProcMemInfo",
    "MonitoringDataProducerProcMount",
    "MonitoringDataProducerProcNetDev",
    "MonitoringDataProducerProcNetSnmp",
    "MonitoringDataProducerProcPidStat",
    "MonitoringDataProducerProcStat",
    "MonitoringDataProducerProcVmStat",
    "MonitoringDataProducerPrometheus",
    "MonitoringDataProducerRackSensor",
    "MonitoringDataProducerRecorder",
    "MonitoringDataProducerSysBlockStat",
    "MonitoringDataProducerSysInfo",
    "MonitoringDataProducerTest",
    "MonitoringDataProducerTrustedTool",
    "MonitoringDataProducerUserCount",
    "MonitoringPowerOffAction",
    "MonitoringPowerOnAction",
    "MonitoringPowerResetAction",
    "MonitoringRebootAction",
    "MonitoringServiceRestartAction",
    "MonitoringServiceStartAction",
    "MonitoringServiceStopAction",
    "MonitoringShutdownAction",
    "ProgramRunnerStatus",
    "NodeHierarchyRule",  # NOTE: Suggested by Koen to avoid causing harm to the cluster setup.
]

READONLY_ENTITIES = [
    "Session",
    "CMService",
]


def import_entity_meta(name: str) -> type:
    meta_data_cache = importlib.import_module("pythoncm.meta_data_cache")
    return meta_data_cache.MetaDataCache().get(name).__class__


def entity_meta_instance(name: str):
    return import_entity_meta(name)()


def entity_internal_fields() -> list[str]:
    entity_meta_data = import_entity_meta("Entity")
    return [field.name for field in entity_meta_data().fields()]


def load_all_metadata_entity_classes() -> None:
    global _LOAD_ALL_METADATA_ENTITY_CLASSES_CALLED  # pylint: disable=global-statement
    if _LOAD_ALL_METADATA_ENTITY_CLASSES_CALLED:
        return

    entity_meta_data = import_entity_meta("Entity")

    entity_meta_data_module = sys.modules[entity_meta_data.__module__]

    if module_file := entity_meta_data_module.__file__:
        meta_data_module_path = os.path.dirname(module_file)
    else:
        raise RuntimeError(f"Can not find module file for {entity_meta_data.__class__.__module__}")

    for _, name, _ in pkgutil.iter_modules((meta_data_module_path,)):
        _ = importlib.import_module("pythoncm.entity.metadata." + name, __package__)
    _LOAD_ALL_METADATA_ENTITY_CLASSES_CALLED = True


# https://stackoverflow.com/questions/3862310/how-to-find-all-the-subclasses-of-a-class-given-its-name
def all_subclasses(cls: type) -> set[type]:
    load_all_metadata_entity_classes()
    return set(cls.__subclasses__()).union([s for c in cls.__subclasses__() for s in all_subclasses(c)])


def all_leaf_entities_for(entity_name: str) -> dict[str, type]:
    entity_meta_data = import_entity_meta(entity_name)
    return {clazz.__name__: clazz for clazz in all_subclasses(entity_meta_data) if clazz().leaf_entity}


def initialize_entities_using_extra_value_list() -> None:
    global _ENTITY_USING_EXTRA_VALUES_INITIALIZED  # pylint: disable=global-statement
    if _ENTITY_USING_EXTRA_VALUES_INITIALIZED:
        return
    leafs = []
    for entity_name in ENTITY_USING_EXTRA_VALUES:
        leafs.extend([cls.__name__ for cls in all_leaf_entities_for(entity_name).values()])

    ENTITY_USING_EXTRA_VALUES.extend(leafs)
    _ENTITY_USING_EXTRA_VALUES_INITIALIZED = True


def is_extra_value_enabled(entity: str) -> bool:
    initialize_entities_using_extra_value_list()
    return entity in ENTITY_USING_EXTRA_VALUES


def get_meta_data_class():
    metadata_mod = importlib.import_module("pythoncm.entity.meta_data")
    return metadata_mod.MetaData()


def expand_field_to_leaf_entites(field) -> list[typing.NamedTuple]:
    metadata = import_entity_meta(field.instance)
    subclasses = [subclass for subclass in all_subclasses(metadata) if subclass().leaf_entity]
    return [field._replace(name=f"{field.name}_{clazz.__name__}", instance=clazz.__name__) for clazz in subclasses]


def all_leaf_entities() -> dict[str, type]:
    return all_leaf_entities_for("Entity")


def all_top_level_entities() -> dict[str, type]:
    entity_meta_data: type = import_entity_meta("Entity")
    return {clazz.__name__: clazz for clazz in all_subclasses(entity_meta_data) if clazz().top_level}


def is_deprecated_entity(entity_name: str) -> bool:
    return entity_name.lower().startswith("openstack")


def is_skip_listed_entity(entity_name: str) -> bool:
    return entity_name in SKIP_LIST_ENTITIES


def is_readonly_entity(entity_name: str) -> bool:
    return entity_name in READONLY_ENTITIES