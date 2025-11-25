from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringLabeledEntityCacheSubSystemInfo(Entity):
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
                description="Current cached size",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="added",
                kind=MetaData.Type.UINT,
                description="Total added entities",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="removed",
                kind=MetaData.Type.UINT,
                description="Total removed entities",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="changes",
                kind=MetaData.Type.UINT,
                description="Total number of changes",
                default=0,
            )
        )
        self.baseType = 'MonitoringLabeledEntityCacheSubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringLabeledEntityCacheSubSystemInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

