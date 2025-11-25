from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.azuredisk import AzureDisk


class AzureDataDisk(AzureDisk):
    """
    Additional disk that can be attached to an azure instance during boot
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="lun",
                kind=MetaData.Type.UINT,
                description="Logical unit number of a block device to be attached",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="removeOnTermination",
                kind=MetaData.Type.BOOL,
                description="If true, the drive will be removed when the instance it is atteched to gets terminated",
                default=True,
            )
        )
        self.baseType = 'AzureDisk'
        self.childType = 'AzureDataDisk'
        self.service_type = self.baseType
        self.allTypes = ['AzureDataDisk', 'AzureDisk']
        self.top_level = False
        self.leaf_entity = True

