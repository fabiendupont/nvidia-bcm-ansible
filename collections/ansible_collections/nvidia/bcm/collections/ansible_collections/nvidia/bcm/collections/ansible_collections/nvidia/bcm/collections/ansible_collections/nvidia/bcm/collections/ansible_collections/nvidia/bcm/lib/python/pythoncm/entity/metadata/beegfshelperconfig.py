from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BeeGFSHelperConfig(Entity):
    """
    BeeGFS helper configuration entry
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
                name="runDaemonized",
                kind=MetaData.Type.BOOL,
                description="Run the helper as a daemon",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="workersNumber",
                kind=MetaData.Type.UINT,
                description="Number of worker threads for helper service",
                default=2,
            )
        )
        self.meta.add(
            MetaDataField(
                name="connectionSettings",
                kind=MetaData.Type.ENTITY,
                description="Submode containing BeeGFS helper connection settings",
                instance='BeeGFSHelperConnectionSettings',
                init_instance='BeeGFSHelperConnectionSettings',
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
        self.baseType = 'BeeGFSHelperConfig'
        self.service_type = self.baseType
        self.allTypes = ['BeeGFSHelperConfig']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'ref_beegfs_cluster_uuid'

