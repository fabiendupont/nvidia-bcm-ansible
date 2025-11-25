from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringexecutionmultiplexer import MonitoringExecutionMultiplexer


class MonitoringCategoryListExecutionMultiplexer(MonitoringExecutionMultiplexer):
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
        self.baseType = 'MonitoringExecutionMultiplexer'
        self.childType = 'MonitoringCategoryListExecutionMultiplexer'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringCategoryListExecutionMultiplexer', 'MonitoringExecutionMultiplexer']
        self.top_level = False
        self.leaf_entity = True

