from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class DiskVolumeGroup(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="extentSize",
                kind=MetaData.Type.STRING,
                description="Size",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="physicalVolumes",
                kind=MetaData.Type.STRING,
                description="Physical volumes",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="logicalVolumes",
                kind=MetaData.Type.ENTITY,
                description="Logical volumes",
                instance='DiskVolume',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'DiskVolumeGroup'
        self.service_type = self.baseType
        self.allTypes = ['DiskVolumeGroup']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

