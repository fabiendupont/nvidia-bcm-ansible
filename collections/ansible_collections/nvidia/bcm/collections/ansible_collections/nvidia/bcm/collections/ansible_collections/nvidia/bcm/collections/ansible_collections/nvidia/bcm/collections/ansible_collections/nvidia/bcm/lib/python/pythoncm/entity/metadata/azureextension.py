from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class AzureExtension(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="User-defined name of the private cloud",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="location",
                kind=MetaData.Type.RESOLVE,
                description="Region of the cluster extension",
                instance='AzureLocation',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="resourceGroup",
                kind=MetaData.Type.STRING,
                description="Azure resource group name for all resources in the extension",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="network",
                kind=MetaData.Type.RESOLVE,
                description="Network associated with the extension",
                clone=False,
                instance='Network',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="extraField",
                kind=MetaData.Type.STRING,
                description="Reserved",
                clone=False,
                vector=True,
                default=[],
            )
        )
        self.baseType = 'AzureExtension'
        self.service_type = self.baseType
        self.allTypes = ['AzureExtension']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

