from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class DiskVolume(Entity):
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
                name="size",
                kind=MetaData.Type.STRING,
                description="Size",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mountpoint",
                kind=MetaData.Type.STRING,
                description="Mount point",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mountoptions",
                kind=MetaData.Type.STRING,
                description="Mount options",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="filesystem",
                kind=MetaData.Type.STRING,
                description="Filesystem",
                default='',
            )
        )
        self.baseType = 'DiskVolume'
        self.service_type = self.baseType
        self.allTypes = ['DiskVolume']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

