from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringexecutionmultiplexer import MonitoringExecutionMultiplexer


class MonitoringDynamicExecutionMultiplexer(MonitoringExecutionMultiplexer):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="local",
                kind=MetaData.Type.BOOL,
                description="Run on the local node",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="host",
                kind=MetaData.Type.BOOL,
                description="Run on the host node of a DPU",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="offload",
                kind=MetaData.Type.BOOL,
                description="Run on the nodes offloaded onto this node",
                default=False,
            )
        )
        self.baseType = 'MonitoringExecutionMultiplexer'
        self.childType = 'MonitoringDynamicExecutionMultiplexer'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDynamicExecutionMultiplexer', 'MonitoringExecutionMultiplexer']
        self.top_level = False
        self.leaf_entity = True

