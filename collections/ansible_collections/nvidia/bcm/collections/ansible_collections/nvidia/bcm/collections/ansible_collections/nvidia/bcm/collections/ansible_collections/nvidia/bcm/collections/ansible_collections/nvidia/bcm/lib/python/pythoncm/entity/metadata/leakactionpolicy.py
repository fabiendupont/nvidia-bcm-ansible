from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class LeakActionPolicy(Entity):
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
                name="rules",
                kind=MetaData.Type.ENTITY,
                description="Rules for this policy",
                instance='LeakActionRule',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'LeakActionPolicy'
        self.service_type = self.baseType
        self.allTypes = ['LeakActionPolicy']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

