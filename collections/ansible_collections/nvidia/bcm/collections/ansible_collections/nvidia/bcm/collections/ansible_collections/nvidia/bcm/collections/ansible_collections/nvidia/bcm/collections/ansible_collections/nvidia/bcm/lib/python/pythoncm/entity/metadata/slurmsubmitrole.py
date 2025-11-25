from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.wlmsubmitrole import WlmSubmitRole


class SlurmSubmitRole(WlmSubmitRole):
    """
    Slurm submit role
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="slurmJobQueueAcccessList",
                kind=MetaData.Type.ENTITY,
                description="List of slurm clusters and their associated queues that can be submitted to",
                instance='SlurmJobQueueAccessList',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'SlurmSubmitRole'
        self.service_type = self.baseType
        self.allTypes = ['SlurmSubmitRole', 'WlmSubmitRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

