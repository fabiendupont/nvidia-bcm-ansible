from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringexecutionfilter import MonitoringExecutionFilter


class MonitoringTypeExecutionFilter(MonitoringExecutionFilter):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="headNode",
                kind=MetaData.Type.BOOL,
                description="Head node",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="physicalNode",
                kind=MetaData.Type.BOOL,
                description="Physical node",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cloudNode",
                kind=MetaData.Type.BOOL,
                description="Cloud node",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="liteNode",
                kind=MetaData.Type.BOOL,
                description="Lite node",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dpuNode",
                kind=MetaData.Type.BOOL,
                description="DPU node",
                default=False,
            )
        )
        self.baseType = 'MonitoringExecutionFilter'
        self.childType = 'MonitoringTypeExecutionFilter'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringTypeExecutionFilter', 'MonitoringExecutionFilter']
        self.top_level = False
        self.leaf_entity = True

