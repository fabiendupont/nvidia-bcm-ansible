from pythoncm.entity.metadata.monitoringaction import MonitoringAction


class MonitoringNVSMHealthDumpAction(MonitoringAction):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringAction'
        self.childType = 'MonitoringNVSMHealthDumpAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringNVSMHealthDumpAction', 'MonitoringAction']
        self.top_level = True
        self.leaf_entity = True

