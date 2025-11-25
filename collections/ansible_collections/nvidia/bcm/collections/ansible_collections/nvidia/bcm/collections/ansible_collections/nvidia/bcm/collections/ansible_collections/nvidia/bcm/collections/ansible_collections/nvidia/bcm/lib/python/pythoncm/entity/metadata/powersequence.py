from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PowerSequence(Entity):
    class Result(Enum):
        FAIL = auto()
        GOOD = auto()
        DONE = auto()
        CANCELED = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="rack",
                kind=MetaData.Type.UUID,
                description="Rack",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="result",
                kind=MetaData.Type.ENUM,
                options=[
                    self.Result.FAIL,
                    self.Result.GOOD,
                    self.Result.DONE,
                    self.Result.CANCELED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Result,
                default=self.Result.FAIL,
            )
        )
        self.meta.add(
            MetaDataField(
                name="stage",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="message",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="last",
                kind=MetaData.Type.BOOL,
                default=False,
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
        self.baseType = 'PowerSequence'
        self.service_type = self.baseType
        self.allTypes = ['PowerSequence']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

