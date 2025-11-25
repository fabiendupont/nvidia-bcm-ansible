from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class HeadNodeRole(Role):
    """
    Headnode role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="failoverId",
                kind=MetaData.Type.UINT,
                clone=False,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disableAutomaticExports",
                kind=MetaData.Type.BOOL,
                description="Disable creation of automatic filesystem exports",
                default=False,
            )
        )
        self.baseType = 'Role'
        self.childType = 'HeadNodeRole'
        self.service_type = self.baseType
        self.allTypes = ['HeadNodeRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

