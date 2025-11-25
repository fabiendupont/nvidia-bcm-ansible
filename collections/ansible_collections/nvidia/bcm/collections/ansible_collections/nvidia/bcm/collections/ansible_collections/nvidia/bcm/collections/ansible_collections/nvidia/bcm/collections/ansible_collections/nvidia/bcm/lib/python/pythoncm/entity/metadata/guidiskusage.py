from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiDiskUsage(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_device_uuid",
                kind=MetaData.Type.UUID,
                description="Device",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mountpoint",
                kind=MetaData.Type.STRING,
                description="Mountpoint",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="used",
                kind=MetaData.Type.UINT,
                description="Bytes in use on this device",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="free",
                kind=MetaData.Type.UINT,
                description="Bytes free on this device",
                default=0,
            )
        )
        self.baseType = 'GuiDiskUsage'
        self.service_type = self.baseType
        self.allTypes = ['GuiDiskUsage']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

