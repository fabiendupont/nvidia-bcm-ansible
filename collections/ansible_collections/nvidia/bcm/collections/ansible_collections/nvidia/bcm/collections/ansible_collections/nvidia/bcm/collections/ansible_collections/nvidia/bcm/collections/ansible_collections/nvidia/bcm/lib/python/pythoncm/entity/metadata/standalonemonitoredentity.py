from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class StandaloneMonitoredEntity(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="type",
                kind=MetaData.Type.STRING,
                description="Optional type in case name matches an other entity",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="data",
                kind=MetaData.Type.STRING,
                description="Data that will be passed to the script enivironment",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="notes",
                kind=MetaData.Type.STRING,
                description="Notes",
                default='',
            )
        )
        self.baseType = 'StandaloneMonitoredEntity'
        self.service_type = self.baseType
        self.allTypes = ['StandaloneMonitoredEntity']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

