from pythoncm.entity.metadata.monitoringaction import MonitoringAction


class MonitoringPowerAction(MonitoringAction):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringAction'
        self.childType = 'MonitoringPowerAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringPowerAction', 'MonitoringAction']
        self.leaf_entity = False

