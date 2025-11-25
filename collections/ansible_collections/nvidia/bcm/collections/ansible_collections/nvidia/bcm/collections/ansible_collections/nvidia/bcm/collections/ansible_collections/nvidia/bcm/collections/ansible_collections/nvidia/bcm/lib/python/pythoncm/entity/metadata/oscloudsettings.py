from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudsettings import CloudSettings


class OSCloudSettings(CloudSettings):
    class VMState(Enum):
        TERMINATED = auto()
        CREATED = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="instanceId",
                kind=MetaData.Type.STRING,
                description="Unique ID of the instance in OpenStack (the UUID).",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="secGroupId",
                kind=MetaData.Type.STRING,
                description="Security group name/ID",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="region",
                kind=MetaData.Type.RESOLVE,
                description="The region of the cloud the VM is located in.",
                instance='OSCloudRegion',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="flavor",
                kind=MetaData.Type.RESOLVE,
                description="Instance Flavor (the type of the VM).",
                instance='OSCloudFlavor',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="image",
                kind=MetaData.Type.STRING,
                description="The name of the cloud image used for creating the VM.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="disks",
                kind=MetaData.Type.ENTITY,
                description="Definitions of storage devices of the VM.",
                instance='OSCloudDisk',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="availabilityZone",
                kind=MetaData.Type.STRING,
                description="Availability zone the VM is supposed to be created in. If left empty, the availability zone will be automatically assigned by the cloud.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="externalIP",
                kind=MetaData.Type.STRING,
                description="The external IP address as set by the cloudprovider",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
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
        self.baseType = 'CloudSettings'
        self.childType = 'OSCloudSettings'
        self.service_type = self.baseType
        self.allTypes = ['OSCloudSettings', 'CloudSettings']
        self.top_level = False
        self.leaf_entity = True

