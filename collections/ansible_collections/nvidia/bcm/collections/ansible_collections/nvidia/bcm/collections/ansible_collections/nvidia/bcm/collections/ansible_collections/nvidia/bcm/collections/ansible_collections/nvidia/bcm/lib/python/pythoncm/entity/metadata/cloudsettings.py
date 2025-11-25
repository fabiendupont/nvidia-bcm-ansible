from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CloudSettings(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="provider",
                kind=MetaData.Type.RESOLVE,
                description="Cloud provider",
                instance='CloudProvider',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="tags",
                kind=MetaData.Type.STRING,
                description="List of tags that will be assigned to cloud instance (for supported providers)",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'CloudSettings'
        self.service_type = self.baseType
        self.allTypes = ['CloudSettings']
        self.leaf_entity = False

