from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SELinuxSettings(Entity):
    """
    SELinux settings
    """
    class ContextAction(Enum):
        AUTO = auto()
        OS = auto()
        ALWAYS = auto()
        CHECK = auto()

    class Mode(Enum):
        ENFORCING = auto()
        PERMISSIVE = auto()
        DISABLED = auto()

    class Policy(Enum):
        TARGETED = auto()
        MINIMUM = auto()
        MLS = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="initialize",
                kind=MetaData.Type.BOOL,
                description="Determines whether SELinux is to be initialized by the node installer",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rebootAfterContextRestore",
                kind=MetaData.Type.BOOL,
                description="This directive determines whether the compute node is to reboot after performing a full filesystem security context restore",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowNFSHomeDirectories",
                kind=MetaData.Type.BOOL,
                description="This directive determines whether to allow using a remote NFS server for the home directories on the node",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="contextActionAutoInstall",
                kind=MetaData.Type.ENUM,
                description="This directive specifies the action which is to be performed by the Node Installer when the node is being installed in the AUTO mode",
                options=[
                    self.ContextAction.AUTO,
                    self.ContextAction.OS,
                    self.ContextAction.ALWAYS,
                    self.ContextAction.CHECK,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.ContextAction,
                default=self.ContextAction.AUTO,
            )
        )
        self.meta.add(
            MetaDataField(
                name="contextActionFullInstall",
                kind=MetaData.Type.ENUM,
                description="This directive specifies the action which is to be performed by the Node Installer when the node is being installed in the FULL mode",
                options=[
                    self.ContextAction.AUTO,
                    self.ContextAction.OS,
                    self.ContextAction.ALWAYS,
                    self.ContextAction.CHECK,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.ContextAction,
                default=self.ContextAction.AUTO,
            )
        )
        self.meta.add(
            MetaDataField(
                name="contextActionNoSyncInstall",
                kind=MetaData.Type.ENUM,
                description="This directive specifies the action which is to be performed by the Node Installer when the node is being installed in the NOSYNC mode",
                options=[
                    self.ContextAction.AUTO,
                    self.ContextAction.OS,
                    self.ContextAction.ALWAYS,
                    self.ContextAction.CHECK,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.ContextAction,
                default=self.ContextAction.ALWAYS,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mode",
                kind=MetaData.Type.ENUM,
                description="Process policy mode",
                options=[
                    self.Mode.ENFORCING,
                    self.Mode.PERMISSIVE,
                    self.Mode.DISABLED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Mode,
                default=self.Mode.PERMISSIVE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="policy",
                kind=MetaData.Type.ENUM,
                description="Process protection policy",
                options=[
                    self.Policy.TARGETED,
                    self.Policy.MINIMUM,
                    self.Policy.MLS,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Policy,
                default=self.Policy.TARGETED,
            )
        )
        self.meta.add(
            MetaDataField(
                name="keyValueSettings",
                kind=MetaData.Type.ENTITY,
                description="Key value settings which can be used to override SELinux options",
                instance='KeyValueSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.baseType = 'SELinuxSettings'
        self.service_type = self.baseType
        self.allTypes = ['SELinuxSettings']
        self.top_level = False
        self.leaf_entity = True

