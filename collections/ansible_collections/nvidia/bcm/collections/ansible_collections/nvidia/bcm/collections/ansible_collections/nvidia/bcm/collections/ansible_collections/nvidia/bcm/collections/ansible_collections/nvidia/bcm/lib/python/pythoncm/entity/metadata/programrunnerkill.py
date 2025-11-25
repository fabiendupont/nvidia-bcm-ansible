from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ProgramRunnerKill(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="node",
                kind=MetaData.Type.UUID,
                description="Node key",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="running",
                kind=MetaData.Type.INT,
                description="Running",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="trackers",
                kind=MetaData.Type.UUID,
                description="Tackers",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="results",
                kind=MetaData.Type.INT,
                description="results",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'ProgramRunnerKill'
        self.service_type = self.baseType
        self.allTypes = ['ProgramRunnerKill']
        self.top_level = False
        self.leaf_entity = True

