from pythoncm.entity.metadata.monitoringpoweraction import MonitoringPowerAction


class MonitoringPowerResetAction(MonitoringPowerAction):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringAction'
        self.childType = 'MonitoringPowerResetAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringPowerResetAction', 'MonitoringPowerAction', 'MonitoringAction']
        self.top_level = True
        self.leaf_entity = True

