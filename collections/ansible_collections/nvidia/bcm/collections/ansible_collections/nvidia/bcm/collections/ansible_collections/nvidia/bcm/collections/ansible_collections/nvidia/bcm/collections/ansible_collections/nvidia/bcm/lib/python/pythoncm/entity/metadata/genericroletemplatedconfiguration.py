from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.genericroleconfiguration import GenericRoleConfiguration


class GenericRoleTemplatedConfiguration(GenericRoleConfiguration):
    """
    Generic role templated configuration
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="templateContent",
                kind=MetaData.Type.STRING,
                description="Template to use for writing file",
                default='',
            )
        )
        self.baseType = 'GenericRoleConfiguration'
        self.childType = 'GenericRoleTemplatedConfiguration'
        self.service_type = self.baseType
        self.allTypes = ['GenericRoleTemplatedConfiguration', 'GenericRoleConfiguration']
        self.top_level = False
        self.leaf_entity = True

