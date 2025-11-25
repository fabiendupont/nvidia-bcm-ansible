from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CloudProvider(Entity):
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
                name="tags",
                kind=MetaData.Type.STRING,
                description="List of tags that will be assigned to all resources created by BCM under this cloud provider",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'CloudProvider'
        self.service_type = self.baseType
        self.allTypes = ['CloudProvider']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

