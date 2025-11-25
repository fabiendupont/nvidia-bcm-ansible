from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class AzureManagedDiskParameters(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="id",
                kind=MetaData.Type.STRING,
                description="Managed disks resource ID",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="storageAccountType",
                kind=MetaData.Type.STRING,
                description="Storage account type for managed disks",
                default="Standard_LRS",
            )
        )
        self.baseType = 'AzureManagedDiskParameters'
        self.service_type = self.baseType
        self.allTypes = ['AzureManagedDiskParameters']
        self.top_level = False
        self.leaf_entity = True

