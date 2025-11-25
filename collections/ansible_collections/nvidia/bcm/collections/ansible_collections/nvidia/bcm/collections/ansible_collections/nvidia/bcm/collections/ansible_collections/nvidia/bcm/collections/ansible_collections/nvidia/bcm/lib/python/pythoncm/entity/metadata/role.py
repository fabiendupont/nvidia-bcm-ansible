from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Role(Entity):
    """
    Role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                required=True,
                diff_type=MetaDataField.Diff.disabled,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="addServices",
                kind=MetaData.Type.BOOL,
                description="Add services to nodes which belong to this node. Be careful setting this to false.",
                default=True,
            )
        )
        self.baseType = 'Role'
        self.service_type = self.baseType
        self.allTypes = ['Role']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

