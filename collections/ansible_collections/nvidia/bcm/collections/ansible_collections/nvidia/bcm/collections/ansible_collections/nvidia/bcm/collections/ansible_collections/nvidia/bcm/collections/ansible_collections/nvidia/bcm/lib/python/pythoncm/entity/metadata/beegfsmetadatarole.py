from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class BeeGFSMetadataRole(Role):
    """
    BeeGFS metadata role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="configurations",
                kind=MetaData.Type.ENTITY,
                description="List of BeeGFS metadata configurations",
                instance='BeeGFSMetadataConfig',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'BeeGFSMetadataRole'
        self.service_type = self.baseType
        self.allTypes = ['BeeGFSMetadataRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

