from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class NodeGroup(Entity):
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
                name="nodes",
                kind=MetaData.Type.RESOLVE,
                description="List of nodes belonging to this group",
                instance='Node',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'NodeGroup'
        self.service_type = self.baseType
        self.allTypes = ['NodeGroup']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

