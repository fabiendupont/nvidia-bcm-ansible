from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class BeeGFSHelperRole(Role):
    """
    BeeGFS helper role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="configurations",
                kind=MetaData.Type.ENTITY,
                description="List of BeeGFS helper configurations",
                instance='BeeGFSHelperConfig',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'BeeGFSHelperRole'
        self.service_type = self.baseType
        self.allTypes = ['BeeGFSHelperRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

