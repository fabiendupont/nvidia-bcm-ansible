from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class EC2OnDemandPrice(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="regionName",
                kind=MetaData.Type.STRING,
                description="Region name.",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="instanceType",
                kind=MetaData.Type.STRING,
                description="Instance type.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="price",
                kind=MetaData.Type.STRING,
                description="On-demand price.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="currency",
                kind=MetaData.Type.STRING,
                description="Currency.",
                default='',
            )
        )
        self.baseType = 'EC2OnDemandPrice'
        self.service_type = self.baseType
        self.allTypes = ['EC2OnDemandPrice']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'regionName'
        self.add_to_cluster = False
        self.allow_commit = False

