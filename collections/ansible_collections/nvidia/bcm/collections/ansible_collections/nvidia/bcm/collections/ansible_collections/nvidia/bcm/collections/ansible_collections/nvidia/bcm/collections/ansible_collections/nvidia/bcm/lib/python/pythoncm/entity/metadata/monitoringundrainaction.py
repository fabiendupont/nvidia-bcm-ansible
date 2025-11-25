from pythoncm.entity.metadata.monitoringaction import MonitoringAction


class MonitoringUndrainAction(MonitoringAction):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringAction'
        self.childType = 'MonitoringUndrainAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringUndrainAction', 'MonitoringAction']
        self.top_level = True
        self.leaf_entity = True

