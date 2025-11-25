from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringexecutionmultiplexer import MonitoringExecutionMultiplexer


class MonitoringOverlayListExecutionMultiplexer(MonitoringExecutionMultiplexer):
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
        self.baseType = 'MonitoringExecutionMultiplexer'
        self.childType = 'MonitoringOverlayListExecutionMultiplexer'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringOverlayListExecutionMultiplexer', 'MonitoringExecutionMultiplexer']
        self.top_level = False
        self.leaf_entity = True

