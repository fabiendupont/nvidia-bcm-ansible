from pythoncm.entity.metadata.monitoringpoweraction import MonitoringPowerAction


class MonitoringPowerOnAction(MonitoringPowerAction):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringAction'
        self.childType = 'MonitoringPowerOnAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringPowerOnAction', 'MonitoringPowerAction', 'MonitoringAction']
        self.top_level = True
        self.leaf_entity = True

