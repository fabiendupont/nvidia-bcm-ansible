from pythoncm.entity.metadata.monitoringserviceaction import MonitoringServiceAction


class MonitoringServiceStopAction(MonitoringServiceAction):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringAction'
        self.childType = 'MonitoringServiceStopAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringServiceStopAction', 'MonitoringServiceAction', 'MonitoringAction']
        self.top_level = True
        self.leaf_entity = True

