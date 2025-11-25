from pythoncm.entity.metadata.monitoringdataproducersinglelinescript import MonitoringDataProducerSingleLineScript


class MonitoringDataProducerSingleLineHealthCheckScript(MonitoringDataProducerSingleLineScript):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerSingleLineHealthCheckScript'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerSingleLineHealthCheckScript', 'MonitoringDataProducerSingleLineScript', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

