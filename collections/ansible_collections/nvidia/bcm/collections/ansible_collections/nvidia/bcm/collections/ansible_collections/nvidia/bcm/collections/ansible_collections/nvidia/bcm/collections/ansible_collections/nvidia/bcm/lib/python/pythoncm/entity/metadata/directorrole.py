from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class DirectorRole(Role):
    """
    Director role
    """
    class Sync(Enum):
        AUTO = auto()
        ALL = auto()
        CUSTOM = auto()

    class CreateHomeDirectories(Enum):
        NEVER = auto()
        ALWAYS = auto()
        WHITELIST = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="syncFSParts",
                kind=MetaData.Type.ENUM,
                description="Sync FSParts mode",
                options=[
                    self.Sync.AUTO,
                    self.Sync.ALL,
                    self.Sync.CUSTOM,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Sync,
                default=self.Sync.AUTO,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fsparts",
                kind=MetaData.Type.RESOLVE,
                description="FSParts",
                instance='FSPart',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="disableAutomaticExports",
                kind=MetaData.Type.BOOL,
                description="Disable creation of automatic filesystem exports",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="createHomeDirectories",
                kind=MetaData.Type.ENUM,
                description="Create home directories for ldap users",
                options=[
                    self.CreateHomeDirectories.NEVER,
                    self.CreateHomeDirectories.ALWAYS,
                    self.CreateHomeDirectories.WHITELIST,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.CreateHomeDirectories,
                default=self.CreateHomeDirectories.NEVER,
            )
        )
        self.meta.add(
            MetaDataField(
                name="whitelistUsers",
                kind=MetaData.Type.STRING,
                description="Whitelist users",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="whitelistGroups",
                kind=MetaData.Type.STRING,
                description="Whitelist groups",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'DirectorRole'
        self.service_type = self.baseType
        self.allTypes = ['DirectorRole', 'Role']
        self.leaf_entity = False

