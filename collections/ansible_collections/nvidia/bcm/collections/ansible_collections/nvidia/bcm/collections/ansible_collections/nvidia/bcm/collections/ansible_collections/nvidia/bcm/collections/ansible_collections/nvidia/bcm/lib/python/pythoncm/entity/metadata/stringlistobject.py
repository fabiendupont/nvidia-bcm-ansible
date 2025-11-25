from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class StringListObject(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="list",
                kind=MetaData.Type.STRING,
                description="List",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'StringListObject'
        self.service_type = self.baseType
        self.allTypes = ['StringListObject']
        self.top_level = False
        self.leaf_entity = True

