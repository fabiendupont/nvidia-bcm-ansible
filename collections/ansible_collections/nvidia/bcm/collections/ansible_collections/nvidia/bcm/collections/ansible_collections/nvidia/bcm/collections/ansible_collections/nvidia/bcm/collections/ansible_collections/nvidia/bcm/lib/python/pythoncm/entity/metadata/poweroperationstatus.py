from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PowerOperationStatus(Entity):
    class State(Enum):
        WAITING = auto()
        BUSY = auto()
        DONE = auto()
        CANCELED = auto()
        UNDEFINED = auto()

    class Operation(Enum):
        ON = auto()
        OFF = auto()
        RESET = auto()
        STATUS = auto()
        AUXCYCLE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="state",
                kind=MetaData.Type.ENUM,
                description="State of the operation",
                options=[
                    self.State.WAITING,
                    self.State.BUSY,
                    self.State.DONE,
                    self.State.CANCELED,
                    self.State.UNDEFINED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.State,
                default=self.State.WAITING,
            )
        )
        self.meta.add(
            MetaDataField(
                name="operation",
                kind=MetaData.Type.ENUM,
                description="Operation to be performed",
                options=[
                    self.Operation.ON,
                    self.Operation.OFF,
                    self.Operation.RESET,
                    self.Operation.STATUS,
                    self.Operation.AUXCYCLE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Operation,
                default=self.Operation.STATUS,
            )
        )
        self.meta.add(
            MetaDataField(
                name="executionTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Execution time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="info",
                kind=MetaData.Type.STRING,
                description="Extra information about the power operation",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="retries",
                kind=MetaData.Type.UINT,
                description="Number of retries",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="devices",
                kind=MetaData.Type.UUID,
                description="Devices",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="index",
                kind=MetaData.Type.INT,
                description="Indexes of power operation",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'PowerOperationStatus'
        self.service_type = self.baseType
        self.allTypes = ['PowerOperationStatus']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

