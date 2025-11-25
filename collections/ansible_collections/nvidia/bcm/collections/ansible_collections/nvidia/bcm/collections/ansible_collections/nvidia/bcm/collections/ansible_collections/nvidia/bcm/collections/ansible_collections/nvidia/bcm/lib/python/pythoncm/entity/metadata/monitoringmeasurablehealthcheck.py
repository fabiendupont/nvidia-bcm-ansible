from pythoncm.entity.metadata.monitoringmeasurable import MonitoringMeasurable


class MonitoringMeasurableHealthCheck(MonitoringMeasurable):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringMeasurable'
        self.childType = 'MonitoringMeasurableHealthCheck'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringMeasurableHealthCheck', 'MonitoringMeasurable']
        self.top_level = True
        self.leaf_entity = True

