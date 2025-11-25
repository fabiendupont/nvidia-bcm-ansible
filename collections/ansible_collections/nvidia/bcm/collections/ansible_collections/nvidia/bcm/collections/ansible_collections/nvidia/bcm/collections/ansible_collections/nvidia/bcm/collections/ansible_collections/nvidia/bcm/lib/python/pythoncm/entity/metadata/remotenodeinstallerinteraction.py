from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class RemoteNodeInstallerInteraction(Entity):
    class Type(Enum):
        FULL_INSTALL = auto()
        DISK_ENCRYPTION_PASSPHRASE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="type",
                kind=MetaData.Type.ENUM,
                description="Type",
                options=[
                    self.Type.FULL_INSTALL,
                    self.Type.DISK_ENCRYPTION_PASSPHRASE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Type,
                default=self.Type.FULL_INSTALL,
            )
        )
        self.meta.add(
            MetaDataField(
                name="node",
                kind=MetaData.Type.RESOLVE,
                description="The node requesting interaction",
                instance='ComputeNode',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="description",
                kind=MetaData.Type.STRING,
                description="The description of the interaction",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="message",
                kind=MetaData.Type.STRING,
                description="The message send back via the manager",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="payload",
                kind=MetaData.Type.STRING,
                description="The resulting payload for the interaction",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="firstSeen",
                kind=MetaData.Type.UINT,
                description="The first time this interaction was requested",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="lastSeen",
                kind=MetaData.Type.UINT,
                description="The last time this interaction was requested",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="wasConfirmed",
                kind=MetaData.Type.BOOL,
                description="Whether the interaction has been confirmed",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="wasDenied",
                kind=MetaData.Type.BOOL,
                description="Whether the interaction has been denied (rejected)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="invalid",
                kind=MetaData.Type.BOOL,
                description="Whether the interaction was found to be invalid",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="force",
                kind=MetaData.Type.BOOL,
                description="Flag to indicate a forced passphrase change",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="reset",
                kind=MetaData.Type.BOOL,
                description="Flag to indicate a custom passphrase should be reset to blank",
                default=False,
            )
        )
        self.baseType = 'RemoteNodeInstallerInteraction'
        self.service_type = self.baseType
        self.allTypes = ['RemoteNodeInstallerInteraction']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

