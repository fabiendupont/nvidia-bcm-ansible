from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BeeGFSManagementConfig(Entity):
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
                name="dataDir",
                kind=MetaData.Type.STRING,
                description="Path to the data directory",
                regex_check=r"^/[^\s\0]+$",
                default="/var/lib/beegfs/management",
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowNewServers",
                kind=MetaData.Type.BOOL,
                description="Allow new servers registration",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowNewTargets",
                kind=MetaData.Type.BOOL,
                description="Allow new storage targets registration",
                default=True,
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
                name="clientAutoRemove",
                kind=MetaData.Type.UINT,
                description="Time after which an unreachable node is considered dead",
                default=30 * 60,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numberOfWorkers",
                kind=MetaData.Type.UINT,
                description="Number of worker threads",
                default=4,
            )
        )
        self.meta.add(
            MetaDataField(
                name="metaDynamicPools",
                kind=MetaData.Type.BOOL,
                description="Raise lower limits if difference in capacity becomes too large between targets",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="metaInodesLowLimit",
                kind=MetaData.Type.STRING,
                description="Metadata inode free space pool threshold",
                default="10M",
            )
        )
        self.meta.add(
            MetaDataField(
                name="metaInodesEmergencyLimit",
                kind=MetaData.Type.STRING,
                description="Metadata inode free space pool threshold",
                default="1M",
            )
        )
        self.meta.add(
            MetaDataField(
                name="metaSpaceLowLimit",
                kind=MetaData.Type.UINT,
                description="Meta space low limit",
                default=10000000000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="metaSpaceEmergencyLimit",
                kind=MetaData.Type.UINT,
                description="Meta space emergency limit",
                default=3000000000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="storageDynamicPools",
                kind=MetaData.Type.BOOL,
                description="Raise lower limits if difference in capacity becomes too large between targets",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="storageInodesLowLimit",
                kind=MetaData.Type.UINT,
                description="Storage inode free space pool threshold",
                default=10000000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="storageInodesEmergencyLimit",
                kind=MetaData.Type.UINT,
                description="Storage inode free space pool threshold",
                default=1000000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="storageSpaceLowLimit",
                kind=MetaData.Type.UINT,
                description="Storage space free space pool threshold",
                default=1000000000000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="storageSpaceEmergencyLimit",
                kind=MetaData.Type.UINT,
                description="Storage space free space pool threshold",
                default=20000000000,
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
                name="quotaQueryGIDFile",
                kind=MetaData.Type.STRING,
                description="Path to a file with GIDs to be checked by quota",
                regex_check=r"^(/[^\s\0]+)?$",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="quotaGIDs",
                kind=MetaData.Type.STRING,
                description="GIDs to be checked by quota",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="quotaQueryGIDRange",
                kind=MetaData.Type.STRING,
                description="GID range to be checked by quota",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="quotaQueryUIDFile",
                kind=MetaData.Type.STRING,
                description="Path to a file with UIDs to be checked by quota",
                regex_check=r"^(/[^\s\0]+)?$",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="quotaUIDs",
                kind=MetaData.Type.STRING,
                description="UIDs to be checked by quota",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="quotaQueryUIDRange",
                kind=MetaData.Type.STRING,
                description="UID range to be checked by quota",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="quotaQueryType",
                kind=MetaData.Type.STRING,
                description="Query type for quota",
                default="system",
            )
        )
        self.meta.add(
            MetaDataField(
                name="quotaQueryWithSystemUsersGroups",
                kind=MetaData.Type.BOOL,
                description="Allow also system users/groups to be checked by quota",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="quotaUpdateInterval",
                kind=MetaData.Type.UINT,
                description="Quota update interval",
                default=10 * 60,
            )
        )
        self.meta.add(
            MetaDataField(
                name="connectionSettings",
                kind=MetaData.Type.ENTITY,
                description="Submode containing BeeGFS management connection settings",
                instance='BeeGFSManagementConnectionSettings',
                init_instance='BeeGFSManagementConnectionSettings',
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
        self.baseType = 'BeeGFSManagementConfig'
        self.service_type = self.baseType
        self.allTypes = ['BeeGFSManagementConfig']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'ref_beegfs_cluster_uuid'

