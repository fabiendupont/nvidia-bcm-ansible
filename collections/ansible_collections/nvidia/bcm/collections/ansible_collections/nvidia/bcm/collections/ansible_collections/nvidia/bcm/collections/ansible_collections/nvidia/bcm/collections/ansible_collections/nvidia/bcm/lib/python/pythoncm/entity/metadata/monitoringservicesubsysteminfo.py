from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringServiceSubSystemInfo(Entity):
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
                name="stopped",
                kind=MetaData.Type.BOOL,
                description="Stopped",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="suspended",
                kind=MetaData.Type.BOOL,
                description="Suspended",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="last",
                kind=MetaData.Type.UINT,
                description="Last sample time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="queued",
                kind=MetaData.Type.UINT,
                description="Queued items",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="handled",
                kind=MetaData.Type.UINT,
                description="Handled items",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cacheMiss",
                kind=MetaData.Type.UINT,
                description="Miss cached count",
                default=0,
            )
        )
        self.baseType = 'MonitoringServiceSubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringServiceSubSystemInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

