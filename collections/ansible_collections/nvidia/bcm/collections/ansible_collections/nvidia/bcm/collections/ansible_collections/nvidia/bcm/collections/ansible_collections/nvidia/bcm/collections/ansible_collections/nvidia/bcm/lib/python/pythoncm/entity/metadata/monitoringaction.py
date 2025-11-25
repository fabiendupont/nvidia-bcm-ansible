from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringAction(Entity):
    class RunOn(Enum):
        NODE = auto()
        ACTIVE = auto()
        MONITORING_NODE = auto()

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
                name="runOn",
                kind=MetaData.Type.ENUM,
                description="Run the action on",
                options=[
                    self.RunOn.NODE,
                    self.RunOn.ACTIVE,
                    self.RunOn.MONITORING_NODE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.RunOn,
                default=self.RunOn.ACTIVE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowedTime",
                kind=MetaData.Type.STRING,
                description="Sets time interval during which action is allowed to be executed",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="disable",
                kind=MetaData.Type.BOOL,
                description="Disable",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="suppressedByGoingDown",
                kind=MetaData.Type.BOOL,
                description="Suppress running action if device is going down",
                default=False,
            )
        )
        self.baseType = 'MonitoringAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringAction']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

