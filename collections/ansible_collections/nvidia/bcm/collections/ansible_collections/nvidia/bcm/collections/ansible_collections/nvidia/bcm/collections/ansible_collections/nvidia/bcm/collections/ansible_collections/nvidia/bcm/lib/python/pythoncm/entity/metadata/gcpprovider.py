from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudprovider import CloudProvider


class GCPProvider(CloudProvider):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="projectId",
                kind=MetaData.Type.STRING,
                description="GCP project ID",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultBootDiskType",
                kind=MetaData.Type.STRING,
                description="Default boot disk type. Used if bootDiskType in cloudsettings is empty.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultBootImageURI",
                kind=MetaData.Type.STRING,
                description="Default boot image URI. Used if bootImageURI in cloudsettings is empty.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultMachineType",
                kind=MetaData.Type.RESOLVE,
                description="Default machine type. Used if machineType in cloudsettings is empty.",
                instance='GCPMachineType',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultMaintenancePolicy",
                kind=MetaData.Type.STRING,
                description="Default maintenance policy. Used if maintenancePolicy in cloudsettings is empty.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultProvisioningModel",
                kind=MetaData.Type.STRING,
                description="Default provisioning model. Used if provisioningModel in cloudsettings is empty.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultReservationName",
                kind=MetaData.Type.STRING,
                description="Default reservation name. Used if reservationName in cloudsettings is empty.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultReservationType",
                kind=MetaData.Type.STRING,
                description="Default reservation type. Used if reservationType in cloudsettings is empty.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultResourcePolicies",
                kind=MetaData.Type.STRING,
                description="Default resource policies. Used if resourcePolicies in cloudsettings is empty.",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultServiceAccount",
                kind=MetaData.Type.STRING,
                description="Default service account. Used if serviceAccount in cloudsettings is empty.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultZone",
                kind=MetaData.Type.RESOLVE,
                description="Default zone. Used if zone in cloudsettings is empty.",
                instance='GCPZone',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="imageStorageLocation",
                kind=MetaData.Type.STRING,
                description="Storage location of newly created image resources. The location may be a GCP region or multiregion (e.g. 'eu').",
                default='',
            )
        )
        self.baseType = 'CloudProvider'
        self.childType = 'GCPProvider'
        self.service_type = self.baseType
        self.allTypes = ['GCPProvider', 'CloudProvider']
        self.top_level = True
        self.leaf_entity = True

