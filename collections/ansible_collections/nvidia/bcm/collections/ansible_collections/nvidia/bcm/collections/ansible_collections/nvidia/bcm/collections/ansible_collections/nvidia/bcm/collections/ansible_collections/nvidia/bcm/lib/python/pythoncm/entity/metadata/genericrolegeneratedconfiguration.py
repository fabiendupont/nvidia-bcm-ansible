from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.genericroleconfiguration import GenericRoleConfiguration


class GenericRoleGeneratedConfiguration(GenericRoleConfiguration):
    """
    Generic role generated configuration
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="script",
                kind=MetaData.Type.STRING,
                description="Script",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="arguments",
                kind=MetaData.Type.STRING,
                description="Arguments",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeout",
                kind=MetaData.Type.UINT,
                description="Timeout",
                default=15,
            )
        )
        self.meta.add(
            MetaDataField(
                name="watch",
                kind=MetaData.Type.BOOL,
                description="Watch script for changes, and rerun",
                default=False,
            )
        )
        self.baseType = 'GenericRoleConfiguration'
        self.childType = 'GenericRoleGeneratedConfiguration'
        self.service_type = self.baseType
        self.allTypes = ['GenericRoleGeneratedConfiguration', 'GenericRoleConfiguration']
        self.top_level = False
        self.leaf_entity = True

