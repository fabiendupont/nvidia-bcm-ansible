from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PowerOperationHistory(Entity):
    class Operation(Enum):
        ON = auto()
        OFF = auto()
        RESET = auto()
        REBOOT = auto()
        SHUTDOWN = auto()
        AUXCYCLE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_device_uuid",
                kind=MetaData.Type.UUID,
                description="Device",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="executionTime",
                kind=MetaData.Type.UINT,
                description="Execution time in milliseconds after epoch",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="operation",
                kind=MetaData.Type.ENUM,
                description="Operation",
                options=[
                    self.Operation.ON,
                    self.Operation.OFF,
                    self.Operation.RESET,
                    self.Operation.REBOOT,
                    self.Operation.SHUTDOWN,
                    self.Operation.AUXCYCLE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Operation,
                default=self.Operation.ON,
            )
        )
        self.meta.add(
            MetaDataField(
                name="success",
                kind=MetaData.Type.BOOL,
                description="Success",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="message",
                kind=MetaData.Type.STRING,
                description="Message",
                default='',
            )
        )
        self.baseType = 'PowerOperationHistory'
        self.service_type = self.baseType
        self.allTypes = ['PowerOperationHistory']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

