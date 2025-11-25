from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudprovider import CloudProvider


class ForgeProvider(CloudProvider):
    class NgcAuthScope(Enum):
        NGC = auto()
        NGC_STG = auto()
        NONE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="authApiKey",
                kind=MetaData.Type.STRING,
                description="API key to connect to Forge",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="authTenantId",
                kind=MetaData.Type.STRING,
                description="Forge tenant ID",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="authOrganizationId",
                kind=MetaData.Type.STRING,
                description="Forge organization ID",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="authSiteId",
                kind=MetaData.Type.STRING,
                description="Forge site ID",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ngcAuthUrl",
                kind=MetaData.Type.STRING,
                description="URL for NGC authentication",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ngcApiUrl",
                kind=MetaData.Type.STRING,
                description="URL for NGC API",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ngcAuthScope",
                kind=MetaData.Type.ENUM,
                description="Scope for NGC authentication",
                options=[
                    self.NgcAuthScope.NGC,
                    self.NgcAuthScope.NGC_STG,
                    self.NgcAuthScope.NONE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.NgcAuthScope,
                default=self.NgcAuthScope.NONE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="vpcId",
                kind=MetaData.Type.STRING,
                description="ID of the VPC containing the cluster",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="consoleKeyGroupId",
                kind=MetaData.Type.STRING,
                description="ID of the SSH key group for serial console connection",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultInstanceType",
                kind=MetaData.Type.RESOLVE,
                description="Default cloud node instance type.",
                instance='ForgeInstanceType',
                entity_allow_null=True,
                default=None,
            )
        )
        self.baseType = 'CloudProvider'
        self.childType = 'ForgeProvider'
        self.service_type = self.baseType
        self.allTypes = ['ForgeProvider', 'CloudProvider']
        self.top_level = True
        self.leaf_entity = True

