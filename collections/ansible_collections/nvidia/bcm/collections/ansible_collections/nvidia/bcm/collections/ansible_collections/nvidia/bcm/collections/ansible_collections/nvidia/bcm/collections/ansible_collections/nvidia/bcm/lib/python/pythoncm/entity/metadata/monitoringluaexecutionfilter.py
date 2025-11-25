from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringexecutionfilter import MonitoringExecutionFilter


class MonitoringLuaExecutionFilter(MonitoringExecutionFilter):
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
        self.baseType = 'MonitoringExecutionFilter'
        self.childType = 'MonitoringLuaExecutionFilter'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringLuaExecutionFilter', 'MonitoringExecutionFilter']
        self.top_level = False
        self.leaf_entity = True

