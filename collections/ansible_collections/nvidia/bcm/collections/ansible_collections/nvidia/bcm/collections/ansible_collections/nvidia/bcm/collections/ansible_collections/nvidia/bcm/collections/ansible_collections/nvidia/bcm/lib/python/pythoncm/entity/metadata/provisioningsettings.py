from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ProvisioningSettings(Entity):
    """
    Provisioning settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="dirtyAutoUpdateTimeout",
                kind=MetaData.Type.UINT,
                description="Delay after which a provisioning node is considered out of date and automatically updated when needed (0 to disable automatic updates)",
                default=300,
            )
        )
        self.meta.add(
            MetaDataField(
                name="autoUpdatePeriod",
                kind=MetaData.Type.UINT,
                description="Period after which all provisioning nodes are automatically updated (0 to disable automatic updates)",
                default=86400,
            )
        )
        self.meta.add(
            MetaDataField(
                name="noRestartRequiredPeriod",
                kind=MetaData.Type.UINT,
                description="Period in which a second request doesn't require a restart of a recently started rsync",
                default=10,
            )
        )
        self.meta.add(
            MetaDataField(
                name="minimalLoadForOffload",
                kind=MetaData.Type.FLOAT,
                description="Minimal provisioning load on the active head node before which dirty provisioning nodes are updated",
                default=0.25,
            )
        )
        self.meta.add(
            MetaDataField(
                name="headNodeLoadMultiplier",
                kind=MetaData.Type.FLOAT,
                description="Load multiplier to reduce the work for the head node and offload more to the provisioning nodes",
                default=0.25,
            )
        )
        self.meta.add(
            MetaDataField(
                name="useGNSSLocationData",
                kind=MetaData.Type.BOOL,
                description="Use GNSS location data where available to find and prefer the closest provisioning node",
                default=True,
            )
        )
        self.baseType = 'ProvisioningSettings'
        self.service_type = self.baseType
        self.allTypes = ['ProvisioningSettings']
        self.top_level = False
        self.leaf_entity = True

