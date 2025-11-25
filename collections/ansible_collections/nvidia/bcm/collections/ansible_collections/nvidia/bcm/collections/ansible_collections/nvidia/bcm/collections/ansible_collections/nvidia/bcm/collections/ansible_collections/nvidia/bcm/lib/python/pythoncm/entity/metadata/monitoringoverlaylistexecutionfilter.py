from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringexecutionfilter import MonitoringExecutionFilter


class MonitoringOverlayListExecutionFilter(MonitoringExecutionFilter):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="overlays",
                kind=MetaData.Type.RESOLVE,
                description="List of overlays belonging to this group",
                instance='ConfigurationOverlay',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'MonitoringExecutionFilter'
        self.childType = 'MonitoringOverlayListExecutionFilter'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringOverlayListExecutionFilter', 'MonitoringExecutionFilter']
        self.top_level = False
        self.leaf_entity = True

