from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class BackupRole(Role):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="directory",
                kind=MetaData.Type.STRING,
                description="Directory where backups for other nodes are saved",
                default="/var/spool/cmd/backup",
            )
        )
        self.meta.add(
            MetaDataField(
                name="disabled",
                kind=MetaData.Type.BOOL,
                description="Disabled nodes will no longer be used",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="backupRing",
                kind=MetaData.Type.UINT,
                description="Only backup to nodes within the same ring",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maximumNumberOfBackups",
                kind=MetaData.Type.UINT,
                description="Maximum number of backups this node should be used for, set 0 for unlimited",
                default=0,
            )
        )
        self.baseType = 'Role'
        self.childType = 'BackupRole'
        self.service_type = self.baseType
        self.allTypes = ['BackupRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

