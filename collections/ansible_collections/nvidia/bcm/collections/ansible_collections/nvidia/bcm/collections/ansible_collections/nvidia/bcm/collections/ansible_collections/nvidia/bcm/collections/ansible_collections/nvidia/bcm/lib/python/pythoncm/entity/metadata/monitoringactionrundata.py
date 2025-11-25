from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringActionRunData(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="target",
                kind=MetaData.Type.UUID,
                description="Target node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="info",
                kind=MetaData.Type.STRING,
                description="Extra information",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="env",
                kind=MetaData.Type.STRING,
                description="Environment",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'MonitoringActionRunData'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringActionRunData']
        self.top_level = False
        self.leaf_entity = True

