from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.ec2storage import EC2Storage


class EC2EphemeralStorage(EC2Storage):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="volumeId",
                kind=MetaData.Type.STRING,
                description="Ephemral ID",
                regex_check=r"^ephemeral[0-9]$",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="size",
                kind=MetaData.Type.UINT,
                description="Size",
                readonly=True,
                default=0,
            )
        )
        self.baseType = 'EC2Storage'
        self.childType = 'EC2EphemeralStorage'
        self.service_type = self.baseType
        self.allTypes = ['EC2EphemeralStorage', 'EC2Storage']
        self.top_level = False
        self.leaf_entity = True

