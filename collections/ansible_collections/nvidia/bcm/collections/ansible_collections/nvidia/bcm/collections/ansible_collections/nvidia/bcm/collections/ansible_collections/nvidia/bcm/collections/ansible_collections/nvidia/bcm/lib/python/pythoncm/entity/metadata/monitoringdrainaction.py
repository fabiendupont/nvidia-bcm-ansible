from pythoncm.entity.metadata.monitoringaction import MonitoringAction


class MonitoringDrainAction(MonitoringAction):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringAction'
        self.childType = 'MonitoringDrainAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDrainAction', 'MonitoringAction']
        self.top_level = True
        self.leaf_entity = True

