from pythoncm.entity.metadata.monitoringmeasurable import MonitoringMeasurable


class MonitoringMeasurableEnum(MonitoringMeasurable):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringMeasurable'
        self.childType = 'MonitoringMeasurableEnum'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringMeasurableEnum', 'MonitoringMeasurable']
        self.top_level = True
        self.leaf_entity = True

