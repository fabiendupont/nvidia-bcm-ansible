from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiNodeOverview(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_node_uuid",
                kind=MetaData.Type.UUID,
                description="Node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="information",
                kind=MetaData.Type.STRING,
                description="Short text describing node information",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="interfaces",
                kind=MetaData.Type.ENTITY,
                description="Detailed interface information",
                instance='GuiNetworkInterface',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="disks",
                kind=MetaData.Type.ENTITY,
                description="Detailed disk information",
                instance='GuiDiskUsage',
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
                name="load1",
                kind=MetaData.Type.FLOAT,
                description="Average system load over the last minute",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="load5",
                kind=MetaData.Type.FLOAT,
                description="Average system load over the last five minutes",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="load15",
                kind=MetaData.Type.FLOAT,
                description="Average system load over the last fifteen minutes",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="uptime",
                kind=MetaData.Type.UINT,
                description="Uptime",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryUsed",
                kind=MetaData.Type.UINT,
                description="Memory used",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryUnused",
                kind=MetaData.Type.UINT,
                description="Memory unused",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryTotal",
                kind=MetaData.Type.UINT,
                description="Total memory",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="swapUsed",
                kind=MetaData.Type.UINT,
                description="Swap memory used",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="swapUnused",
                kind=MetaData.Type.UINT,
                description="Swap memory unused",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="swapTotal",
                kind=MetaData.Type.UINT,
                description="Total swap memory",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="wlmSlotsUsed",
                kind=MetaData.Type.UINT,
                description="WLM slots used",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="wlmSlotsUnused",
                kind=MetaData.Type.UINT,
                description="WLM slots unused",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="wlmSlotsTotal",
                kind=MetaData.Type.UINT,
                description="Total WLM slots",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usageUser",
                kind=MetaData.Type.FLOAT,
                description="Percentage of cpu time spend on user processes",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usageSystem",
                kind=MetaData.Type.FLOAT,
                description="Percentage of cpu time spend on system processes",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usageIdle",
                kind=MetaData.Type.FLOAT,
                description="Percentage of cpu time spend in idle",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usageOther",
                kind=MetaData.Type.FLOAT,
                description="Percentage of cpu time spend in non user/system/idle",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usageSoftIrq",
                kind=MetaData.Type.FLOAT,
                description="Percentage of cpu time spend in soft irq",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usageIrq",
                kind=MetaData.Type.FLOAT,
                description="Percentage of cpu time spend in irq",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usageNice",
                kind=MetaData.Type.FLOAT,
                description="Percentage of cpu time spend in nice",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usageSteal",
                kind=MetaData.Type.FLOAT,
                description="Percentage of cpu time spend in steal",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usageGuest",
                kind=MetaData.Type.FLOAT,
                description="Percentage of cpu time spend in guest",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usageWait",
                kind=MetaData.Type.FLOAT,
                description="Percentage of cpu time spend in wait",
                default=0.0,
            )
        )
        self.baseType = 'GuiNodeOverview'
        self.service_type = self.baseType
        self.allTypes = ['GuiNodeOverview']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

