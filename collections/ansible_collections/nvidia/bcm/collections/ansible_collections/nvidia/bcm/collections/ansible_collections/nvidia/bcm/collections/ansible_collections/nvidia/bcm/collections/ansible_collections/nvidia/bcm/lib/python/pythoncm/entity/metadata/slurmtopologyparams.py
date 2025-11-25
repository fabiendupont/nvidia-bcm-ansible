from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SlurmTopologyParams(Entity):
    """
    Slurm Topology plugins parameters (TopologyParam value of slurm.conf)
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="dragonfly",
                kind=MetaData.Type.BOOL,
                description="Enable allocation optimization for Dragonfly network (TopologyParam=Dragonfly)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="routePart",
                kind=MetaData.Type.BOOL,
                description="Instead  of using the plugin's default route calculation, use partition node lists to route communications from the controller (TopologyParam=RoutePart)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="switchAsNodeRank",
                kind=MetaData.Type.BOOL,
                description="Assign  the  same  node  rank  to  all nodes under one leaf switch (TopologyParam=SwitchAsNodeRank)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="routeTree",
                kind=MetaData.Type.BOOL,
                description="Use the switch hierarchy defined in a topology.conf file for routing instead of just scheduling (TopologyParam=RouteTree)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="topoOptional",
                kind=MetaData.Type.BOOL,
                description="Only optimize allocation for network topology if the job includes a switch option (TopologyParam=TopoOptional)",
                default=False,
            )
        )
        self.baseType = 'SlurmTopologyParams'
        self.service_type = self.baseType
        self.allTypes = ['SlurmTopologyParams']
        self.top_level = False
        self.leaf_entity = True

