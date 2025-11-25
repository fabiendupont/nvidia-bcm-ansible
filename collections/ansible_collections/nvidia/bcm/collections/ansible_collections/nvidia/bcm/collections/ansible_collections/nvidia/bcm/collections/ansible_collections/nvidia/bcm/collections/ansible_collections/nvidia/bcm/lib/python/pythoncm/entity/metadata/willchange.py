from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class WillChange(Entity):
    class AutoChange(Enum):
        NO = auto()
        YES = auto()
        FORCE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_base_type",
                kind=MetaData.Type.STRING,
                description="Base type",
                default='',
            )
        )
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
                name="parameter",
                kind=MetaData.Type.STRING,
                description="Parameter",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="auto_change",
                kind=MetaData.Type.ENUM,
                description="Auto change",
                options=[
                    self.AutoChange.NO,
                    self.AutoChange.YES,
                    self.AutoChange.FORCE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.AutoChange,
                default=self.AutoChange.NO,
            )
        )
        self.baseType = 'WillChange'
        self.service_type = self.baseType
        self.allTypes = ['WillChange']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

