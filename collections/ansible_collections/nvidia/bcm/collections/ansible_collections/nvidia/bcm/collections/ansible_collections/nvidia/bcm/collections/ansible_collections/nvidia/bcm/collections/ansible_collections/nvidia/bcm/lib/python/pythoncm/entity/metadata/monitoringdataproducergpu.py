from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducer import MonitoringDataProducer


class MonitoringDataProducerGPU(MonitoringDataProducer):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="updateFreq",
                kind=MetaData.Type.FLOAT,
                description="Update frequency of the internal cuda metric sampler",
                default=10,
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerGPU'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerGPU', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

