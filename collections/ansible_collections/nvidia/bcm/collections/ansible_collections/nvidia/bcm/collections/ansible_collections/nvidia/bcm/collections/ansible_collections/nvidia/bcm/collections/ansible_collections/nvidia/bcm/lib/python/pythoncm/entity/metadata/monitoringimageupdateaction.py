from pythoncm.entity.metadata.monitoringaction import MonitoringAction


class MonitoringImageUpdateAction(MonitoringAction):
    def __init__(self):
        super().__init__()
        self.baseType = 'MonitoringAction'
        self.childType = 'MonitoringImageUpdateAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringImageUpdateAction', 'MonitoringAction']
        self.top_level = True
        self.leaf_entity = True

