from pythoncm.entity.metadata.monitoringdataproducerinternal import MonitoringDataProducerInternal


class MonitoringDataProducerRedFishSubscription(MonitoringDataProducerInternal):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerRedFishSubscription'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerRedFishSubscription', 'MonitoringDataProducerInternal', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

