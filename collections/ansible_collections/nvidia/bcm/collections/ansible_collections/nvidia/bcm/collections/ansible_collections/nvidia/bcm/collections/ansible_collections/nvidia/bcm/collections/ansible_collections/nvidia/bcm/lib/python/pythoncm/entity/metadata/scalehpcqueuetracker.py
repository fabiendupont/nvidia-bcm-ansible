from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.scaletracker import ScaleTracker


class ScaleHpcQueueTracker(ScaleTracker):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="queue",
                kind=MetaData.Type.STRING,
                description="Tracking job queue",
                default='',
            )
        )
        self.baseType = 'ScaleTracker'
        self.childType = 'ScaleHpcQueueTracker'
        self.service_type = self.baseType
        self.allTypes = ['ScaleHpcQueueTracker', 'ScaleTracker']
        self.top_level = False
        self.leaf_entity = True

