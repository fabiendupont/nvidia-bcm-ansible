from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudprovider import CloudProvider


class OSCloudProvider(CloudProvider):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="cloudApiType",
                kind=MetaData.Type.STRING,
                description="Cloud provider type",
                default="rackspace",
            )
        )
        self.meta.add(
            MetaDataField(
                name="authUrl",
                kind=MetaData.Type.STRING,
                description="Keystone URL",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="username",
                kind=MetaData.Type.STRING,
                description="Username",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="password",
                kind=MetaData.Type.STRING,
                description="Password",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="projectId",
                kind=MetaData.Type.STRING,
                description="Project ID",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="projectName",
                kind=MetaData.Type.STRING,
                description="Project Name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="projectDomainId",
                kind=MetaData.Type.STRING,
                description="Project Domain Id",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="userDomainId",
                kind=MetaData.Type.STRING,
                description="User Domain Id",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="keyPairName",
                kind=MetaData.Type.STRING,
                description="SSH Key Pair Name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="openStackVersion",
                kind=MetaData.Type.STRING,
                description="OpenStack release version (e.g. 2015.1.3)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="openStackVersionName",
                kind=MetaData.Type.STRING,
                description="OpenStack release codename (e.g. Kilo)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="extensions",
                kind=MetaData.Type.ENTITY,
                description="List of extensions",
                instance='OSCloudExtension',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultRegion",
                kind=MetaData.Type.RESOLVE,
                description="Default region to start instances",
                instance='OSCloudRegion',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultFlavor",
                kind=MetaData.Type.RESOLVE,
                description="Default cloud node flavor",
                instance='OSCloudFlavor',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultDirectorFlavor",
                kind=MetaData.Type.RESOLVE,
                description="Default cloud director Flavor",
                instance='OSCloudFlavor',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultImage",
                kind=MetaData.Type.STRING,
                description="Default node-installer image, can be overridden in the OS disk",
                default='',
            )
        )
        self.baseType = 'CloudProvider'
        self.childType = 'OSCloudProvider'
        self.service_type = self.baseType
        self.allTypes = ['OSCloudProvider', 'CloudProvider']
        self.top_level = True
        self.leaf_entity = True

