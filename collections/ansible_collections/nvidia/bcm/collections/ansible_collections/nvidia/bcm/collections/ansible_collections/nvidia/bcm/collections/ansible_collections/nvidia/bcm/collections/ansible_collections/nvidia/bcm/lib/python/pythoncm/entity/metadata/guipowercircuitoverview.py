from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiPowerCircuitOverview(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_power_circuit_uuid",
                kind=MetaData.Type.UUID,
                description="PowerCircuit",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="power",
                kind=MetaData.Type.FLOAT,
                description="Circuit power",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="current",
                kind=MetaData.Type.FLOAT,
                description="Current",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="currentLimit",
                kind=MetaData.Type.FLOAT,
                description="Current limit",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="currentPhase1",
                kind=MetaData.Type.FLOAT,
                description="Current phase 1",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="currentPhase2",
                kind=MetaData.Type.FLOAT,
                description="Current phase 2",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="currentPhase3",
                kind=MetaData.Type.FLOAT,
                description="Current phase 3",
                default=0.0,
            )
        )
        self.baseType = 'GuiPowerCircuitOverview'
        self.service_type = self.baseType
        self.allTypes = ['GuiPowerCircuitOverview']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

