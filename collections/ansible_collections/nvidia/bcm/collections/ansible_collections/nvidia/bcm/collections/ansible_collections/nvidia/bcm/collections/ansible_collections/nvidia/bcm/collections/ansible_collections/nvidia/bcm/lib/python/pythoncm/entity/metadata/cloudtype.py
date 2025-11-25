from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CloudType(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="The name of the VM type.",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="provider",
                kind=MetaData.Type.RESOLVE,
                description="Cloud provider",
                instance='CloudProvider',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cpu",
                kind=MetaData.Type.STRING,
                description="The amount of CPU cores.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="gpu",
                kind=MetaData.Type.STRING,
                description="The amount of GPUs.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="memory",
                kind=MetaData.Type.STRING,
                description="The amount of operating system memory.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="disks",
                kind=MetaData.Type.STRING,
                description="AWS: The amount of disks comming with the type. Azure: the maximum amount of data disks that can be attached to VMs of this type. OCI: The number of local disks available for this shape. GCP: Maximum number of persistent disks.     ",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="description",
                kind=MetaData.Type.STRING,
                description="The description.",
                default='',
            )
        )
        self.baseType = 'CloudType'
        self.service_type = self.baseType
        self.allTypes = ['CloudType']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

