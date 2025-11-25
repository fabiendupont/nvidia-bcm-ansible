from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CMService(Entity):
    def __init__(self):
        super().__init__()
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
                name="tokens",
                kind=MetaData.Type.STRING,
                description="Tokens belonging to this service",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'CMService'
        self.service_type = self.baseType
        self.allTypes = ['CMService']
        self.top_level = True
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

