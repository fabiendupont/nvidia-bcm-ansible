from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringexecutionmultiplexer import MonitoringExecutionMultiplexer


class MonitoringLuaExecutionMultiplexer(MonitoringExecutionMultiplexer):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="code",
                kind=MetaData.Type.STRING,
                description="Lua code",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="notes",
                kind=MetaData.Type.STRING,
                description="Notes",
                default='',
            )
        )
        self.baseType = 'MonitoringExecutionMultiplexer'
        self.childType = 'MonitoringLuaExecutionMultiplexer'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringLuaExecutionMultiplexer', 'MonitoringExecutionMultiplexer']
        self.top_level = False
        self.leaf_entity = True

