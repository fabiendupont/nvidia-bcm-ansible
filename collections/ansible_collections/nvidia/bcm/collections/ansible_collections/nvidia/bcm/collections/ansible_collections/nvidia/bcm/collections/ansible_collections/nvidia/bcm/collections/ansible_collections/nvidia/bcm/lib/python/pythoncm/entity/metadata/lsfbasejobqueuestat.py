from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.jobqueuestat import JobQueueStat


class LSFBaseJobQueueStat(JobQueueStat):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="status",
                kind=MetaData.Type.STRING,
                description="Queue status",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="priority",
                kind=MetaData.Type.UINT,
                description="Queue priority",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="njobs",
                kind=MetaData.Type.UINT,
                description="Number of all jobs in queue",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="suspended",
                kind=MetaData.Type.UINT,
                description="Number of suspended jobs in queue",
                readonly=True,
                default=0,
            )
        )
        self.baseType = 'JobQueueStat'
        self.childType = 'LSFBaseJobQueueStat'
        self.service_type = self.baseType
        self.allTypes = ['LSFBaseJobQueueStat', 'JobQueueStat']
        self.leaf_entity = False
        self.add_to_cluster = False
        self.allow_commit = False

