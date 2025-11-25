from pythoncm.entity.metadata.monitoringdataproducerinternal import MonitoringDataProducerInternal


class MonitoringDataProducerSysInfo(MonitoringDataProducerInternal):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerSysInfo'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerSysInfo', 'MonitoringDataProducerInternal', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

