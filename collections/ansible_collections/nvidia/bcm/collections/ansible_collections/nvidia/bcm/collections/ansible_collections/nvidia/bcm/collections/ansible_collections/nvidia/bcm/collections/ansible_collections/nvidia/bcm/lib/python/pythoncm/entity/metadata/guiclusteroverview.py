from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiClusterOverview(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_partition_uuid",
                kind=MetaData.Type.UUID,
                description="Partition",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="information",
                kind=MetaData.Type.STRING,
                description="Short text describing cluster information",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="uptime",
                kind=MetaData.Type.UINT,
                description="Uptime of the active head node",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="phaseLoad",
                kind=MetaData.Type.FLOAT,
                description="Phase load accross all PDUs",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalInletActive",
                kind=MetaData.Type.FLOAT,
                description="Total inlet active current accross all APCs",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalPowerShelfInputCurrent",
                kind=MetaData.Type.FLOAT,
                description="Total input current over all power shelves",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodesUp",
                kind=MetaData.Type.UINT,
                description="Number of nodes that are listed as up",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodesDown",
                kind=MetaData.Type.UINT,
                description="Number of nodes that are listed as down",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodesClosed",
                kind=MetaData.Type.UINT,
                description="Number of nodes that are listed as closed",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodesTotal",
                kind=MetaData.Type.UINT,
                description="Number of nodes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="liteNodesUp",
                kind=MetaData.Type.UINT,
                description="Number of lite nodes that are listed as up",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="liteNodesDown",
                kind=MetaData.Type.UINT,
                description="Number of lite nodes that are listed as down",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="liteNodesClosed",
                kind=MetaData.Type.UINT,
                description="Number of lite nodes that are listed as closed",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="liteNodesTotal",
                kind=MetaData.Type.UINT,
                description="Number of lite nodes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dpuNodesUp",
                kind=MetaData.Type.UINT,
                description="Number of DPU nodes that are listed as up",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dpuNodesDown",
                kind=MetaData.Type.UINT,
                description="Number of DPU nodes that are listed as down",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dpuNodesClosed",
                kind=MetaData.Type.UINT,
                description="Number of DPU nodes that are listed as closed",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dpuNodesTotal",
                kind=MetaData.Type.UINT,
                description="Number of DPU nodes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="managedSwitchesUp",
                kind=MetaData.Type.UINT,
                description="Number of managed switches that are listed as up",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="managedSwitchesDown",
                kind=MetaData.Type.UINT,
                description="Number of managed switches that are listed as down",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="managedSwitchesClosed",
                kind=MetaData.Type.UINT,
                description="Number of managed switches that are listed as closed",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="managedSwitchesTotal",
                kind=MetaData.Type.UINT,
                description="Number of managed switches",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="devicesUp",
                kind=MetaData.Type.UINT,
                description="Number of non-node devices that are listed as up",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="devicesDown",
                kind=MetaData.Type.UINT,
                description="Number of non-node devices that are listed as down",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="devicesClosed",
                kind=MetaData.Type.UINT,
                description="Number of non-node devices that are listed as closed",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="devicesTotal",
                kind=MetaData.Type.UINT,
                description="Number of non-node devices",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="coresUp",
                kind=MetaData.Type.UINT,
                description="Sum of all cores for nodes which are up",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="coresDown",
                kind=MetaData.Type.UINT,
                description="Sum of all cores for nodes which are down",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="coresTotal",
                kind=MetaData.Type.UINT,
                description="Sum of all cores for nodes which are up at one time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gpusUp",
                kind=MetaData.Type.UINT,
                description="Sum of all GPUs for nodes which are up",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gpusDown",
                kind=MetaData.Type.UINT,
                description="Sum of all GPUs for nodes which are down",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gpusTotal",
                kind=MetaData.Type.UINT,
                description="Sum of all GPUs for nodes which are up at one time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fpgasUp",
                kind=MetaData.Type.UINT,
                description="Sum of all FPGAs for nodes which are up",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fpgasDown",
                kind=MetaData.Type.UINT,
                description="Sum of all FPGAs for nodes which are down",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fpgasTotal",
                kind=MetaData.Type.UINT,
                description="Sum of all FPGAs for nodes which are up at one time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disks",
                kind=MetaData.Type.ENTITY,
                description="Number of disks",
                instance='GuiDiskUsage',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="workload",
                kind=MetaData.Type.ENTITY,
                description="Workload information",
                instance='GuiWorkload',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="usersLoggedIn",
                kind=MetaData.Type.UINT,
                description="Number of logged in users on the active head node",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usersLoggedOut",
                kind=MetaData.Type.UINT,
                description="Number of logged out users on the active head node",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usersTotal",
                kind=MetaData.Type.UINT,
                description="Number of users known to the active head node",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryUsed",
                kind=MetaData.Type.UINT,
                description="Sum of used memory over all nodes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryUnused",
                kind=MetaData.Type.UINT,
                description="Sum of unused memory over all nodes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryTotal",
                kind=MetaData.Type.UINT,
                description="Sum of total memory over all nodes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="swapUsed",
                kind=MetaData.Type.UINT,
                description="Sum of used swap memory over all nodes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="swapUnused",
                kind=MetaData.Type.UINT,
                description="Sum of unused swap memory over all nodes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="swapTotal",
                kind=MetaData.Type.UINT,
                description="Sum of total swap over all nodes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usageUser",
                kind=MetaData.Type.FLOAT,
                description="Average user cpu usage over all nodes",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usageSystem",
                kind=MetaData.Type.FLOAT,
                description="Average system cpu usage over all nodes",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usageIdle",
                kind=MetaData.Type.FLOAT,
                description="Average idle cpu usage over all nodes",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usageOther",
                kind=MetaData.Type.FLOAT,
                description="Percentage of cpu time spend on other operations",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="occupationRate",
                kind=MetaData.Type.FLOAT,
                description="Formula: Average{allnodes} (min(load, cores) / cores)",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="freeRate",
                kind=MetaData.Type.FLOAT,
                description="Formula: 1 - Average{allnodes} (min(load, cores) / cores)",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gpus",
                kind=MetaData.Type.ENTITY,
                description="Detailed GPU information",
                instance='GuiGPU',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="switches",
                kind=MetaData.Type.ENTITY,
                description="Detailed switch information",
                instance='GuiSwitch',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerShelves",
                kind=MetaData.Type.ENTITY,
                description="Detailed powershelf information",
                instance='GuiPowerShelf',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'GuiClusterOverview'
        self.service_type = self.baseType
        self.allTypes = ['GuiClusterOverview']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

