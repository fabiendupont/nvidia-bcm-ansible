from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ProjectManager(Entity):
    class Operator(Enum):
        AND = auto()
        OR = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="users",
                kind=MetaData.Type.STRING,
                description="List of users managed",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="accounts",
                kind=MetaData.Type.STRING,
                description="List of accounts managed",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="op",
                kind=MetaData.Type.ENUM,
                description="Job needs to belong to one of the users and/or accounts",
                options=[
                    self.Operator.AND,
                    self.Operator.OR,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Operator,
                default=self.Operator.OR,
            )
        )
        self.baseType = 'ProjectManager'
        self.service_type = self.baseType
        self.allTypes = ['ProjectManager']
        self.top_level = False
        self.leaf_entity = True

