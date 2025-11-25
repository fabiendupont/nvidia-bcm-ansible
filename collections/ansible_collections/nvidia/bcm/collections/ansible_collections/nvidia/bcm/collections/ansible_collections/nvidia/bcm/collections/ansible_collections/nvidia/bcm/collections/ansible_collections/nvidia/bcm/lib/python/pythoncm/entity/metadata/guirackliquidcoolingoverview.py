from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiRackLiquidCoolingOverview(Entity):
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
                name="supplyTemperature",
                kind=MetaData.Type.FLOAT,
                description="Supply temperature",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="returnTemperature",
                kind=MetaData.Type.FLOAT,
                description="Return temperature",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="flowRate",
                kind=MetaData.Type.FLOAT,
                description="Flow rate",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="differentialPressure",
                kind=MetaData.Type.FLOAT,
                description="Differential pressure",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="liquidIsolationStatus",
                kind=MetaData.Type.UINT,
                description="Liquid isolation status, 0 means none",
                default=0,
            )
        )
        self.baseType = 'GuiRackLiquidCoolingOverview'
        self.service_type = self.baseType
        self.allTypes = ['GuiRackLiquidCoolingOverview']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

