from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SystemctlUnit(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_node_uuid",
                kind=MetaData.Type.UUID,
                description="Node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="unit",
                kind=MetaData.Type.STRING,
                description="Unit",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="load",
                kind=MetaData.Type.STRING,
                description="Load",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="active",
                kind=MetaData.Type.STRING,
                description="Active",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="sub",
                kind=MetaData.Type.STRING,
                description="The low-level unit activation state, values depend on unit type",
                default='',
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
        self.baseType = 'SystemctlUnit'
        self.service_type = self.baseType
        self.allTypes = ['SystemctlUnit']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

