from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringJobExtraLabelCacheSubSystemInfo(Entity):
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
                name="skipped",
                kind=MetaData.Type.UINT,
                description="Total skipped entities",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="delayed",
                kind=MetaData.Type.UINT,
                description="Total delayed entities",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nothing",
                kind=MetaData.Type.UINT,
                description="Total entities for which nothing was done",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="enriched",
                kind=MetaData.Type.UINT,
                description="Total entities that were enriched",
                default=0,
            )
        )
        self.baseType = 'MonitoringJobExtraLabelCacheSubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringJobExtraLabelCacheSubSystemInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

