from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GenericRoleEnvironment(Entity):
    """
    Generic role environment
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                regex_check=r"^[a-zA-Z0-9_]+$",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="value",
                kind=MetaData.Type.STRING,
                description="Value",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeEnvironment",
                kind=MetaData.Type.BOOL,
                description="Update the node environment variables",
                default=False,
            )
        )
        self.baseType = 'GenericRoleEnvironment'
        self.service_type = self.baseType
        self.allTypes = ['GenericRoleEnvironment']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

