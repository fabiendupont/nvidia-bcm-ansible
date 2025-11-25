from pythoncm.entity.metadata.monitoringdataproducer import MonitoringDataProducer


class MonitoringDataProducerCPU(MonitoringDataProducer):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerCPU'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerCPU', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

