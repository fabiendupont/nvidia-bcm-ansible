from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringCacheSubSystemInfo(Entity):
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
                name="queued",
                kind=MetaData.Type.UINT,
                description="Number of samples ready for delivery",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pickup",
                kind=MetaData.Type.UINT,
                description="Number of times data has been picked up",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="delivered",
                kind=MetaData.Type.UINT,
                description="Number of samples delivered the last pick up",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="handled",
                kind=MetaData.Type.UINT,
                description="Total number of samples handled",
                default=0,
            )
        )
        self.baseType = 'MonitoringCacheSubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringCacheSubSystemInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

