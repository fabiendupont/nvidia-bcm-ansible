from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.jobqueuestat import JobQueueStat


class PBSJobQueueStat(JobQueueStat):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="held",
                kind=MetaData.Type.UINT,
                description="Held jobs",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="waiting",
                kind=MetaData.Type.UINT,
                description="Waiting jobs",
                readonly=True,
                default=0,
            )
        )
        self.baseType = 'JobQueueStat'
        self.childType = 'PBSJobQueueStat'
        self.service_type = self.baseType
        self.allTypes = ['PBSJobQueueStat', 'JobQueueStat']
        self.leaf_entity = False
        self.add_to_cluster = False
        self.allow_commit = False

