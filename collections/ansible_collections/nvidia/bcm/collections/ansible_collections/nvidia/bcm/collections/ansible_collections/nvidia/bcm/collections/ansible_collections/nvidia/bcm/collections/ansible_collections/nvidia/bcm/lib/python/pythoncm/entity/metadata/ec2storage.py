from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class EC2Storage(Entity):
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
                name="drive",
                kind=MetaData.Type.STRING,
                description="Mount device as /dev/?",
                regex_check=r"^(/dev/)?(h|xv|s)d[a-z]$",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="tags",
                kind=MetaData.Type.STRING,
                description="List of tags that will be assigned to storage",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'EC2Storage'
        self.service_type = self.baseType
        self.allTypes = ['EC2Storage']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

