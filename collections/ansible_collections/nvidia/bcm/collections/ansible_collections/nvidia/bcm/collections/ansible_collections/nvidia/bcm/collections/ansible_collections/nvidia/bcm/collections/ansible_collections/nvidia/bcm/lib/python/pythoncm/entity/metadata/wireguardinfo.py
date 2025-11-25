from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class WireguardInfo(Entity):
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
                name="interface",
                kind=MetaData.Type.STRING,
                description="Interface name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="publicKey",
                kind=MetaData.Type.STRING,
                description="Public key",
                default='',
            )
        )
        self.baseType = 'WireguardInfo'
        self.service_type = self.baseType
        self.allTypes = ['WireguardInfo']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

