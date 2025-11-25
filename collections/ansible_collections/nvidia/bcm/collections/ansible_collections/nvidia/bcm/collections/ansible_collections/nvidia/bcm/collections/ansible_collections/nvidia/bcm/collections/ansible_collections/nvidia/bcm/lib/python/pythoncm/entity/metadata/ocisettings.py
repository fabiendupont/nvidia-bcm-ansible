from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudsettings import CloudSettings


class OCISettings(CloudSettings):
    class CapacityTypes(Enum):
        ON_DEMAND = auto()
        PREEMPTIBLE = auto()
        RESERVED = auto()
        DEDICATED = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="compartmentId",
                kind=MetaData.Type.STRING,
                description="Compartment ID",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="availabilityDomain",
                kind=MetaData.Type.STRING,
                description="Availability domain",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="instanceId",
                kind=MetaData.Type.STRING,
                description="Instance ID in OCI",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="imageId",
                kind=MetaData.Type.STRING,
                description="ID of the image used to create instance ('latest': use latest AMI, '': inherit AMI from cloud provider)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ocpus",
                kind=MetaData.Type.UINT,
                description="Oracle CPUs. If set to 0 then the default value from the shape will be used",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memory",
                kind=MetaData.Type.UINT,
                description="Size of the node's main memory. If set to 0 then the default value from the shape will be used",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disks",
                kind=MetaData.Type.ENTITY,
                description="Definitions of storage devices of the VM",
                instance='OCIDisk',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="shape",
                kind=MetaData.Type.RESOLVE,
                description="Instance shape",
                instance='OCIShape',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="region",
                kind=MetaData.Type.RESOLVE,
                description="Region for instance",
                instance='OCIRegion',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="instancePool",
                kind=MetaData.Type.RESOLVE,
                description="Instance pool to place the VM in",
                instance='OCIInstancePool',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gpuMemoryCluster",
                kind=MetaData.Type.RESOLVE,
                description="GPU memory cluster the VM is in",
                instance='OCIGPUMemoryCluster',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="useKernelAndInitrdFromTheSoftwareImage",
                kind=MetaData.Type.BOOL,
                description="Make the cloud node's node-installer download the kernel and the initrd from the software image configured for this cloud node and then reboot the cloud node to use those, instead of using the kernel and initrd already present on the node-installer's cloud image.",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="definedTags",
                kind=MetaData.Type.STRING,
                description="List of OCI defined tags that will be assigned to cloud instance. Defined tags are case-insensitive and require the format 'namespace.key.value'",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="capacityType",
                kind=MetaData.Type.ENUM,
                description="Instance capacity type",
                options=[
                    self.CapacityTypes.ON_DEMAND,
                    self.CapacityTypes.PREEMPTIBLE,
                    self.CapacityTypes.RESERVED,
                    self.CapacityTypes.DEDICATED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.CapacityTypes,
                default=self.CapacityTypes.ON_DEMAND,
            )
        )
        self.meta.add(
            MetaDataField(
                name="capacityReservationId",
                kind=MetaData.Type.STRING,
                description="Capacity Reservation ID",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="platformConfig",
                kind=MetaData.Type.ENTITY,
                description="The platform configuration requested for the instance.",
                instance='OCIPlatformConfig',
                init_instance='OCIPlatformConfig',
                create_instance=True,
                default=None,
            )
        )
        self.baseType = 'CloudSettings'
        self.childType = 'OCISettings'
        self.service_type = self.baseType
        self.allTypes = ['OCISettings', 'CloudSettings']
        self.top_level = False
        self.leaf_entity = True

