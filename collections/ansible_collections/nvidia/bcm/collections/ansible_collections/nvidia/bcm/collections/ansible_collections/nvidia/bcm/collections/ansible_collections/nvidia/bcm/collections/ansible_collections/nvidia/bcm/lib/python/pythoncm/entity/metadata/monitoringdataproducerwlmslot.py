from pythoncm.entity.metadata.monitoringdataproducer import MonitoringDataProducer


class MonitoringDataProducerWlmSlot(MonitoringDataProducer):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerWlmSlot'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerWlmSlot', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

