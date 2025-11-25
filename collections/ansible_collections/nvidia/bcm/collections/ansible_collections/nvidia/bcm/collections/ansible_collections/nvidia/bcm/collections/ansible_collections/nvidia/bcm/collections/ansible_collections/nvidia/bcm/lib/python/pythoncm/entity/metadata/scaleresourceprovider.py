from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ScaleResourceProvider(Entity):
    class LongStartingNodeActionType(Enum):
        NONE = auto()
        POWEROFF = auto()
        TERMINATE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Resource provider name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="enabled",
                kind=MetaData.Type.BOOL,
                description="Resource provider is currently enabled",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="priority",
                kind=MetaData.Type.UINT,
                description="Node provider priority",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="wholeTime",
                kind=MetaData.Type.UINT,
                description="A compute node running time (in minutes) before it is stopped if no workload requires it",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="stoppingAllowancePeriod",
                kind=MetaData.Type.UINT,
                description="A time (in minutes) just before the end of the wholeTime period prior to which all power off (or terminate) operations must be started",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="keepRunning",
                kind=MetaData.Type.STRING,
                description="Nodes that should not be stopped or terminated even if they are unused (range format)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="extraNodes",
                kind=MetaData.Type.STRING,
                description="Nodes that should be started before regular nodes",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="extraNodeIdleTime",
                kind=MetaData.Type.UINT,
                description="Time that extra nodes can remain unused (after this time they are stopped)",
                default=3600,
            )
        )
        self.meta.add(
            MetaDataField(
                name="extraNodeStart",
                kind=MetaData.Type.BOOL,
                description="Automatically start extra node before the first compute node is started",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="extraNodeStop",
                kind=MetaData.Type.BOOL,
                description="Automatically stop extra node after the last compute node stops",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="allocationProlog",
                kind=MetaData.Type.STRING,
                description="Script that is executed when a node is allocated to a workload",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="allocationEpilog",
                kind=MetaData.Type.STRING,
                description="Script that is executed when a node is deallocated",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="allocationScriptsTimeout",
                kind=MetaData.Type.UINT,
                description="Allocation scripts timeout",
                default=10,
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultResources",
                kind=MetaData.Type.STRING,
                description="List of default resources in format [name=value]",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="shutdownEnabled",
                kind=MetaData.Type.BOOL,
                description="Shutdown nodes instead of just power off, and wait until a set timeout before doing a hard power off",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="shutdownTimeout",
                kind=MetaData.Type.UINT,
                description="Shutdown timeout before powering off",
                default=180,
            )
        )
        self.meta.add(
            MetaDataField(
                name="longStartingNodeAction",
                kind=MetaData.Type.ENUM,
                description="Action applied to nodes that start for too long",
                options=[
                    self.LongStartingNodeActionType.NONE,
                    self.LongStartingNodeActionType.POWEROFF,
                    self.LongStartingNodeActionType.TERMINATE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.LongStartingNodeActionType,
                default=self.LongStartingNodeActionType.NONE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="longStartingNodeTimeout",
                kind=MetaData.Type.UINT,
                description="How long Auto Scaler should wait before the action is applied for long starting nodes",
                default=600,
            )
        )
        self.meta.add(
            MetaDataField(
                name="options",
                kind=MetaData.Type.STRING,
                description="Additional resource provider related parameters that will be passed to cm-scale daemon",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'ScaleResourceProvider'
        self.service_type = self.baseType
        self.allTypes = ['ScaleResourceProvider']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

