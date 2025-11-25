from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.lsfbasejobqueue import LSFBaseJobQueue


class LSFJobQueue(LSFBaseJobQueue):
    """
    LSF job queues
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="fairshare",
                kind=MetaData.Type.STRING,
                description="Fairshare scheduling",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="backfill",
                kind=MetaData.Type.STRING,
                description="Backfill scheduling",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="preemption",
                kind=MetaData.Type.STRING,
                description="Preemption scheduling",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultQueue",
                kind=MetaData.Type.BOOL,
                description="Specifies the queue which is to accept jobs when no queue is requested",
                clone=False,
                default=False,
            )
        )
        self.baseType = 'JobQueue'
        self.childType = 'LSFJobQueue'
        self.service_type = self.baseType
        self.allTypes = ['LSFJobQueue', 'LSFBaseJobQueue', 'JobQueue']
        self.top_level = True
        self.leaf_entity = True

