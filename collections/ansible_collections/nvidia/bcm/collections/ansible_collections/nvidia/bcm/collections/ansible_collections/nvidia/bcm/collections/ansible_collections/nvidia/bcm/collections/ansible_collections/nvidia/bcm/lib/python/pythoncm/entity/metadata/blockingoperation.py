from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BlockingOperation(Entity):
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
                name="message",
                kind=MetaData.Type.STRING,
                description="Message",
                default='',
            )
        )
        self.baseType = 'BlockingOperation'
        self.service_type = self.baseType
        self.allTypes = ['BlockingOperation']
        self.leaf_entity = False
        self.allow_commit = False

