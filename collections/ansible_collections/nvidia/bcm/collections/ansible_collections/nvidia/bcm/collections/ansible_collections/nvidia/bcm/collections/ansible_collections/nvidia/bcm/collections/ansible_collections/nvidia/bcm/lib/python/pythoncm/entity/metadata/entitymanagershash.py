from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class EntityManagersHash(Entity):
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
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="hashes",
                kind=MetaData.Type.STRING,
                description="Hashes",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'EntityManagersHash'
        self.service_type = self.baseType
        self.allTypes = ['EntityManagersHash']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

