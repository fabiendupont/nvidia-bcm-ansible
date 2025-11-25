from pythoncm.entity.metadata.monitoringdataproducer import MonitoringDataProducer


class MonitoringDataProducerInternal(MonitoringDataProducer):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerInternal'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerInternal', 'MonitoringDataProducer']
        self.leaf_entity = False

