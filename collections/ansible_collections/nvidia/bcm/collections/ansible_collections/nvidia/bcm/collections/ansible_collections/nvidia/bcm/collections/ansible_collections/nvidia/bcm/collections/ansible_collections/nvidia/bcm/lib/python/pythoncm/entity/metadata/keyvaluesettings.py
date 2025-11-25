from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class KeyValueSettings(Entity):
    """
    Generic key value settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="keyValues",
                kind=MetaData.Type.STRING,
                description="List of key=value pairs",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'KeyValueSettings'
        self.service_type = self.baseType
        self.allTypes = ['KeyValueSettings']
        self.top_level = False
        self.leaf_entity = True

