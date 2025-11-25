from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PowerStatus(Entity):
    class Action(Enum):
        ON = auto()
        OFF = auto()
        RESET = auto()
        UNKNOWN = auto()
        FAILED = auto()
        PDU_OFF = auto()
        SKIPPED = auto()
        PENDING = auto()
        CANCELED = auto()
        AUXCYCLE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="device",
                kind=MetaData.Type.UUID,
                description="Device",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="host",
                kind=MetaData.Type.UUID,
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerDistributionUnit",
                kind=MetaData.Type.UUID,
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gpu",
                kind=MetaData.Type.INT,
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="port",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="state",
                kind=MetaData.Type.ENUM,
                options=[
                    self.Action.ON,
                    self.Action.OFF,
                    self.Action.RESET,
                    self.Action.UNKNOWN,
                    self.Action.FAILED,
                    self.Action.PDU_OFF,
                    self.Action.SKIPPED,
                    self.Action.PENDING,
                    self.Action.CANCELED,
                    self.Action.AUXCYCLE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Action,
                default=self.Action.UNKNOWN,
            )
        )
        self.meta.add(
            MetaDataField(
                name="msg",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="extendedMsg",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="indexes",
                kind=MetaData.Type.INT,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="tracker",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="retries",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.baseType = 'PowerStatus'
        self.service_type = self.baseType
        self.allTypes = ['PowerStatus']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

