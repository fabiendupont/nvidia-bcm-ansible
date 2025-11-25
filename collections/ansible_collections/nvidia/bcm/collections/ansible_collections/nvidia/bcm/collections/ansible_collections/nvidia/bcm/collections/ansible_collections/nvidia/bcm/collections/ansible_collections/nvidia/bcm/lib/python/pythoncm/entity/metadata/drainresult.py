from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class DrainResult(Entity):
    class Result(Enum):
        NOTANODE = auto()
        DRAINED = auto()
        UNDRAINED = auto()
        INVALID = auto()
        FAILED = auto()
        UNKNOWN = auto()
        DRAINING = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_entity_uuid",
                kind=MetaData.Type.UUID,
                description="Entity",
                default=self.zero_uuid,
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
                name="ref_node_uuids",
                kind=MetaData.Type.UUID,
                description="Node",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_queue_uuids",
                kind=MetaData.Type.UUID,
                description="Job queue",
                entity_allow_null=True,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="reason",
                kind=MetaData.Type.STRING,
                description="Reason",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="result",
                kind=MetaData.Type.ENUM,
                description="Result",
                options=[
                    self.Result.NOTANODE,
                    self.Result.DRAINED,
                    self.Result.UNDRAINED,
                    self.Result.INVALID,
                    self.Result.FAILED,
                    self.Result.UNKNOWN,
                    self.Result.DRAINING,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Result,
                vector=True,
                default=[],
            )
        )
        self.baseType = 'DrainResult'
        self.service_type = self.baseType
        self.allTypes = ['DrainResult']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

