from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ExternalOperationResult(Entity):
    class Result(Enum):
        GOOD = auto()
        FAILED = auto()
        BUSY = auto()
        DIFFERENT = auto()
        STOPPED = auto()
        TIMEOUT = auto()
        EMPTY = auto()
        NO_SUCH_DEVICE = auto()
        NO_SUCH_DPU_NODE = auto()
        ERROR = auto()
        DOWN = auto()

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
                name="result",
                kind=MetaData.Type.ENUM,
                description="Result",
                options=[
                    self.Result.GOOD,
                    self.Result.FAILED,
                    self.Result.BUSY,
                    self.Result.DIFFERENT,
                    self.Result.STOPPED,
                    self.Result.TIMEOUT,
                    self.Result.EMPTY,
                    self.Result.NO_SUCH_DEVICE,
                    self.Result.NO_SUCH_DPU_NODE,
                    self.Result.ERROR,
                    self.Result.DOWN,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Result,
                default=self.Result.GOOD,
            )
        )
        self.baseType = 'ExternalOperationResult'
        self.service_type = self.baseType
        self.allTypes = ['ExternalOperationResult']
        self.leaf_entity = False
        self.add_to_cluster = False
        self.allow_commit = False

