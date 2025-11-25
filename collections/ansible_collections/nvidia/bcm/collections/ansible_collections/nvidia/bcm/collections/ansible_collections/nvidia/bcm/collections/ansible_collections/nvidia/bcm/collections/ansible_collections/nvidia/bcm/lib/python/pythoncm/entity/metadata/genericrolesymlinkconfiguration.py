from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.genericroleconfiguration import GenericRoleConfiguration


class GenericRoleSymlinkConfiguration(GenericRoleConfiguration):
    """
    Generic role symlink configuration
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="sourceFilename",
                kind=MetaData.Type.STRING,
                description="Source filename",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="watch",
                kind=MetaData.Type.BOOL,
                description="Watch source file for changes, and treat as file change",
                default=False,
            )
        )
        self.baseType = 'GenericRoleConfiguration'
        self.childType = 'GenericRoleSymlinkConfiguration'
        self.service_type = self.baseType
        self.allTypes = ['GenericRoleSymlinkConfiguration', 'GenericRoleConfiguration']
        self.top_level = False
        self.leaf_entity = True

