from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudprovider import CloudProvider


class AzureProvider(CloudProvider):
    class HyperVGeneration(Enum):
        V1 = auto()
        V2 = auto()

    class MarketplacePreference(Enum):
        ALWAYS = auto()
        NEVER = auto()
        AS_NEEDED = auto()

    class FreeImageType(Enum):
        VHD = auto()
        MARKETPLACE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="subscriptionId",
                kind=MetaData.Type.STRING,
                description="Azure Subscription ID.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="clientId",
                kind=MetaData.Type.STRING,
                description="Azure Client ID.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="clientSecret",
                kind=MetaData.Type.STRING,
                description="Azure Client Secret.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="tenantId",
                kind=MetaData.Type.STRING,
                description="Tenant ID.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="cloudName",
                kind=MetaData.Type.STRING,
                description="Azure Cloud Name. Used to access non-public regions.",
                default="AzureCloud",
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultLocation",
                kind=MetaData.Type.RESOLVE,
                description="Default location to start virtual machine in.",
                instance='AzureLocation',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultVMSize",
                kind=MetaData.Type.RESOLVE,
                description="Default cloud node VM size.",
                instance='AzureVMSize',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultDirectorVMSize",
                kind=MetaData.Type.RESOLVE,
                description="Default cloud director VM size.",
                instance='AzureVMSize',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultHyperVGeneration",
                kind=MetaData.Type.ENUM,
                description="Hyper-V generation to use by default (V1 or V2), see https://docs.microsoft.com/en-us/azure/virtual-machines/generation-2",
                options=[
                    self.HyperVGeneration.V1,
                    self.HyperVGeneration.V2,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.HyperVGeneration,
                default=self.HyperVGeneration.V1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="extensions",
                kind=MetaData.Type.ENTITY,
                description="List of extensions",
                instance='AzureExtension',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="regions",
                kind=MetaData.Type.RESOLVE,
                instance='AzureLocation',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultNodeInstallerImage",
                kind=MetaData.Type.STRING,
                description="Default node-installer image, can be overridden in the OS disk.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="marketplaceUsePolicy",
                kind=MetaData.Type.ENUM,
                description="Preference towards using marketplace images",
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
        self.meta.add(
            MetaDataField(
                name="freeImageType",
                kind=MetaData.Type.ENUM,
                description="What kind of image to use for cloud nodes within the license",
                options=[
                    self.FreeImageType.VHD,
                    self.FreeImageType.MARKETPLACE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.FreeImageType,
                default=self.FreeImageType.MARKETPLACE,
            )
        )
        self.baseType = 'CloudProvider'
        self.childType = 'AzureProvider'
        self.service_type = self.baseType
        self.allTypes = ['AzureProvider', 'CloudProvider']
        self.top_level = True
        self.leaf_entity = True

