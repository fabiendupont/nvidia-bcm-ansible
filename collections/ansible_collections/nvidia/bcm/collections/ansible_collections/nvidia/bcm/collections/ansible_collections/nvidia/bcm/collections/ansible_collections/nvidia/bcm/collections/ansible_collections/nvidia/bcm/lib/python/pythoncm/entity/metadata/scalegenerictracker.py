from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.scaletracker import ScaleTracker


class ScaleGenericTracker(ScaleTracker):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="handler",
                kind=MetaData.Type.STRING,
                description="Full path to python module that produces workload entities for cm-scale",
                default='',
            )
        )
        self.baseType = 'ScaleTracker'
        self.childType = 'ScaleGenericTracker'
        self.service_type = self.baseType
        self.allTypes = ['ScaleGenericTracker', 'ScaleTracker']
        self.top_level = False
        self.leaf_entity = True

