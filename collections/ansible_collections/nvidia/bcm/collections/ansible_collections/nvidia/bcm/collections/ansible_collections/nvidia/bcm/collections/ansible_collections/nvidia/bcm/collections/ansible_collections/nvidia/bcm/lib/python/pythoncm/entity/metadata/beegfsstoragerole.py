from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class BeeGFSStorageRole(Role):
    """
    BeeGFS storage role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="configurations",
                kind=MetaData.Type.ENTITY,
                description="List of BeeGFS storage configurations",
                instance='BeeGFSStorageConfig',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'BeeGFSStorageRole'
        self.service_type = self.baseType
        self.allTypes = ['BeeGFSStorageRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

