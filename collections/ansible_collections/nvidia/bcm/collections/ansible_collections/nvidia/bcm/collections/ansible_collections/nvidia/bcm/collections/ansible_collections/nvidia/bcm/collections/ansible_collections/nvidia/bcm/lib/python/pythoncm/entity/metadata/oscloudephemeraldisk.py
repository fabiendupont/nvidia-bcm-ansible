from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.osclouddisk import OSCloudDisk


class OSCloudEphemeralDisk(OSCloudDisk):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="format",
                kind=MetaData.Type.STRING,
                description="Filesystem to format the disk",
                default='',
            )
        )
        self.baseType = 'OSCloudDisk'
        self.childType = 'OSCloudEphemeralDisk'
        self.service_type = self.baseType
        self.allTypes = ['OSCloudEphemeralDisk', 'OSCloudDisk']
        self.top_level = False
        self.leaf_entity = True

