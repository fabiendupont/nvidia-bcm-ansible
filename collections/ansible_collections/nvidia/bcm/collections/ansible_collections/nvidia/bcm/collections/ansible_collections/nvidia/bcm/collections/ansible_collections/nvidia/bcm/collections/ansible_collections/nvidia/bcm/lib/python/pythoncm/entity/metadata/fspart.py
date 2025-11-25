from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class FSPart(Entity):
    class Type(Enum):
        IMAGE = auto()
        BOOT = auto()
        CM_SHARED = auto()
        CM_NODE_INSTALLER = auto()
        TFTPBOOT = auto()
        CUSTOM = auto()
        MONITORING = auto()

    class Compress(Enum):
        NEVER = auto()
        ALWAYS = auto()
        WHEN_SSH = auto()
        WHEN_TUNNEL = auto()
        WHEN_SSH_OR_TUNNEL = auto()

    class CompressLevel(Enum):
        NONE = auto()
        FAST = auto()
        DEFAULT = auto()
        BEST = auto()
        SSH = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="path",
                kind=MetaData.Type.STRING,
                description="Full source path of the filesystem part",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="type",
                kind=MetaData.Type.ENUM,
                description="The type of filesystem part",
                options=[
                    self.Type.IMAGE,
                    self.Type.BOOT,
                    self.Type.CM_SHARED,
                    self.Type.CM_NODE_INSTALLER,
                    self.Type.TFTPBOOT,
                    self.Type.CUSTOM,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Type,
                default=self.Type.CUSTOM,
            )
        )
        self.meta.add(
            MetaDataField(
                name="watchDirectories",
                kind=MetaData.Type.STRING,
                description="Watch directories for changes on the active head node, filesystem part will be marked dirty when changed",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="dirtyAutoSyncDelay",
                kind=MetaData.Type.UINT,
                description="Time to wait before automatically syncing after the filesystem part became dirty, set 0 to disable",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="autoDirtyDelay",
                kind=MetaData.Type.UINT,
                description="Time to wait before automatically marking an filesystem part as dirty, set 0 to disable",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="preSyncScript",
                kind=MetaData.Type.STRING,
                description="Script to be executed before rsync runs",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="postSyncScript",
                kind=MetaData.Type.STRING,
                description="Script to be executed after rsync runs",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="abortOnPreSyncScriptFailure",
                kind=MetaData.Type.BOOL,
                description="Do not rsync if the pre sync script exited with a non zero exit code",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="runPostOnFailure",
                kind=MetaData.Type.BOOL,
                description="Run the post rsync script even if the pre sync or sync ended with a non zero exit code",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="syncScriptTimeout",
                kind=MetaData.Type.UINT,
                description="Script timeout",
                default=15,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rsyncAcls",
                kind=MetaData.Type.BOOL,
                description="Rsync with --acls",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rsyncXattrs",
                kind=MetaData.Type.BOOL,
                description="Rsync with --xattrs",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rsyncHardlinks",
                kind=MetaData.Type.BOOL,
                description="Rsync with --hard-links",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rsyncSparse",
                kind=MetaData.Type.BOOL,
                description="Rsync with --sparse",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rsyncNumericIds",
                kind=MetaData.Type.BOOL,
                description="Rsync with --numeric-ids",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rsyncForce",
                kind=MetaData.Type.BOOL,
                description="Rsync with --force",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rsyncPrune",
                kind=MetaData.Type.BOOL,
                description="Rsync with --prune-empty-dirs",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rsyncDelta",
                kind=MetaData.Type.BOOL,
                description="Rsync with --inplace --no-whole-file",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rsyncBlockSize",
                kind=MetaData.Type.UINT,
                description="Rsync with --block-size=<value> Max 128KB, 0 implies rsync default",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rsyncBandWidthLimit",
                kind=MetaData.Type.UINT,
                description="Rsync with --bwlimit=<value>",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rsyncCompress",
                kind=MetaData.Type.ENUM,
                description="Rsync with --compress",
                options=[
                    self.Compress.NEVER,
                    self.Compress.ALWAYS,
                    self.Compress.WHEN_SSH,
                    self.Compress.WHEN_TUNNEL,
                    self.Compress.WHEN_SSH_OR_TUNNEL,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Compress,
                default=self.Compress.NEVER,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rsyncCompressLevel",
                kind=MetaData.Type.ENUM,
                description="Rsync compression at a specific level",
                options=[
                    self.CompressLevel.NONE,
                    self.CompressLevel.FAST,
                    self.CompressLevel.DEFAULT,
                    self.CompressLevel.BEST,
                    self.CompressLevel.SSH,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.CompressLevel,
                default=self.CompressLevel.DEFAULT,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rsyncCheckNetworkMount",
                kind=MetaData.Type.BOOL,
                description="Rsync check if file is on remote mount before delete and if so: skip it",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="extraRsyncArguments",
                kind=MetaData.Type.STRING,
                description="Extra rsync arguments. These can be made condition based on type=no-new-files|normal and mode=sync|update|full|sync. For example: --max-delete=0?type=normal&mode=update|sync",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeListSnippets",
                kind=MetaData.Type.ENTITY,
                instance='ExcludeListSnippet',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'FSPart'
        self.service_type = self.baseType
        self.allTypes = ['FSPart']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'path'

