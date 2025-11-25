from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringHealthOverview(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_entity_uuid",
                kind=MetaData.Type.UUID,
                description="Entity",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="alertLevelMaximum",
                kind=MetaData.Type.UINT,
                description="Maximal severity of all failed triggers",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="alertLevelSum",
                kind=MetaData.Type.UINT,
                description="Total severity of all failed triggers",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="alertLevelCount",
                kind=MetaData.Type.UINT,
                description="Total count of all failed triggers",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="timestamp",
                kind=MetaData.Type.UINT,
                description="Timestamp of data",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="info",
                kind=MetaData.Type.STRING,
                description="Info",
                default='',
            )
        )
        self.baseType = 'MonitoringHealthOverview'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringHealthOverview']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

