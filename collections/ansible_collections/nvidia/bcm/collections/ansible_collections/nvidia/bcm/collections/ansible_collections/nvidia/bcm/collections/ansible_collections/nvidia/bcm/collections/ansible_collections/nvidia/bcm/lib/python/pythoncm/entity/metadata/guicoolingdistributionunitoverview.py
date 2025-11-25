from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiCoolingDistributionUnitOverview(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_device_uuid",
                kind=MetaData.Type.UUID,
                description="Cooling distribution unit",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="liquidSupplyTemperature",
                kind=MetaData.Type.FLOAT,
                description="Liquid supply temperature",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="liquidReturnTemperature",
                kind=MetaData.Type.FLOAT,
                description="Liquid return temperature",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="liquidDifferentialPressure",
                kind=MetaData.Type.FLOAT,
                description="Liquid differential pressure",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="liquidFlow",
                kind=MetaData.Type.FLOAT,
                description="Liquid flow",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="liquidSystemPressure",
                kind=MetaData.Type.FLOAT,
                description="Liquid system pressure",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="status",
                kind=MetaData.Type.UINT,
                description="Status",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="available",
                kind=MetaData.Type.UINT,
                description="Available",
                default=0,
            )
        )
        self.baseType = 'GuiCoolingDistributionUnitOverview'
        self.service_type = self.baseType
        self.allTypes = ['GuiCoolingDistributionUnitOverview']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

