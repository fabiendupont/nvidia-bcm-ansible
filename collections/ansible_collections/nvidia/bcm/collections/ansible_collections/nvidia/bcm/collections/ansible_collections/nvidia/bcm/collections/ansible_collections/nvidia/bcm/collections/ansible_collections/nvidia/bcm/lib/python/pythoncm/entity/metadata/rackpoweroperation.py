from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class RackPowerOperation(Entity):
    class Operation(Enum):
        FULL_ON = auto()
        FULL_OFF = auto()
        DOMAIN_ON = auto()
        DOMAIN_OFF = auto()
        COMPUTE_ON = auto()
        COMPUTE_OFF = auto()
        EMERGENCY_OFF = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="racks",
                kind=MetaData.Type.UUID,
                description="Racks",
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
                name="operation",
                kind=MetaData.Type.ENUM,
                description="Operation to be performed",
                options=[
                    self.Operation.FULL_ON,
                    self.Operation.FULL_OFF,
                    self.Operation.DOMAIN_ON,
                    self.Operation.DOMAIN_OFF,
                    self.Operation.COMPUTE_ON,
                    self.Operation.COMPUTE_OFF,
                    self.Operation.EMERGENCY_OFF,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Operation,
                default=self.Operation.COMPUTE_ON,
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
                name="message",
                kind=MetaData.Type.STRING,
                description="Message",
                default='',
            )
        )
        self.baseType = 'RackPowerOperation'
        self.service_type = self.baseType
        self.allTypes = ['RackPowerOperation']
        self.top_level = False
        self.leaf_entity = True

