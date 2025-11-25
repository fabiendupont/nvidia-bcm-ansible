from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringOffloadBackupInformation(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_monitoring_node_uuid",
                kind=MetaData.Type.UUID,
                description="Node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_backup_node_uuids",
                kind=MetaData.Type.UUID,
                description="Node",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'MonitoringOffloadBackupInformation'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringOffloadBackupInformation']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

