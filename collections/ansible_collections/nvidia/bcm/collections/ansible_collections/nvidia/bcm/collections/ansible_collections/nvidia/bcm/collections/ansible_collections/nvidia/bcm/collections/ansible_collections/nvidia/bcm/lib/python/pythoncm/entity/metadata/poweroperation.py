from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PowerOperation(Entity):
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
                name="devices",
                kind=MetaData.Type.UUID,
                description="Devices",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="pdus",
                kind=MetaData.Type.UUID,
                description="A list of (PDU, port) pairs",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="pdu_ports",
                kind=MetaData.Type.INT,
                description="A list of (PDU, port) pairs",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="shelves",
                kind=MetaData.Type.UUID,
                description="A list of (PowerShelf, PSU) pairs",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="shelf_psus",
                kind=MetaData.Type.INT,
                description="A list of (PowerShelf, PSU) pairs",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="session_uuid",
                kind=MetaData.Type.UUID,
                description="Session",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="force",
                kind=MetaData.Type.BOOL,
                description="Set to true to also do power operation on closed devices",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="delay",
                kind=MetaData.Type.UINT,
                description="Delay between sequencial operations in milliseconds",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="deviceDelay",
                kind=MetaData.Type.INT,
                description="Individual device delay in milliseconds",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="headIndex",
                kind=MetaData.Type.UINT,
                description="Should be 0",
                default=0,
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
                name="retryCount",
                kind=MetaData.Type.UINT,
                description="Number of times to retry on failure",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="retryDelay",
                kind=MetaData.Type.UINT,
                description="Delay between consecutive tries in milliseconds",
                default=0,
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
        self.baseType = 'PowerOperation'
        self.service_type = self.baseType
        self.allTypes = ['PowerOperation']
        self.top_level = False
        self.leaf_entity = True

