from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringDataProducerDPUSettingsEvent(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="index",
                kind=MetaData.Type.UINT,
                description="Index",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="counter",
                kind=MetaData.Type.UINT,
                description="Counter",
                default=0,
            )
        )
        self.baseType = 'MonitoringDataProducerDPUSettingsEvent'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerDPUSettingsEvent']
        self.leaf_entity = False

