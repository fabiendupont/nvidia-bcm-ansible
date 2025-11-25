from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class FileWriteInfo(Entity):
    class Actor(Enum):
        CMD = auto()
        NODE_INSTALLER = auto()
        PYTHONCM = auto()
        CM_SETUP = auto()
        CM_LITE_DAEMON = auto()
        OTHER = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_device_uuid",
                kind=MetaData.Type.UUID,
                description="Device",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="path",
                kind=MetaData.Type.STRING,
                description="Path",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="timestamp",
                kind=MetaData.Type.TIMESTAMP,
                description="Timestamp on which file was last changed",
                clone=False,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="actor",
                kind=MetaData.Type.ENUM,
                description="Actor that wrote the file",
                options=[
                    self.Actor.CMD,
                    self.Actor.NODE_INSTALLER,
                    self.Actor.PYTHONCM,
                    self.Actor.CM_SETUP,
                    self.Actor.CM_LITE_DAEMON,
                    self.Actor.OTHER,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Actor,
                default=self.Actor.CMD,
            )
        )
        self.meta.add(
            MetaDataField(
                name="frozen",
                kind=MetaData.Type.BOOL,
                description="Frozen",
                default=False,
            )
        )
        self.baseType = 'FileWriteInfo'
        self.service_type = self.baseType
        self.allTypes = ['FileWriteInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

