from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.jobqueuestat import JobQueueStat


class SlurmJobQueueStat(JobQueueStat):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="memory",
                kind=MetaData.Type.STRING,
                description="Memory",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="cpus",
                kind=MetaData.Type.UINT,
                description="CPUs",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="total",
                kind=MetaData.Type.UINT,
                description="Total nodes",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usable",
                kind=MetaData.Type.UINT,
                description="Usable nodes",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="free",
                kind=MetaData.Type.UINT,
                description="Free nodes",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeLimit",
                kind=MetaData.Type.UINT,
                description="Node limit",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeLimit",
                kind=MetaData.Type.STRING,
                description="Time limit",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="other",
                kind=MetaData.Type.STRING,
                description="Other traits",
                readonly=True,
                default='',
            )
        )
        self.baseType = 'JobQueueStat'
        self.childType = 'SlurmJobQueueStat'
        self.service_type = self.baseType
        self.allTypes = ['SlurmJobQueueStat', 'JobQueueStat']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

