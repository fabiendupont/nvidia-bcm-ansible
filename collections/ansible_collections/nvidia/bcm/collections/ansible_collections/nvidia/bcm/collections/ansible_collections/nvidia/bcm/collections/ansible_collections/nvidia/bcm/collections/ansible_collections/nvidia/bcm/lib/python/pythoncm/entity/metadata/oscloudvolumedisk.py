from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.osclouddisk import OSCloudDisk


class OSCloudVolumeDisk(OSCloudDisk):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="imageId",
                kind=MetaData.Type.STRING,
                description="Image ID to use as source for this disk",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="snapshotId",
                kind=MetaData.Type.STRING,
                description="Snapshot ID to use as source for this disk",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="volumeId",
                kind=MetaData.Type.STRING,
                description="Volume ID to use as source for this disk",
                default='',
            )
        )
        self.baseType = 'OSCloudDisk'
        self.childType = 'OSCloudVolumeDisk'
        self.service_type = self.baseType
        self.allTypes = ['OSCloudVolumeDisk', 'OSCloudDisk']
        self.top_level = False
        self.leaf_entity = True

