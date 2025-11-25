from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiRackElectricalOverview(Entity):
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
                name="powerUsed",
                kind=MetaData.Type.FLOAT,
                description="Power used",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerBudget",
                kind=MetaData.Type.FLOAT,
                description="Power budget",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="electricalIsolationStatus",
                kind=MetaData.Type.UINT,
                description="Electrical isolation status, 0 means none",
                default=0,
            )
        )
        self.baseType = 'GuiRackElectricalOverview'
        self.service_type = self.baseType
        self.allTypes = ['GuiRackElectricalOverview']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

