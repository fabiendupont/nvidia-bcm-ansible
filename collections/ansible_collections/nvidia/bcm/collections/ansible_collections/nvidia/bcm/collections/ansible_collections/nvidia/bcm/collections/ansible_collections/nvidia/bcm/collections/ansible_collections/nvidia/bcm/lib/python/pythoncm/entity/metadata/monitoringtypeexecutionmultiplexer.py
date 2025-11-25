from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringexecutionmultiplexer import MonitoringExecutionMultiplexer


class MonitoringTypeExecutionMultiplexer(MonitoringExecutionMultiplexer):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="types",
                kind=MetaData.Type.STRING,
                description="Types",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'MonitoringExecutionMultiplexer'
        self.childType = 'MonitoringTypeExecutionMultiplexer'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringTypeExecutionMultiplexer', 'MonitoringExecutionMultiplexer']
        self.top_level = False
        self.leaf_entity = True

