from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MemoryInfo(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="IDs",
                kind=MetaData.Type.STRING,
                description="IDs",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="locations",
                kind=MetaData.Type.STRING,
                description="Location",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="speed",
                kind=MetaData.Type.UINT,
                description="Speed",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="size",
                kind=MetaData.Type.UINT,
                description="Size",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="description",
                kind=MetaData.Type.STRING,
                description="Description",
                default='',
            )
        )
        self.baseType = 'MemoryInfo'
        self.service_type = self.baseType
        self.allTypes = ['MemoryInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

