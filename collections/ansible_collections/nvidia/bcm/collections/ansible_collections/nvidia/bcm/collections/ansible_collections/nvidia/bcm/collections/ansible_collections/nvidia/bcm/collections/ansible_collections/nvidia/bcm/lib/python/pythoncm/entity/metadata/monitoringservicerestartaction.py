from pythoncm.entity.metadata.monitoringserviceaction import MonitoringServiceAction


class MonitoringServiceRestartAction(MonitoringServiceAction):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringAction'
        self.childType = 'MonitoringServiceRestartAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringServiceRestartAction', 'MonitoringServiceAction', 'MonitoringAction']
        self.top_level = True
        self.leaf_entity = True

