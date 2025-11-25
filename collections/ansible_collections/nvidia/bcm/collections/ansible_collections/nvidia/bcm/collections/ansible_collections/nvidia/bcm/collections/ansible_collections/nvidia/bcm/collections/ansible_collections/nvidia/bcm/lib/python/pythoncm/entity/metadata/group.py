from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Group(Entity):
    """
    Group
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ID",
                kind=MetaData.Type.STRING,
                description="Group ID",
                regex_check=r"^(|\d+)$",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Group name",
                regex_check=r"^[a-zA-Z_]([.a-zA-Z0-9_-]{0,31}|[.a-zA-Z0-9_-]{0,30}\$)$",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="members",
                kind=MetaData.Type.STRING,
                description="Users belonging to this group",
                regex_check=r"^[a-zA-Z_]([.a-zA-Z0-9_-]{0,31}|[.a-zA-Z0-9_-]{0,30}\$)$",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Group'
        self.service_type = self.baseType
        self.allTypes = ['Group']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

