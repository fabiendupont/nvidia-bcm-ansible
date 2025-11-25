from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ProgramRunnerStatus(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="startTime",
                kind=MetaData.Type.TIMESTAMP,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="runtime",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="session_uuid",
                kind=MetaData.Type.UUID,
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="running",
                kind=MetaData.Type.INT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="unknown",
                kind=MetaData.Type.INT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="internal",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.UUID,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="state",
                kind=MetaData.Type.INT,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="input",
                kind=MetaData.Type.ENTITY,
                instance='ProgramRunnerInput',
                default=None,
            )
        )
        self.baseType = 'ProgramRunnerStatus'
        self.service_type = self.baseType
        self.allTypes = ['ProgramRunnerStatus']
        self.top_level = True
        self.leaf_entity = True
        self.allow_commit = False

