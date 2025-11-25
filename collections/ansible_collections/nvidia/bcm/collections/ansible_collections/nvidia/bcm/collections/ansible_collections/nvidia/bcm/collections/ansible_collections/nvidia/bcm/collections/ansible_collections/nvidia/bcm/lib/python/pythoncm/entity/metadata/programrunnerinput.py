from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ProgramRunnerInput(Entity):
    class Logger(Enum):
        NONE = auto()
        ACTION = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="user",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="startInShell",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cmd",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="info",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="args",
                kind=MetaData.Type.STRING,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="env",
                kind=MetaData.Type.STRING,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="datacin",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mergeCoutCerr",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxruntime",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="updateinterval",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="priority",
                kind=MetaData.Type.INT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="tracker",
                kind=MetaData.Type.UUID,
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="logger",
                kind=MetaData.Type.ENUM,
                options=[
                    self.Logger.NONE,
                    self.Logger.ACTION,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Logger,
                default=self.Logger.NONE,
            )
        )
        self.baseType = 'ProgramRunnerInput'
        self.service_type = self.baseType
        self.allTypes = ['ProgramRunnerInput']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

