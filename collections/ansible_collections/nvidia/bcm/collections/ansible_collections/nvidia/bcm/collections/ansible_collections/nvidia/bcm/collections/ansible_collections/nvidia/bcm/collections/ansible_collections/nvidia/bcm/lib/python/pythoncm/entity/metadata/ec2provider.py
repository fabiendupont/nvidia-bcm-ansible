from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudprovider import CloudProvider


class EC2Provider(CloudProvider):
    class MarketplacePreference(Enum):
        ALWAYS = auto()
        NEVER = auto()
        AS_NEEDED = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="APIRegionName",
                kind=MetaData.Type.STRING,
                description="AWS region to be used for listing available regions",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="accessKeyId",
                kind=MetaData.Type.STRING,
                description="AWS access key ID",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="accessKeySecret",
                kind=MetaData.Type.STRING,
                description="AWS secret access key",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="iamRoleName",
                kind=MetaData.Type.STRING,
                description="IAM role to get AWS credentials from. The role must be assigned to the COD-AWS head node.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="VPCs",
                kind=MetaData.Type.ENTITY,
                description="List of VPCs",
                instance='EC2VPC',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="regions",
                kind=MetaData.Type.RESOLVE,
                instance='EC2Region',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultRegion",
                kind=MetaData.Type.RESOLVE,
                description="Default region to start instances in",
                instance='EC2Region',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultType",
                kind=MetaData.Type.RESOLVE,
                description="Default type for instances",
                instance='EC2Type',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultDirectorType",
                kind=MetaData.Type.RESOLVE,
                description="Default type for cloud director instances",
                instance='EC2Type',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="imageOwners",
                kind=MetaData.Type.STRING,
                description="AWS Account IDs to be used to search for images",
                vector=True,
                default=["137677339600", "197943594779"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="addJobBasedTag",
                kind=MetaData.Type.BOOL,
                description="Enable automatic tagging of cloud resources with information of running cloud jobs to allow cost monitoring",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="JobIdTagName",
                kind=MetaData.Type.STRING,
                description="The name of the tag that contains the job ID when using job based tagging",
                default="BCM_JOB_ID",
            )
        )
        self.meta.add(
            MetaDataField(
                name="JobAccountTagName",
                kind=MetaData.Type.STRING,
                description="The name of the tag that contains the job account when using job based tagging",
                default="BCM_JOB_ACCOUNT",
            )
        )
        self.meta.add(
            MetaDataField(
                name="JobUserTagName",
                kind=MetaData.Type.STRING,
                description="The name of the tag that contains the user name when using job based tagging",
                default="BCM_JOB_USER",
            )
        )
        self.meta.add(
            MetaDataField(
                name="JobNameTagName",
                kind=MetaData.Type.STRING,
                description="The name of the tag that contains the job name when using job based tagging",
                default="BCM_JOB_NAME",
            )
        )
        self.meta.add(
            MetaDataField(
                name="marketplaceUsePolicy",
                kind=MetaData.Type.ENUM,
                description="Preference towards using marketplace AMIs",
                options=[
                    self.MarketplacePreference.ALWAYS,
                    self.MarketplacePreference.NEVER,
                    self.MarketplacePreference.AS_NEEDED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.MarketplacePreference,
                default=self.MarketplacePreference.NEVER,
            )
        )
        self.baseType = 'CloudProvider'
        self.childType = 'EC2Provider'
        self.service_type = self.baseType
        self.allTypes = ['EC2Provider', 'CloudProvider']
        self.top_level = True
        self.leaf_entity = True

