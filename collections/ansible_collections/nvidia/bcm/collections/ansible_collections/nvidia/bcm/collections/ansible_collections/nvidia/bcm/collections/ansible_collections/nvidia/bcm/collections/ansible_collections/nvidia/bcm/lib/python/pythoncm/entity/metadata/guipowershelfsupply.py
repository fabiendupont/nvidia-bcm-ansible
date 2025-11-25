from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiPowerShelfSupply(Entity):
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
                name="index",
                kind=MetaData.Type.UINT,
                description="Index",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="inputPower",
                kind=MetaData.Type.FLOAT,
                description="Total input power",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="inputCurrent",
                kind=MetaData.Type.FLOAT,
                description="Total input current",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="inputVoltage",
                kind=MetaData.Type.FLOAT,
                description="Total input voltage",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="railPower",
                kind=MetaData.Type.FLOAT,
                description="Total rail power",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="railCurrent",
                kind=MetaData.Type.FLOAT,
                description="Total rail current",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="railVoltage",
                kind=MetaData.Type.FLOAT,
                description="Total rail voltage",
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
                name="healthy",
                kind=MetaData.Type.UINT,
                description="Healthy",
                default=0,
            )
        )
        self.baseType = 'GuiPowerShelfSupply'
        self.service_type = self.baseType
        self.allTypes = ['GuiPowerShelfSupply']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

