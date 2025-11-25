from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PbsProCommSettings(Entity):
    """
    PBS pro pbs_comm settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="commRouters",
                kind=MetaData.Type.STRING,
                description="Tells a pbs_comm where to find its fellow communication daemons (PBS_COMM_ROUTERS parameter in pbs.conf)",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="commThreads",
                kind=MetaData.Type.UINT,
                description="Tells pbs_comm how many threads to start (PBS_COMM_THREADS parameter in pbs.conf)",
                default=4,
            )
        )
        self.meta.add(
            MetaDataField(
                name="startComm",
                kind=MetaData.Type.BOOL,
                description="Configure pbs_com daemon start (PBS_START_COMM parameter in pbs.conf)",
                default=False,
            )
        )
        self.baseType = 'PbsProCommSettings'
        self.service_type = self.baseType
        self.allTypes = ['PbsProCommSettings']
        self.top_level = False
        self.leaf_entity = True

