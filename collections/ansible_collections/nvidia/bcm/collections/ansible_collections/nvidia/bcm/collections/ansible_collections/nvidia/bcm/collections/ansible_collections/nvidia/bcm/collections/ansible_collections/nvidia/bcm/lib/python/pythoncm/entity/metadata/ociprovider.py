from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudprovider import CloudProvider


class OCIProvider(CloudProvider):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="defaultNodeInstallerImageId",
                kind=MetaData.Type.STRING,
                description="Default node-installer image, can be overridden in cloudsettings",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultCompartmentId",
                kind=MetaData.Type.STRING,
                description="Default compartment ID used, others are listed in https://cloud.oracle.com/identity/compartments.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultRegion",
                kind=MetaData.Type.RESOLVE,
                description="Default region to start virtual machine in.",
                instance='OCIRegion',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultShape",
                kind=MetaData.Type.RESOLVE,
                description="Default cloud node VM shape.",
                instance='OCIShape',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="APIRegionName",
                kind=MetaData.Type.STRING,
                description="OCI region name to be used for listing available regions",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="regions",
                kind=MetaData.Type.RESOLVE,
                instance='OCIRegion',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="securityGroupNode",
                kind=MetaData.Type.STRING,
                description="Security group ID of the cloud nodes",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="computeClusterID",
                kind=MetaData.Type.STRING,
                description="Compute Cluster ID for nodes that use GPU Memory Cluster",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultAvailabilityDomain",
                kind=MetaData.Type.STRING,
                description="Default availablity domain for cloud nodes",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="authUser",
                kind=MetaData.Type.STRING,
                description="User ocid. Format is ocid1.user.oc1..<unique ID>, can be found in Profile->User Settings",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="authKeyContent",
                kind=MetaData.Type.STRING,
                description="API private key file's content (PEM format) to connect to OCI",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="authFingerprint",
                kind=MetaData.Type.STRING,
                description="Fingerprint of API Keys. Format is 12:34:56:78:90:ab:cd:ef:12:34:56:78:90:ab:cd:ef, can be found in Identity->Users->User Details->API Keys",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="authTenancy",
                kind=MetaData.Type.STRING,
                description="Usually one company will have a single tenancy. Format is ocid1.tenancy.oc1..<unique ID>, can be found in https://cloud.oracle.com/tenancy",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="imagesCompartmentId",
                kind=MetaData.Type.STRING,
                description="Compartment OCID to search for custom images",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="imagesManifestBaseURL",
                kind=MetaData.Type.STRING,
                description="Base URL to download images manifests",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="definedTags",
                kind=MetaData.Type.STRING,
                description="List of OCI defined tags that will be assigned to cloud nodes. Defined tags are case-insensitive and require the format 'namespace.key.value'",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'CloudProvider'
        self.childType = 'OCIProvider'
        self.service_type = self.baseType
        self.allTypes = ['OCIProvider', 'CloudProvider']
        self.top_level = True
        self.leaf_entity = True

