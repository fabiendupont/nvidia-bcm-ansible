from pythoncm.entity.metadata.monitoringdataproducerinternal import MonitoringDataProducerInternal


class MonitoringDataProducerAlertLevel(MonitoringDataProducerInternal):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerAlertLevel'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerAlertLevel', 'MonitoringDataProducerInternal', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

