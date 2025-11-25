from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudsettings import CloudSettings


class EC2Settings(CloudSettings):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="instanceId",
                kind=MetaData.Type.STRING,
                description="Instance-ID provided by EC2",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="spotId",
                kind=MetaData.Type.STRING,
                description="Spot-request-ID provided by EC2",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="sshConnectString",
                kind=MetaData.Type.STRING,
                description="SSH connection string provided by EC2",
                readonly=True,
                clone=False,
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
                name="releaseStaticIPOnTermination",
                kind=MetaData.Type.BOOL,
                description="Release Static IP on termination of the instance",
                default=True,
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
                name="type",
                kind=MetaData.Type.RESOLVE,
                description="Type for instance",
                instance='EC2Type',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="region",
                kind=MetaData.Type.RESOLVE,
                description="Region for instance",
                instance='EC2Region',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="imageId",
                kind=MetaData.Type.STRING,
                description="ID of the AMI used to create instance ('latest': use latest AMI, '': inherit AMI from cloud provider)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="usesMarketplaceImage",
                kind=MetaData.Type.BOOL,
                description="Whether a paid AWS Marketplace is used for this node",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="allocatePublicIP",
                kind=MetaData.Type.BOOL,
                description="Whether to allocate a public IP for this instance. Always true for cloud directors.",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="sourceDestinationCheck",
                kind=MetaData.Type.BOOL,
                description="Whether to perform source/destination checks on the instance traffic.",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="kernel",
                kind=MetaData.Type.STRING,
                description="Kernel used to create instance",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="initrd",
                kind=MetaData.Type.STRING,
                description="Initial ramdisk used to create instance",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="options",
                kind=MetaData.Type.STRING,
                description="User defined options passed to EC2 on instance creation",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="storage",
                kind=MetaData.Type.ENTITY,
                description="Assign EC2 storage",
                instance='EC2Storage',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="cpuOptions",
                kind=MetaData.Type.STRING,
                description="CPU Options in AWS shorthand syntax (e.g: CoreCount=8,ThreadsPerCore=1)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="spotPrice",
                kind=MetaData.Type.FLOAT,
                description="Maximum price to start instance with",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="spotPersistent",
                kind=MetaData.Type.BOOL,
                description="Persistent spot instances are requested again after they are automatically stopped, because price became to high",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="useNonDefaultVirtualizationType",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="placementGroup",
                kind=MetaData.Type.STRING,
                description="Start instance in the specified placement group",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="iamInstanceProfile",
                kind=MetaData.Type.STRING,
                description="Name or ARN of instance profile to associate with",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="capacityReservationPreference",
                kind=MetaData.Type.STRING,
                description="Capacity reservation preference ('open' or 'none')",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="capacityReservationId",
                kind=MetaData.Type.STRING,
                description="The ID of the Capacity Reservation in which to run the instance",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="capacityReservationResourceGroupARN",
                kind=MetaData.Type.STRING,
                description="The Amazon Resource Name (ARN) of the Capacity Reservation resource group in which to run the instance",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="marketType",
                kind=MetaData.Type.STRING,
                description="Instance market type ('spot' or 'capacity-block')",
                default='',
            )
        )
        self.baseType = 'CloudSettings'
        self.childType = 'EC2Settings'
        self.service_type = self.baseType
        self.allTypes = ['EC2Settings', 'CloudSettings']
        self.top_level = False
        self.leaf_entity = True

