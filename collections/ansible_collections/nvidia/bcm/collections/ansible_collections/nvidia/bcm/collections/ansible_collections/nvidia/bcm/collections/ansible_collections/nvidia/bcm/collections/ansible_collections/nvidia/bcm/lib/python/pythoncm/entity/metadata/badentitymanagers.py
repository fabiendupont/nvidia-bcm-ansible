from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BadEntityManagers(Entity):
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
                name="added",
                kind=MetaData.Type.STRING,
                description="Added",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="removed",
                kind=MetaData.Type.STRING,
                description="Removed",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="changed",
                kind=MetaData.Type.STRING,
                description="Changed",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="error",
                kind=MetaData.Type.STRING,
                description="Error",
                default='',
            )
        )
        self.baseType = 'BadEntityManagers'
        self.service_type = self.baseType
        self.allTypes = ['BadEntityManagers']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

