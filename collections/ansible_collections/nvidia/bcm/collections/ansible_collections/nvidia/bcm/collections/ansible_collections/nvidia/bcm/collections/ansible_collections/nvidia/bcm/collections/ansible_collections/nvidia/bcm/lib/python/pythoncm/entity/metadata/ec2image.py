from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class EC2Image(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="The name of the image.",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="id",
                kind=MetaData.Type.STRING,
                description="The AMI ID",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="apiHash",
                kind=MetaData.Type.STRING,
                description="The API hash used to select compatible images.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="regionName",
                kind=MetaData.Type.STRING,
                description="The name of the image region.",
                required=True,
                default='',
            )
        )
        self.baseType = 'EC2Image'
        self.service_type = self.baseType
        self.allTypes = ['EC2Image']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'regionName'

