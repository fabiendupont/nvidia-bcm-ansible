from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiRackOverview(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_rack_uuid",
                kind=MetaData.Type.UUID,
                description="Rack",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="information",
                kind=MetaData.Type.STRING,
                description="Short text describing rack information",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobs",
                kind=MetaData.Type.ENTITY,
                description="Detailed job information",
                instance='GuiJob',
                vector=True,
                default=[],
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
                name="nvlinkSwitchesUp",
                kind=MetaData.Type.UINT,
                description="Number of nvlink switches that are listed as up",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nvlinkSwitchesDown",
                kind=MetaData.Type.UINT,
                description="Number of nvlink switches that are listed as down",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nvlinkSwitchesClosed",
                kind=MetaData.Type.UINT,
                description="Number of nvlink switches that are listed as closed",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nvlinkSwitchesTotal",
                kind=MetaData.Type.UINT,
                description="Number of nvlink switches",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerShelvesUp",
                kind=MetaData.Type.UINT,
                description="Number of power shelves that are listed as up",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerShelvesDown",
                kind=MetaData.Type.UINT,
                description="Number of power shelves that are listed as down",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerShelvesClosed",
                kind=MetaData.Type.UINT,
                description="Number of power shelves that are listed as closed",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerShelvesTotal",
                kind=MetaData.Type.UINT,
                description="Number of power shelves",
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
                name="totalPowerShelfAvailablePSU",
                kind=MetaData.Type.FLOAT,
                description="Available PSU",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalPowerShelfInputPower",
                kind=MetaData.Type.FLOAT,
                description="Total power shelf input power",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalPowerShelfInputCurrent",
                kind=MetaData.Type.FLOAT,
                description="Total power shelf input current",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalPowerShelfRailPower",
                kind=MetaData.Type.FLOAT,
                description="Total power shelf rail power",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalPowerShelfRailCurrent",
                kind=MetaData.Type.FLOAT,
                description="Total power shelf rail current",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="averagePowerShelfTemperature",
                kind=MetaData.Type.FLOAT,
                description="Average power shelf temperature",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalGPUNvlinkBandwidth",
                kind=MetaData.Type.FLOAT,
                description="Total GPU NVLink bandwidth",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalGPUPowerUsage",
                kind=MetaData.Type.FLOAT,
                description="Total GPU power usage",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalGPUUtilization",
                kind=MetaData.Type.FLOAT,
                description="Total GPU utilization",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="averageGPUTemperature",
                kind=MetaData.Type.FLOAT,
                description="Average GPU temperature",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalCPUPowerUsage",
                kind=MetaData.Type.FLOAT,
                description="Total CPU power usage",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="averageCPUTemperature",
                kind=MetaData.Type.FLOAT,
                description="Average CPU temperature",
                default=0.0,
            )
        )
        self.baseType = 'GuiRackOverview'
        self.service_type = self.baseType
        self.allTypes = ['GuiRackOverview']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

