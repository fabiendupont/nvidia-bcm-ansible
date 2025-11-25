from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducer import MonitoringDataProducer


class MonitoringDataProducerPRS(MonitoringDataProducer):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="maxSampleAge",
                kind=MetaData.Type.FLOAT,
                description="Maximal age of node sample to contribute",
                default=300.0,
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerPRS'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerPRS', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

