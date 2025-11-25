from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiPowerShelfOverview(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_power_shelf_uuid",
                kind=MetaData.Type.UUID,
                description="PowerShelf",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="activePSU",
                kind=MetaData.Type.UINT,
                description="Active PSU",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalPSU",
                kind=MetaData.Type.UINT,
                description="Total PSU",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerSupplies",
                kind=MetaData.Type.ENTITY,
                description="Power supplies",
                instance='GuiPowerShelfSupply',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="info",
                kind=MetaData.Type.JSON,
                description="Additional information",
                default=None,
            )
        )
        self.baseType = 'GuiPowerShelfOverview'
        self.service_type = self.baseType
        self.allTypes = ['GuiPowerShelfOverview']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

