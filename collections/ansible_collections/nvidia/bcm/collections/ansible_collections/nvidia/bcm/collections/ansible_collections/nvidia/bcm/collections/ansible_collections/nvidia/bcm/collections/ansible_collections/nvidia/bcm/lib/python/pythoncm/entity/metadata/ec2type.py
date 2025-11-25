from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudtype import CloudType


class EC2Type(CloudType):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="virtualizationType",
                kind=MetaData.Type.STRING,
                description="Virtualization type.",
                default='',
            )
        )
        self.baseType = 'CloudType'
        self.childType = 'EC2Type'
        self.service_type = self.baseType
        self.allTypes = ['EC2Type', 'CloudType']
        self.top_level = True
        self.leaf_entity = True
        self.allow_commit = False

