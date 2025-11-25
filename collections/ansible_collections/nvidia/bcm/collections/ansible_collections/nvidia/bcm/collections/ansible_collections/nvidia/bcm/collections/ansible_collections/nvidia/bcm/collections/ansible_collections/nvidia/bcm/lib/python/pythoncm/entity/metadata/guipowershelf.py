from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiPowerShelf(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_powershelf_uuid",
                kind=MetaData.Type.UUID,
                description="PowerShelf",
                default=self.zero_uuid,
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
                name="outputPower",
                kind=MetaData.Type.FLOAT,
                description="Total output power",
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
        self.baseType = 'GuiPowerShelf'
        self.service_type = self.baseType
        self.allTypes = ['GuiPowerShelf']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

