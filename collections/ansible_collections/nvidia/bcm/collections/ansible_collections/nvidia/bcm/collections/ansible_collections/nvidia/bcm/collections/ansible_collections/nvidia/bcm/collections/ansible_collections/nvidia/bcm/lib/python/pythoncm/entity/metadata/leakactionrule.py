from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class LeakActionRule(Entity):
    class Scope(Enum):
        DEVICE = auto()
        RACK = auto()
        CDU = auto()
        ROW = auto()
        ROOM = auto()
        BUILDING = auto()
        LOCATION = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="scope",
                kind=MetaData.Type.ENUM,
                description="Scope of the leak action rule",
                options=[
                    self.Scope.DEVICE,
                    self.Scope.RACK,
                    self.Scope.CDU,
                    self.Scope.ROW,
                    self.Scope.ROOM,
                    self.Scope.BUILDING,
                    self.Scope.LOCATION,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Scope,
                default=self.Scope.RACK,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disabled",
                kind=MetaData.Type.BOOL,
                description="Disable the rule",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="minimalDevices",
                kind=MetaData.Type.UINT,
                description="Minimal devices that need to report leaks before the rule to become active",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maximalDevices",
                kind=MetaData.Type.UINT,
                description="Maximal devices that are allowed to report leaks before the rule to become inactive",
                default=100,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gracePeriod",
                kind=MetaData.Type.UINT,
                description="Delay since the rule becomes active before running the actions",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="correlationWindow",
                kind=MetaData.Type.UINT,
                description="Temporal window in which two separate leaks are considered correlated",
                default=300,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerOff",
                kind=MetaData.Type.BOOL,
                description="Power off devices in the scope of the rule",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerOffRack",
                kind=MetaData.Type.BOOL,
                description="Power off all devices in the scope of the rule, via rack power operation and fallback to per device",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="electricalIsolation",
                kind=MetaData.Type.BOOL,
                description="Electrically isolate the devices in the scope of the rule",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="liquidIsolation",
                kind=MetaData.Type.BOOL,
                description="Liquid isolate the devices in the scope of the rule",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="minimalSeverity",
                kind=MetaData.Type.UINT,
                description="Minimal severity that need to report leaks before the rule to become active",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maximalSeverity",
                kind=MetaData.Type.UINT,
                description="Maximal severity that is allowed to report leaks before the rule to become inactive",
                default=100,
            )
        )
        self.baseType = 'LeakActionRule'
        self.service_type = self.baseType
        self.allTypes = ['LeakActionRule']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

