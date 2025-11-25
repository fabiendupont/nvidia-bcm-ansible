from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudtype import CloudType


class OSCloudFlavor(CloudType):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="id",
                kind=MetaData.Type.STRING,
                description="The ID of the flavor",
                default='',
            )
        )
        self.baseType = 'CloudType'
        self.childType = 'OSCloudFlavor'
        self.service_type = self.baseType
        self.allTypes = ['OSCloudFlavor', 'CloudType']
        self.top_level = True
        self.leaf_entity = True
        self.allow_commit = False

