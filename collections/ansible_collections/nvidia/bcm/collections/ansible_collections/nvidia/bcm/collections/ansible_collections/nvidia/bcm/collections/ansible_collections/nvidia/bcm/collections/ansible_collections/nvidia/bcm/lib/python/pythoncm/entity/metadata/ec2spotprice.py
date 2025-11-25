from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class EC2SpotPrice(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="az",
                kind=MetaData.Type.STRING,
                description="Availabiliy zone.",
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
                description="Spot price.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="timestamp",
                kind=MetaData.Type.UINT,
                description="Price timestamp.",
                default=0,
            )
        )
        self.baseType = 'EC2SpotPrice'
        self.service_type = self.baseType
        self.allTypes = ['EC2SpotPrice']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'az'
        self.add_to_cluster = False
        self.allow_commit = False

