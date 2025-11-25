from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudtype import CloudType


class AzureVMSize(CloudType):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="hyperVGenerations",
                kind=MetaData.Type.STRING,
                description="Supported Hyper-V generations.",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'CloudType'
        self.childType = 'AzureVMSize'
        self.service_type = self.baseType
        self.allTypes = ['AzureVMSize', 'CloudType']
        self.top_level = True
        self.leaf_entity = True
        self.allow_commit = False

