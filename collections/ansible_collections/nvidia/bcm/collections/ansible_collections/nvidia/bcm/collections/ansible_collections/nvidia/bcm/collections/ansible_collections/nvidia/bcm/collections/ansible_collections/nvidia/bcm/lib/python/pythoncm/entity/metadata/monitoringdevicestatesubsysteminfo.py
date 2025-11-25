from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringDeviceStateSubSystemInfo(Entity):
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
                name="up",
                kind=MetaData.Type.UINT,
                description="Number of up devices",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="down",
                kind=MetaData.Type.UINT,
                description="Number of down devices",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="closed",
                kind=MetaData.Type.UINT,
                description="Number of closed devices",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="muted",
                kind=MetaData.Type.UINT,
                description="Number of muted devices",
                default=0,
            )
        )
        self.baseType = 'MonitoringDeviceStateSubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDeviceStateSubSystemInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

