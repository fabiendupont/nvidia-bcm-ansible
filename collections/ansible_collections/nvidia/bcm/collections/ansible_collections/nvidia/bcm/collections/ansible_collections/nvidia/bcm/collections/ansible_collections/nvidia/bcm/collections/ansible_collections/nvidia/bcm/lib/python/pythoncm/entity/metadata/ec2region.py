from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudregion import CloudRegion


class EC2Region(CloudRegion):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="url",
                kind=MetaData.Type.STRING,
                description="url",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="availabilityZones",
                kind=MetaData.Type.ENTITY,
                description="Availability zones",
                instance='EC2AvailabilityZone',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'CloudRegion'
        self.childType = 'EC2Region'
        self.service_type = self.baseType
        self.allTypes = ['EC2Region', 'CloudRegion']
        self.top_level = True
        self.leaf_entity = True

