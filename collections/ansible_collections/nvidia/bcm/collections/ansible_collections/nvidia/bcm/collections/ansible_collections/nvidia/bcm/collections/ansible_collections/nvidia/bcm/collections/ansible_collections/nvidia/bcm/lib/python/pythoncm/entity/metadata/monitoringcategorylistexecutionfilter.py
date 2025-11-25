from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringexecutionfilter import MonitoringExecutionFilter


class MonitoringCategoryListExecutionFilter(MonitoringExecutionFilter):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="categories",
                kind=MetaData.Type.RESOLVE,
                description="List of categories belonging to this group",
                instance='Category',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'MonitoringExecutionFilter'
        self.childType = 'MonitoringCategoryListExecutionFilter'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringCategoryListExecutionFilter', 'MonitoringExecutionFilter']
        self.top_level = False
        self.leaf_entity = True

