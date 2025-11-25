from pythoncm.entity.metadata.monitoringdataproducerinternal import MonitoringDataProducerInternal


class MonitoringDataProducerPowerDistributionUnit(MonitoringDataProducerInternal):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerPowerDistributionUnit'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerPowerDistributionUnit', 'MonitoringDataProducerInternal', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

