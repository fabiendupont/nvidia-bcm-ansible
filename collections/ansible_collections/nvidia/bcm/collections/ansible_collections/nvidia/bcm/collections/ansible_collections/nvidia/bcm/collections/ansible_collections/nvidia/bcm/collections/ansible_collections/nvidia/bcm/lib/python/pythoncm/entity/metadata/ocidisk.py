from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class OCIDisk(Entity):
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
                name="size",
                kind=MetaData.Type.UINT,
                description="Size of the drive",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="kmsKeyId",
                kind=MetaData.Type.STRING,
                description="The OCID of the Vault service key to assign as the master encryption key for the volume",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="vpusPerGb",
                kind=MetaData.Type.UINT,
                description="The number of volume performance units (VPUs) that will be applied to this volume per GB, representing the Block Volume service's elastic performance options",
                default=10,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxVPUsPerGB",
                kind=MetaData.Type.UINT,
                description="This will be the maximum VPUs/GB performance level that the volume will be auto-tuned temporarily based on performance monitoring. This parameter has an effect only if performance based autotune is enabled",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="enablePerformanceBasedAutotune",
                kind=MetaData.Type.BOOL,
                description="If a volume is being throttled at the current setting for a certain period of time, auto-tune will gradually increase the volume's performance limited up to Maximum VPUs/GB. After the volume has been idle at the current setting for a certain period of time, auto-tune will gradually decrease the volume's performance limited down to Default/Minimum VPUs/GB",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="enableDetachedAutotune",
                kind=MetaData.Type.BOOL,
                description="Volume's performace will be tuned to the lower cost settings once detached",
                default=False,
            )
        )
        self.baseType = 'OCIDisk'
        self.service_type = self.baseType
        self.allTypes = ['OCIDisk']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

