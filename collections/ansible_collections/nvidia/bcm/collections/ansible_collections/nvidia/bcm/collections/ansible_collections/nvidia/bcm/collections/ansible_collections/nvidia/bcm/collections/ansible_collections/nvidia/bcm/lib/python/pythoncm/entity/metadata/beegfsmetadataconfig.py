from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BeeGFSMetadataConfig(Entity):
    """
    BeeGFS metadata configuration entry
    """
    class StorageTargetType(Enum):
        RANDOMIZED = auto()
        ROUNDROBIN = auto()
        RANDOMROBIN = auto()
        RANDOMINTERNODE = auto()
        RANDOMINTRANODE = auto()

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
                name="dataDir",
                kind=MetaData.Type.STRING,
                description="Path to the data directory",
                regex_check=r"^/[^\s\0]+$",
                default="/var/lib/beegfs/metadata",
            )
        )
        self.meta.add(
            MetaDataField(
                name="bindToNumaZone",
                kind=MetaData.Type.STRING,
                description="Zero-based NUMA zone number to which all threads of metadata process should be bound",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="runDaemonized",
                kind=MetaData.Type.BOOL,
                description="Run the storage service as a daemon",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="clientXAttrs",
                kind=MetaData.Type.BOOL,
                description="Enable client-side extended attributes",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="clientACLs",
                kind=MetaData.Type.BOOL,
                description="Enable handling and storage of client-side ACLs",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="useExtendedAttributes",
                kind=MetaData.Type.BOOL,
                description="Store metadata as extended attributes or not",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowUserSetPattern",
                kind=MetaData.Type.BOOL,
                description="Allow non-privileged users to modify stripe pattern settings for directories they own",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="useAggressiveStreamPoll",
                kind=MetaData.Type.BOOL,
                description="Actively poll for events instead of sleeping until an event occur",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usePerUserMsgQueues",
                kind=MetaData.Type.BOOL,
                description="Use per-user queues for pending requests",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="targetChooser",
                kind=MetaData.Type.ENUM,
                description="The algorithm to choose storage targets for file creation",
                options=[
                    self.StorageTargetType.RANDOMIZED,
                    self.StorageTargetType.ROUNDROBIN,
                    self.StorageTargetType.RANDOMROBIN,
                    self.StorageTargetType.RANDOMINTERNODE,
                    self.StorageTargetType.RANDOMINTRANODE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.StorageTargetType,
                default=self.StorageTargetType.RANDOMIZED,
            )
        )
        self.meta.add(
            MetaDataField(
                name="targetOfflineTimeout",
                kind=MetaData.Type.UINT,
                description="Timeout until targets on a storage server are considered offline when no target status is received",
                default=180,
            )
        )
        self.meta.add(
            MetaDataField(
                name="targetAttachmentFile",
                kind=MetaData.Type.STRING,
                description="File with a list of targets to be grouped within the same domain for randominternode",
                regex_check=r"^(/[^\s\0]+)?$",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="numberOfStreamListeners",
                kind=MetaData.Type.UINT,
                description="The number of threads waiting for incoming data events",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numberOfWorkers",
                kind=MetaData.Type.UINT,
                description="Number of worker threads",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="startByCMDaemon",
                kind=MetaData.Type.BOOL,
                description="Start service by CMDaemon or manually",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="connectionSettings",
                kind=MetaData.Type.ENTITY,
                description="Submode containing BeeGFS metadata connection settings",
                instance='BeeGFSMetadataConnectionSettings',
                init_instance='BeeGFSMetadataConnectionSettings',
                create_instance=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="logSettings",
                kind=MetaData.Type.ENTITY,
                description="Submode containing BeeGFS logging settings",
                instance='BeeGFSLogSettings',
                init_instance='BeeGFSLogSettings',
                create_instance=True,
                default=None,
            )
        )
        self.baseType = 'BeeGFSMetadataConfig'
        self.service_type = self.baseType
        self.allTypes = ['BeeGFSMetadataConfig']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'ref_beegfs_cluster_uuid'

