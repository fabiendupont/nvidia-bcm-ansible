from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudtype import CloudType


class ForgeInstanceType(CloudType):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="id",
                kind=MetaData.Type.STRING,
                description="The ID of the instance type",
                default='',
            )
        )
        self.baseType = 'CloudType'
        self.childType = 'ForgeInstanceType'
        self.service_type = self.baseType
        self.allTypes = ['ForgeInstanceType', 'CloudType']
        self.top_level = True
        self.leaf_entity = True
        self.allow_commit = False

