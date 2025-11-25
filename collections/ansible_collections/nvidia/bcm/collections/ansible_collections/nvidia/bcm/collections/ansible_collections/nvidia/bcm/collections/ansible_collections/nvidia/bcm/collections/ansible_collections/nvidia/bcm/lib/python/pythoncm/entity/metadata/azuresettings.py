from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudsettings import CloudSettings


class AzureSettings(CloudSettings):
    class HyperVGeneration(Enum):
        UNDEFINED = auto()
        V1 = auto()
        V2 = auto()

    class FreeImageType(Enum):
        UNDEFINED = auto()
        VHD = auto()
        MARKETPLACE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="instanceId",
                kind=MetaData.Type.STRING,
                description="Instance-ID provided by Azure",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="availabilitySetName",
                kind=MetaData.Type.STRING,
                description="Availability set name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="nicId",
                kind=MetaData.Type.STRING,
                description="Network interface identifier",
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
        self.meta.add(
            MetaDataField(
                name="location",
                kind=MetaData.Type.RESOLVE,
                description="Virtual Machine location",
                instance='AzureLocation',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="resourceGroupName",
                kind=MetaData.Type.STRING,
                description="Azure Resource Group Name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="storageAccountName",
                kind=MetaData.Type.STRING,
                description="Name of a storage account where boot diagnostics will be stored for this instance",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="deploymentName",
                kind=MetaData.Type.STRING,
                description="Name of the Azure deployment associated with this node",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="publicIpName",
                kind=MetaData.Type.STRING,
                description="Name of a public ip object to be assigned to the node",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="VMSize",
                kind=MetaData.Type.RESOLVE,
                description="Virtual Machine size",
                instance='AzureVMSize',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hyperVGeneration",
                kind=MetaData.Type.ENUM,
                description="Hyper-V generation to use (V1 or V2), see https://docs.microsoft.com/en-us/azure/virtual-machines/generation-2",
                options=[
                    self.HyperVGeneration.UNDEFINED,
                    self.HyperVGeneration.V1,
                    self.HyperVGeneration.V2,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.HyperVGeneration,
                default=self.HyperVGeneration.UNDEFINED,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disks",
                kind=MetaData.Type.ENTITY,
                description="Storage disks.",
                instance='AzureDisk',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="availabilityZone",
                kind=MetaData.Type.STRING,
                description="Azure Availability zone where all the resources related to this VM will be allocated",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="freeImageType",
                kind=MetaData.Type.ENUM,
                description="What kind of image to use for cloud nodes within the license",
                options=[
                    self.FreeImageType.UNDEFINED,
                    self.FreeImageType.VHD,
                    self.FreeImageType.MARKETPLACE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.FreeImageType,
                default=self.FreeImageType.UNDEFINED,
            )
        )
        self.baseType = 'CloudSettings'
        self.childType = 'AzureSettings'
        self.service_type = self.baseType
        self.allTypes = ['AzureSettings', 'CloudSettings']
        self.top_level = False
        self.leaf_entity = True

