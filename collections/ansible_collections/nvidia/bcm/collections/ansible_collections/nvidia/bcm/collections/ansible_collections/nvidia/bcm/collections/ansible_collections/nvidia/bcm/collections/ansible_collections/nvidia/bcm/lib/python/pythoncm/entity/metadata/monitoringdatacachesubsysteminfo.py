from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringDataCacheSubSystemInfo(Entity):
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
                kind=MetaData.Type.UINT,
                description="First plot request",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="updates",
                kind=MetaData.Type.UINT,
                description="Last plot request",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="requests",
                kind=MetaData.Type.UINT,
                description="Number of plot requests",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="lookup",
                kind=MetaData.Type.UINT,
                description="Size of the optimized lookup cache",
                default=0,
            )
        )
        self.baseType = 'MonitoringDataCacheSubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataCacheSubSystemInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

