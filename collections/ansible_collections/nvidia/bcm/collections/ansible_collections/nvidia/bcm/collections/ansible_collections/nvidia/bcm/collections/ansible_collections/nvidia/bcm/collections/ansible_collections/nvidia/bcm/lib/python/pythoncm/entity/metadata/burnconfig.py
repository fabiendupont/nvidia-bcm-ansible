from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BurnConfig(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="A short name to identify this burn configuration.",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="description",
                kind=MetaData.Type.STRING,
                description="A more extensive description of this burn configuration.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="configuration",
                kind=MetaData.Type.STRING,
                description="This XML data describes which burn tests should be used.",
                default='',
            )
        )
        self.baseType = 'BurnConfig'
        self.service_type = self.baseType
        self.allTypes = ['BurnConfig']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

