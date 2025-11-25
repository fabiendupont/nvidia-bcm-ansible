from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ProgramRunnerOutput(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="node",
                kind=MetaData.Type.UUID,
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="datacout",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="datacerr",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="exitcode",
                kind=MetaData.Type.INT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="signal",
                kind=MetaData.Type.INT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pid",
                kind=MetaData.Type.INT,
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
                name="state",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.baseType = 'ProgramRunnerOutput'
        self.service_type = self.baseType
        self.allTypes = ['ProgramRunnerOutput']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

