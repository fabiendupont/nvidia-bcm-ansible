from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.directorrole import DirectorRole


class CloudDirectorRole(DirectorRole):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="bootImageFromProvisioningRole",
                kind=MetaData.Type.BOOL,
                description="Only allow nodes to boot from images defined in the provisioning role",
                default=True,
            )
        )
        self.baseType = 'Role'
        self.childType = 'CloudDirectorRole'
        self.service_type = self.baseType
        self.allTypes = ['CloudDirectorRole', 'DirectorRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

