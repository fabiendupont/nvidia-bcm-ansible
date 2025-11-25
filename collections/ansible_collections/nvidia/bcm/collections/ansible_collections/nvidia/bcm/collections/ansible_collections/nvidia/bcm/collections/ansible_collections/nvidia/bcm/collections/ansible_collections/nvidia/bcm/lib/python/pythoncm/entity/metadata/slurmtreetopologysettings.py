from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SlurmTreeTopologySettings(Entity):
    """
    Slurm Tree topology plugin settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="topologySwitches",
                kind=MetaData.Type.RESOLVE,
                description="List of switches that should be used to write the topology file",
                instance='Switch',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="topologyEphemeralSwitches",
                kind=MetaData.Type.BOOL,
                description="Add ephemeral switches to topology.conf",
                default=True,
            )
        )
        self.baseType = 'SlurmTreeTopologySettings'
        self.service_type = self.baseType
        self.allTypes = ['SlurmTreeTopologySettings']
        self.top_level = False
        self.leaf_entity = True

