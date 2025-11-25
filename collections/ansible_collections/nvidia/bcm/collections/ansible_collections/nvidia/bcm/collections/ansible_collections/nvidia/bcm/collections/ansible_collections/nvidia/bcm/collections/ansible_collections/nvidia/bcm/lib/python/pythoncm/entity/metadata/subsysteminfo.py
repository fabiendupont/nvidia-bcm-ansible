from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SubSystemInfo(Entity):
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
                name="timestamp",
                kind=MetaData.Type.TIMESTAMP,
                description="Time",
                default=0,
            )
        )
        self.baseType = 'SubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['SubSystemInfo']
        self.leaf_entity = False
        self.add_to_cluster = False
        self.allow_commit = False

