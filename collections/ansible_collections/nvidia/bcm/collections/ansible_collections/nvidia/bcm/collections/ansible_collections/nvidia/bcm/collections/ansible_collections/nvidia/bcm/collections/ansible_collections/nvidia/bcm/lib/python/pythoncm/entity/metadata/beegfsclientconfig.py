from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BeeGFSClientConfig(Entity):
    """
    BeeGFS client configuration entry
    """
    class BeeGFSClientLogType(Enum):
        SYSLOG = auto()
        HELPERD = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_beegfs_cluster_uuid",
                kind=MetaData.Type.UUID,
                description="BeeGFS cluster",
                required=True,
                diff_type=MetaDataField.Diff.disabled,
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="enableQuota",
                kind=MetaData.Type.BOOL,
                description="Enable quota",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="createHardlinksAsSymlinks",
                kind=MetaData.Type.BOOL,
                description="Create a symlink when an application tries to create a hardlink",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mountSanityCheck",
                kind=MetaData.Type.FLOAT,
                description="Time in ms server has to respond after mount sanity check",
                default=11.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="sessionCheckOnClose",
                kind=MetaData.Type.BOOL,
                description="Check for valid sessions on storage server when a file is closed",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="syncOnClose",
                kind=MetaData.Type.BOOL,
                description="Sync file content on close",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="targetOfflineTimeout",
                kind=MetaData.Type.UINT,
                description="Timeout until all storage targets are considered offlinewhen no target state updates can be fetched from management server",
                default=900,
            )
        )
        self.meta.add(
            MetaDataField(
                name="updateTargetStatesTime",
                kind=MetaData.Type.FLOAT,
                description="Interval for storage targets states check",
                default=60,
            )
        )
        self.meta.add(
            MetaDataField(
                name="enableXAttrs",
                kind=MetaData.Type.BOOL,
                description="Enable xattrs",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="enableACLs",
                kind=MetaData.Type.BOOL,
                description="Enable ACLs",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fileCacheType",
                kind=MetaData.Type.STRING,
                description="File read/write cache type",
                default="buffered",
            )
        )
        self.meta.add(
            MetaDataField(
                name="preferredMetaFile",
                kind=MetaData.Type.STRING,
                description="Path to a file with preffered metadata servers",
                regex_check=r"^(/[^\s\0]+)?$",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="preferredStorageFile",
                kind=MetaData.Type.STRING,
                description="Path to a file with preffered storage targets",
                regex_check=r"^(/[^\s\0]+)?$",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="preferredMetadataServers",
                kind=MetaData.Type.STRING,
                description="Preferred metadata server IDs",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="preferredStorageServers",
                kind=MetaData.Type.STRING,
                description="Preferred metadata server IDs",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="remoteFSync",
                kind=MetaData.Type.BOOL,
                description="Should fsync be executed on server to flush cached file",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="useGlobalAppendLocks",
                kind=MetaData.Type.BOOL,
                description="Should files, opened in append mode, be protected by locks on local machine (YES) or on servers (NO)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="useGlobalFileLocks",
                kind=MetaData.Type.BOOL,
                description="Should advisory locks be checked on local machine (YES) or on servers (NO)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="connectionSettings",
                kind=MetaData.Type.ENTITY,
                description="Submode containing BeeGFS client connection settings",
                instance='BeeGFSClientConnectionSettings',
                init_instance='BeeGFSClientConnectionSettings',
                create_instance=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="logType",
                kind=MetaData.Type.ENUM,
                description="Send log messages to the helper daemon or syslog to send them to the system logger",
                options=[
                    self.BeeGFSClientLogType.SYSLOG,
                    self.BeeGFSClientLogType.HELPERD,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.BeeGFSClientLogType,
                default=self.BeeGFSClientLogType.SYSLOG,
            )
        )
        self.meta.add(
            MetaDataField(
                name="level",
                kind=MetaData.Type.UINT,
                description="Log level",
                default=3,
            )
        )
        self.meta.add(
            MetaDataField(
                name="addClientId",
                kind=MetaData.Type.BOOL,
                description="Defines whether the ClientID should appear in each log line",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="helperIp",
                kind=MetaData.Type.STRING,
                description="Defines the IP address of the node on which the beegfs-helperd runs for remote logging",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.baseType = 'BeeGFSClientConfig'
        self.service_type = self.baseType
        self.allTypes = ['BeeGFSClientConfig']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'ref_beegfs_cluster_uuid'

