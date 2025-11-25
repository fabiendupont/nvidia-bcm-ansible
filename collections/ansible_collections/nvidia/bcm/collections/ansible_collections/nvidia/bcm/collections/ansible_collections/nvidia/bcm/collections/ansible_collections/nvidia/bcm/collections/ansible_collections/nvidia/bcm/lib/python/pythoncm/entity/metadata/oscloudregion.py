from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudregion import CloudRegion


class OSCloudRegion(CloudRegion):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="id",
                kind=MetaData.Type.STRING,
                description="The ID of the region",
                default='',
            )
        )
        self.baseType = 'CloudRegion'
        self.childType = 'OSCloudRegion'
        self.service_type = self.baseType
        self.allTypes = ['OSCloudRegion', 'CloudRegion']
        self.top_level = True
        self.leaf_entity = True

