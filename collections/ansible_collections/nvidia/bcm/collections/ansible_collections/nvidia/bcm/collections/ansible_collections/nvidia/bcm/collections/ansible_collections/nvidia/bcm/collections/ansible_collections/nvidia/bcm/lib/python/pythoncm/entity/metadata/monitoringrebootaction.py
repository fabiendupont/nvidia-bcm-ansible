from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringaction import MonitoringAction


class MonitoringRebootAction(MonitoringAction):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="runPreHaltOperations",
                kind=MetaData.Type.BOOL,
                description="Run pre-halt operations",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="preHaltOperationTimeout",
                kind=MetaData.Type.UINT,
                description="Run pre-halt operation timeout",
                default=300,
            )
        )
        self.baseType = 'MonitoringAction'
        self.childType = 'MonitoringRebootAction'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringRebootAction', 'MonitoringAction']
        self.top_level = True
        self.leaf_entity = True

