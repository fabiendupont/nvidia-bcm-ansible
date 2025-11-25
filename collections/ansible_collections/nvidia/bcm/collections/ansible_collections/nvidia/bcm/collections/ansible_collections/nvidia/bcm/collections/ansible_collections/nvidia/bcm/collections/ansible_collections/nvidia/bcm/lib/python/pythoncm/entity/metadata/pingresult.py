from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PingResult(Entity):
    class Result(Enum):
        OK = auto()
        ERROR = auto()
        FAILED = auto()
        TIMEOUT = auto()
        NO_ADDRESS = auto()
        UNREACHABLE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="source",
                kind=MetaData.Type.UUID,
                description="Source",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="destination",
                kind=MetaData.Type.UUID,
                description="Destination",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="result",
                kind=MetaData.Type.ENUM,
                description="Result of the ping operation",
                options=[
                    self.Result.OK,
                    self.Result.ERROR,
                    self.Result.FAILED,
                    self.Result.TIMEOUT,
                    self.Result.NO_ADDRESS,
                    self.Result.UNREACHABLE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Result,
                default=self.Result.OK,
            )
        )
        self.meta.add(
            MetaDataField(
                name="latency",
                kind=MetaData.Type.FLOAT,
                description="Round trip latency",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="sequenceId",
                kind=MetaData.Type.UINT,
                description="Sequence ID",
                default=0,
            )
        )
        self.baseType = 'PingResult'
        self.service_type = self.baseType
        self.allTypes = ['PingResult']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

