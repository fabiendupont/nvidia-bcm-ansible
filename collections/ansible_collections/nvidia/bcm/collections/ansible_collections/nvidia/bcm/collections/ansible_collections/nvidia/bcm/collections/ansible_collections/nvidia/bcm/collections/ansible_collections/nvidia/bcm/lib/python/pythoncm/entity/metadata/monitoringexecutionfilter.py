from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringExecutionFilter(Entity):
    class FilterOperation(Enum):
        NONE = auto()
        INCLUDE = auto()
        EXCLUDE = auto()

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
                name="filterOperation",
                kind=MetaData.Type.ENUM,
                description="The filter operation to be performed",
                options=[
                    self.FilterOperation.NONE,
                    self.FilterOperation.INCLUDE,
                    self.FilterOperation.EXCLUDE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.FilterOperation,
                default=self.FilterOperation.INCLUDE,
            )
        )
        self.baseType = 'MonitoringExecutionFilter'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringExecutionFilter']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

