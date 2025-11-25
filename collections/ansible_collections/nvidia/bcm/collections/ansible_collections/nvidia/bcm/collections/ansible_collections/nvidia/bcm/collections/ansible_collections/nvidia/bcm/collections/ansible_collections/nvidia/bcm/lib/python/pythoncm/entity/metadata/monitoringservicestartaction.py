from pythoncm.entity.metadata.monitoringserviceaction import MonitoringServiceAction


class MonitoringServiceStartAction(MonitoringServiceAction):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringAction'
        self.childType = 'MonitoringServiceStartAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringServiceStartAction', 'MonitoringServiceAction', 'MonitoringAction']
        self.top_level = True
        self.leaf_entity = True

