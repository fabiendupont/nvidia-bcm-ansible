from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class FSPartRole(Role):
    """
    FSPart role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="fsparts",
                kind=MetaData.Type.RESOLVE,
                description="FSParts",
                instance='FSPart',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="fspartSource",
                kind=MetaData.Type.BOOL,
                description="Server as source for all these FSParts",
                default=True,
            )
        )
        self.baseType = 'Role'
        self.childType = 'FSPartRole'
        self.service_type = self.baseType
        self.allTypes = ['FSPartRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

