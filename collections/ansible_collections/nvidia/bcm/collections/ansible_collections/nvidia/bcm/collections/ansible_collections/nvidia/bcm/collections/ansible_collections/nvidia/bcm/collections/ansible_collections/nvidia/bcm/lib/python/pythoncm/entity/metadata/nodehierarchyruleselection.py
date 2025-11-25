from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class NodeHierarchyRuleSelection(Entity):
    class Operation(Enum):
        INCLUDE = auto()
        EXCLUDE = auto()
        DISABLED = auto()

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
                name="operation",
                kind=MetaData.Type.ENUM,
                description="Operation",
                options=[
                    self.Operation.INCLUDE,
                    self.Operation.EXCLUDE,
                    self.Operation.DISABLED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Operation,
                default=self.Operation.INCLUDE,
            )
        )
        self.baseType = 'NodeHierarchyRuleSelection'
        self.service_type = self.baseType
        self.allTypes = ['NodeHierarchyRuleSelection']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

