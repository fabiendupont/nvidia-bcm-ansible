from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.azuredisk import AzureDisk


class AzureOSDisk(AzureDisk):
    class AzureOSDiskCachingType(Enum):
        Disabled = auto()
        ReadOnly = auto()
        ReadWrite = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="cachingType",
                kind=MetaData.Type.ENUM,
                description="Disk caching type",
                options=[
                    self.AzureOSDiskCachingType.Disabled,
                    self.AzureOSDiskCachingType.ReadOnly,
                    self.AzureOSDiskCachingType.ReadWrite,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.AzureOSDiskCachingType,
                default=self.AzureOSDiskCachingType.Disabled,
            )
        )
        self.baseType = 'AzureDisk'
        self.childType = 'AzureOSDisk'
        self.service_type = self.baseType
        self.allTypes = ['AzureOSDisk', 'AzureDisk']
        self.top_level = False
        self.leaf_entity = True

