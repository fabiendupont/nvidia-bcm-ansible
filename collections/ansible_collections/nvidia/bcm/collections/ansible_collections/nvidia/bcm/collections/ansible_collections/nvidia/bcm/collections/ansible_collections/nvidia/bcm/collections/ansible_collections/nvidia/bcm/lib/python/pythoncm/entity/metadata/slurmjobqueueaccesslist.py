from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SlurmJobQueueAccessList(Entity):
    """
    Slurm job queue access list
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="wlmCluster",
                kind=MetaData.Type.RESOLVE,
                description="WLM cluster link to this job queue access list",
                instance='WlmCluster',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="slurmJobQueue",
                kind=MetaData.Type.RESOLVE,
                description="List of queues that can be submitted to. If none is specified, this access list will submit to all job queues in the specified WlmCluster.",
                instance='SlurmJobQueue',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'SlurmJobQueueAccessList'
        self.service_type = self.baseType
        self.allTypes = ['SlurmJobQueueAccessList']
        self.top_level = False
        self.leaf_entity = True

