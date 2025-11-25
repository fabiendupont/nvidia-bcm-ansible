from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringStorageSubSystemInfo(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_node_uuid",
                kind=MetaData.Type.UUID,
                description="Node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="elements",
                kind=MetaData.Type.UINT,
                description="Elements",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disksize",
                kind=MetaData.Type.UINT,
                description="Disk size",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="freespace",
                kind=MetaData.Type.UINT,
                description="Free disk space",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usage",
                kind=MetaData.Type.FLOAT,
                description="Usage",
                default=0.0,
            )
        )
        self.baseType = 'MonitoringStorageSubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringStorageSubSystemInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

