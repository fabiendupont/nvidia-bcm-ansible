from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class OSCloudDisk(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name of the disk",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="bootIndex",
                kind=MetaData.Type.INT,
                description="Defines the order in which a hypervisor will try devices when attempting to boot the guest from storage. Setting a negative value indicates that the device should not be used for booting",
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="size",
                kind=MetaData.Type.UINT,
                description="Size of the disk",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="diskBus",
                kind=MetaData.Type.STRING,
                description="Hypervisor-specific details about disk bus type",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="deviceType",
                kind=MetaData.Type.STRING,
                description="Hypervisor-specific details about disk device type",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="removeOnTermination",
                kind=MetaData.Type.BOOL,
                description="If true, the drive will be removed when the instance it is attached to gets terminated",
                default=True,
            )
        )
        self.baseType = 'OSCloudDisk'
        self.service_type = self.baseType
        self.allTypes = ['OSCloudDisk']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

