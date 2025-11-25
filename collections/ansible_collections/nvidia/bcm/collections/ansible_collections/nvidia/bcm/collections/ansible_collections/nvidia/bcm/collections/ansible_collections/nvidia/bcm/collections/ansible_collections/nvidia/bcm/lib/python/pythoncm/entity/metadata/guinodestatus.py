from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiNodeStatus(Entity):
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
                name="status",
                kind=MetaData.Type.ENTITY,
                description="Device status",
                instance='DeviceStatus',
                default=None,
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
                name="swapUsed",
                kind=MetaData.Type.UINT,
                description="Swap memory used",
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
        self.baseType = 'GuiNodeStatus'
        self.service_type = self.baseType
        self.allTypes = ['GuiNodeStatus']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

