from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiSwitch(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_switch_uuid",
                kind=MetaData.Type.UUID,
                description="Switch",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerUsage",
                kind=MetaData.Type.FLOAT,
                description="Power usage",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="utilization",
                kind=MetaData.Type.FLOAT,
                description="CPU utilization",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryUtilization",
                kind=MetaData.Type.FLOAT,
                description="Memory utilization",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="networkUtilization",
                kind=MetaData.Type.FLOAT,
                description="Network utilization",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="temperature",
                kind=MetaData.Type.FLOAT,
                description="Average temperature",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fanSpeed",
                kind=MetaData.Type.FLOAT,
                description="Average fan speed",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="linksActive",
                kind=MetaData.Type.UINT,
                description="Active links",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="linksInactive",
                kind=MetaData.Type.UINT,
                description="Inactive links",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="linksTotal",
                kind=MetaData.Type.UINT,
                description="Total links",
                default=0,
            )
        )
        self.baseType = 'GuiSwitch'
        self.service_type = self.baseType
        self.allTypes = ['GuiSwitch']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

