from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringexecutionfilter import MonitoringExecutionFilter


class MonitoringNodeListExecutionFilter(MonitoringExecutionFilter):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.RESOLVE,
                description="List of nodes belonging to this group",
                instance='Node',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'MonitoringExecutionFilter'
        self.childType = 'MonitoringNodeListExecutionFilter'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringNodeListExecutionFilter', 'MonitoringExecutionFilter']
        self.top_level = False
        self.leaf_entity = True

