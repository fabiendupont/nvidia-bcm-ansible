from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class AzureDisk(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name of the data disk",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="size",
                kind=MetaData.Type.UINT,
                description="Size of the drive",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="image",
                kind=MetaData.Type.STRING,
                description="URL to a source image for the disk",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="storageAccountName",
                kind=MetaData.Type.STRING,
                description="Name of a storage account to hold the disk",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="imageContainerName",
                kind=MetaData.Type.STRING,
                description="If the disk has the image url set, the image will be copied to a container with this name",
                default="images",
            )
        )
        self.meta.add(
            MetaDataField(
                name="containerName",
                kind=MetaData.Type.STRING,
                description="Name of a container in storage account to hold the disk",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="managedDiskParameters",
                kind=MetaData.Type.ENTITY,
                description="Azure Managed Disk parameters",
                instance='AzureManagedDiskParameters',
                init_instance='AzureManagedDiskParameters',
                create_instance=True,
                default=None,
            )
        )
        self.baseType = 'AzureDisk'
        self.service_type = self.baseType
        self.allTypes = ['AzureDisk']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

