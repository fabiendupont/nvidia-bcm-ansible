from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BeeGFSStorageConfig(Entity):
    """
    BeeGFS management configuration entry
    """
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
                name="dataDirs",
                kind=MetaData.Type.STRING,
                description="Path to the data directories",
                regex_check=r"^/[^\s\0]+$",
                vector=True,
                default=["/var/lib/beegfs/storage"],
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
                name="useAggressiveStreamPoll",
                kind=MetaData.Type.BOOL,
                description="Actively poll for events instead of sleeping until an event occur",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usePerTargetWorkers",
                kind=MetaData.Type.BOOL,
                description="Create a separate set of workers and attach it for each storage target",
                default=True,
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
                name="runDaemonized",
                kind=MetaData.Type.BOOL,
                description="Run the storage service as a daemon",
                default=True,
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
                name="resyncSafetyThreshold",
                kind=MetaData.Type.UINT,
                description="Add an extra amount of time to the last successful communication timestamp, in case of a potential cache loss",
                default=10 * 60,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fileReadAheadSize",
                kind=MetaData.Type.UINT,
                description="Byte range submitted to the kernel for read-ahead after number of bytes was already read from target",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fileReadAheadTriggerSize",
                kind=MetaData.Type.UINT,
                description="Number of bytes after reading which the read-ahead is triggered",
                default=4000000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fileReadSize",
                kind=MetaData.Type.UINT,
                description="Maximum amount of data server should read in a single operation",
                default=128000000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fileWriteSize",
                kind=MetaData.Type.UINT,
                description="Maximum amount of data server should write in a single operation",
                default=128000000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fileWriteSyncSize",
                kind=MetaData.Type.UINT,
                description="Number of bytes after which kernel will be advised to commit data",
                default=128000000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="workerBufferSize",
                kind=MetaData.Type.UINT,
                description="Size of network and io buffers, allocated for each worker",
                default=4000000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numberOfResyncGatherSlaves",
                kind=MetaData.Type.UINT,
                description="Number of threads to gather filesystem information for a buddy mirror resync",
                default=6,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numberOfResyncSlaves",
                kind=MetaData.Type.UINT,
                description="Number of threads to sync filesystem information for a buddy mirror resync",
                default=12,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numberOfStreamListeners",
                kind=MetaData.Type.UINT,
                description="Number of threads waiting for incoming data events",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numberOfWorkers",
                kind=MetaData.Type.UINT,
                description="Number of worker threads",
                default=12,
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
                description="Submode containing BeeGFS storage connection settings",
                instance='BeeGFSStorageConnectionSettings',
                init_instance='BeeGFSStorageConnectionSettings',
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
        self.baseType = 'BeeGFSStorageConfig'
        self.service_type = self.baseType
        self.allTypes = ['BeeGFSStorageConfig']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'ref_beegfs_cluster_uuid'

