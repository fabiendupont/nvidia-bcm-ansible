from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Consolidator(Entity):
    class Kind(Enum):
        AVERAGE = auto()
        MINIMUM = auto()
        MAXIMUM = auto()

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
                name="maxAge",
                kind=MetaData.Type.FLOAT,
                description="Maximal age of historic data, 0 for forever",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxSamples",
                kind=MetaData.Type.UINT,
                description="Maximal samples of historic data, 0 for no limit",
                default=65536,
            )
        )
        self.meta.add(
            MetaDataField(
                name="interval",
                kind=MetaData.Type.FLOAT,
                description="Consolidation interval",
                default=3600,
            )
        )
        self.meta.add(
            MetaDataField(
                name="offset",
                kind=MetaData.Type.FLOAT,
                description="Time offset for sampling interval",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="kind",
                kind=MetaData.Type.ENUM,
                description="Kind of consolidation to be done",
                options=[
                    self.Kind.AVERAGE,
                    self.Kind.MINIMUM,
                    self.Kind.MAXIMUM,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Kind,
                default=self.Kind.AVERAGE,
            )
        )
        self.baseType = 'Consolidator'
        self.service_type = self.baseType
        self.allTypes = ['Consolidator']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

