from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.genericroleconfiguration import GenericRoleConfiguration


class GenericRoleStaticConfiguration(GenericRoleConfiguration):
    """
    Generic role static configuration
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="content",
                kind=MetaData.Type.STRING,
                description="Content to write into file",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="filemask",
                kind=MetaData.Type.UINT,
                description="Filemask",
                default=0o644,
            )
        )
        self.baseType = 'GenericRoleConfiguration'
        self.childType = 'GenericRoleStaticConfiguration'
        self.service_type = self.baseType
        self.allTypes = ['GenericRoleStaticConfiguration', 'GenericRoleConfiguration']
        self.top_level = False
        self.leaf_entity = True

