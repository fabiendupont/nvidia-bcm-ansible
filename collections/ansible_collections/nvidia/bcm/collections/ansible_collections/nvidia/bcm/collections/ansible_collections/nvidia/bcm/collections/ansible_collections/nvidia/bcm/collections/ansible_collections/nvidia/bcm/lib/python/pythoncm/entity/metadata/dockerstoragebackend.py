from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class DockerStorageBackend(Entity):
    """
    Docker storage backend
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Docker storage backend name",
                required=True,
                default='',
            )
        )
        self.baseType = 'DockerStorageBackend'
        self.service_type = self.baseType
        self.allTypes = ['DockerStorageBackend']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

