from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducer import MonitoringDataProducer


class MonitoringDataProducerLua(MonitoringDataProducer):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="code",
                kind=MetaData.Type.STRING,
                description="Lua code",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeout",
                kind=MetaData.Type.UINT,
                description="Lua timeout",
                default=5,
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerLua'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerLua', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

