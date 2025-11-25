from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class EC2RegionAMI(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="region",
                kind=MetaData.Type.RESOLVE,
                description="The cloud region containing this AMI",
                instance='EC2Region',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="amiID",
                kind=MetaData.Type.STRING,
                description="The AMI ID",
                default='',
            )
        )
        self.baseType = 'EC2RegionAMI'
        self.service_type = self.baseType
        self.allTypes = ['EC2RegionAMI']
        self.top_level = False
        self.leaf_entity = True

