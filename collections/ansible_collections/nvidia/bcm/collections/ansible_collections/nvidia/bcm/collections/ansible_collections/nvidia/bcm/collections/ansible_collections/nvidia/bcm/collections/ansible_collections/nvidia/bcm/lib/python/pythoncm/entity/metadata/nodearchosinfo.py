from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class NodeArchOSInfo(Entity):
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
                name="timestamp",
                kind=MetaData.Type.UINT,
                description="Reported timestamp",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="reportedArchOS",
                kind=MetaData.Type.ENTITY,
                description="Reported arch/OS",
                instance='ArchOSInfo',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="configuredArchOS",
                kind=MetaData.Type.ENTITY,
                description="Configured arch/OS",
                instance='ArchOSInfo',
                entity_allow_null=True,
                default=None,
            )
        )
        self.baseType = 'NodeArchOSInfo'
        self.service_type = self.baseType
        self.allTypes = ['NodeArchOSInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

