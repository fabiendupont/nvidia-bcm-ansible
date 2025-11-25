from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Validation(Entity):
    class Error(Enum):
        NOT_NULL = auto()
        NOT_SET = auto()
        NOT_IN_SET = auto()
        BAD_VALUE = auto()
        MISMATCH = auto()
        KEY_NOT_FOUND = auto()
        DUPLICATE_FIELD = auto()
        OUT_OF_RANGE = auto()
        NOT_ALLOWED = auto()
        SAVE_FAILED = auto()
        NOT_ACTIVE = auto()
        LOAD_FAILED = auto()
        DUPLICATE_NAME = auto()
        PRE_UPDATE = auto()
        LICENCE_NODECOUNT = auto()
        GENERIC_WARNING = auto()

    class Severity(Enum):
        WARNING = auto()
        ERROR = auto()
        FORCE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_entity_uuid",
                kind=MetaData.Type.UUID,
                description="Entity",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="field",
                kind=MetaData.Type.STRING,
                description="Field",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="error_code",
                kind=MetaData.Type.ENUM,
                description="Error",
                options=[
                    self.Error.NOT_NULL,
                    self.Error.NOT_SET,
                    self.Error.NOT_IN_SET,
                    self.Error.BAD_VALUE,
                    self.Error.MISMATCH,
                    self.Error.KEY_NOT_FOUND,
                    self.Error.DUPLICATE_FIELD,
                    self.Error.OUT_OF_RANGE,
                    self.Error.NOT_ALLOWED,
                    self.Error.SAVE_FAILED,
                    self.Error.NOT_ACTIVE,
                    self.Error.LOAD_FAILED,
                    self.Error.DUPLICATE_NAME,
                    self.Error.PRE_UPDATE,
                    self.Error.LICENCE_NODECOUNT,
                    self.Error.GENERIC_WARNING,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Error,
                default=self.Error.NOT_SET,
            )
        )
        self.meta.add(
            MetaDataField(
                name="message",
                kind=MetaData.Type.STRING,
                description="Message",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="severity",
                kind=MetaData.Type.ENUM,
                description="Severity",
                options=[
                    self.Severity.WARNING,
                    self.Severity.ERROR,
                    self.Severity.FORCE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Severity,
                default=self.Severity.ERROR,
            )
        )
        self.baseType = 'Validation'
        self.service_type = self.baseType
        self.allTypes = ['Validation']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

