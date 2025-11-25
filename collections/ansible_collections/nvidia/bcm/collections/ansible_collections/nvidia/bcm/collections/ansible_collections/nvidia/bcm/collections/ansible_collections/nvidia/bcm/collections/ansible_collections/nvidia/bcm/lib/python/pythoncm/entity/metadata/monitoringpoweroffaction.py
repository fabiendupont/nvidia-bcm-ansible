from pythoncm.entity.metadata.monitoringpoweraction import MonitoringPowerAction


class MonitoringPowerOffAction(MonitoringPowerAction):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringAction'
        self.childType = 'MonitoringPowerOffAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringPowerOffAction', 'MonitoringPowerAction', 'MonitoringAction']
        self.top_level = True
        self.leaf_entity = True

