from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class FirmwareInfo(Entity):
    class State(Enum):
        PENDING = auto()
        UPLOADING = auto()
        FLASHING = auto()
        EXCEPTION = auto()
        COMPLETED = auto()
        CANCELED = auto()
        CURRENT = auto()
        UNDEFINED = auto()
        AVAILABLE = auto()
        ERROR = auto()

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
                name="filename",
                kind=MetaData.Type.STRING,
                description="Filename",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="component",
                kind=MetaData.Type.STRING,
                description="Component",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="version",
                kind=MetaData.Type.STRING,
                description="Version",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="state",
                kind=MetaData.Type.ENUM,
                description="Result",
                options=[
                    self.State.PENDING,
                    self.State.UPLOADING,
                    self.State.FLASHING,
                    self.State.EXCEPTION,
                    self.State.COMPLETED,
                    self.State.CANCELED,
                    self.State.CURRENT,
                    self.State.UNDEFINED,
                    self.State.AVAILABLE,
                    self.State.ERROR,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.State,
                default=self.State.UNDEFINED,
            )
        )
        self.meta.add(
            MetaDataField(
                name="progress",
                kind=MetaData.Type.FLOAT,
                description="Progress",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="result",
                kind=MetaData.Type.STRING,
                description="Result",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="size",
                kind=MetaData.Type.UINT,
                description="Size",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="date",
                kind=MetaData.Type.STRING,
                description="Date",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="timestamp",
                kind=MetaData.Type.TIMESTAMP,
                description="Epoch timestamp, parsed version of date",
                default=0,
            )
        )
        self.baseType = 'FirmwareInfo'
        self.service_type = self.baseType
        self.allTypes = ['FirmwareInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

