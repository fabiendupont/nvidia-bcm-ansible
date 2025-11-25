from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PbsPelog(Entity):
    """
    PBS pelog (prolog/epilog) hook settings
    """
    class PbsPelogAction(Enum):
        RERUN = auto()
        DELETE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="enabled",
                kind=MetaData.Type.BOOL,
                description="Enable hook",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Hook name in PBS",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="events",
                kind=MetaData.Type.STRING,
                description="List of hook events",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="path",
                kind=MetaData.Type.STRING,
                description="Fully qualified pathname of a hook script",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultAction",
                kind=MetaData.Type.ENUM,
                description="PBS prolog/epilog default action",
                options=[
                    self.PbsPelogAction.RERUN,
                    self.PbsPelogAction.DELETE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.PbsPelogAction,
                default=self.PbsPelogAction.RERUN,
            )
        )
        self.meta.add(
            MetaDataField(
                name="enableParallel",
                kind=MetaData.Type.BOOL,
                description="Enable parallel prologues/epilogues that run on sister moms",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="verboseUserOutput",
                kind=MetaData.Type.BOOL,
                description="Provide verbose hook output to the user's .o/.e file",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="torqueCompatible",
                kind=MetaData.Type.BOOL,
                description="Make torque compatible",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="order",
                kind=MetaData.Type.UINT,
                description="Hook order",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="alarm",
                kind=MetaData.Type.UINT,
                description="Hook alarm time (timeout)",
                default=300,
            )
        )
        self.meta.add(
            MetaDataField(
                name="debug",
                kind=MetaData.Type.BOOL,
                description="Enable hook debug (in PBS)",
                default=False,
            )
        )
        self.baseType = 'PbsPelog'
        self.service_type = self.baseType
        self.allTypes = ['PbsPelog']
        self.top_level = False
        self.leaf_entity = True

