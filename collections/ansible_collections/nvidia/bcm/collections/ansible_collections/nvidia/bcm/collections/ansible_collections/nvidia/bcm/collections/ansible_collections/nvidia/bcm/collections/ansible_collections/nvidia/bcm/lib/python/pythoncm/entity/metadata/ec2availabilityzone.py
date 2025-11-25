from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class EC2AvailabilityZone(Entity):
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
        self.baseType = 'EC2AvailabilityZone'
        self.service_type = self.baseType
        self.allTypes = ['EC2AvailabilityZone']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

