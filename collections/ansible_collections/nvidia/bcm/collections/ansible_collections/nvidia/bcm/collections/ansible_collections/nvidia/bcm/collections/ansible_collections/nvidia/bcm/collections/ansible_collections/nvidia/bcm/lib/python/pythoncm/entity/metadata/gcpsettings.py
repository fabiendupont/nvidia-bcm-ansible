from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudsettings import CloudSettings


class GCPSettings(CloudSettings):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="instanceId",
                kind=MetaData.Type.STRING,
                description="Instance ID in GCP",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="bootDiskType",
                kind=MetaData.Type.STRING,
                description="Disk type of the boot disk. The default is pd-standard.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="bootImageURI",
                kind=MetaData.Type.STRING,
                description="URI of boot image. Specify either a cloud storage directory, blob, or image resource.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="machineType",
                kind=MetaData.Type.RESOLVE,
                description="Machine type of the instance.",
                instance='GCPMachineType',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maintenancePolicy",
                kind=MetaData.Type.STRING,
                description="Host maintenance policy of the instance (MIGRATE, TERMINATE).",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="provisioningModel",
                kind=MetaData.Type.STRING,
                description="Provisioning model of the instance (UNDEFINED_PROVISIONING_MODEL, STANDARD, SPOT, RESERVATION_BOUND).",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="reservationName",
                kind=MetaData.Type.STRING,
                description="Reservation name to use if the reservation type is set to SPECIFIC_RESERVATION. This can be either a name to a reservation in the same project or 'projects/different-project/reservations/some-reservation-name' to target a shared reservation in the same zone but in a different project.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="reservationType",
                kind=MetaData.Type.STRING,
                description="Reservation type (ANY_RESERVATION, SPECIFIC_RESERVATION, NO_RESERVATION).",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="resourcePolicies",
                kind=MetaData.Type.STRING,
                description="Resource policies applied to this instance.",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="serviceAccount",
                kind=MetaData.Type.STRING,
                description="Email address of the service account.",
                function_check=MetaData.check_isEmail,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="zone",
                kind=MetaData.Type.RESOLVE,
                description="Instance zone",
                instance='GCPZone',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disks",
                kind=MetaData.Type.ENTITY,
                description="Storage disks.",
                instance='GCPDisk',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'CloudSettings'
        self.childType = 'GCPSettings'
        self.service_type = self.baseType
        self.allTypes = ['GCPSettings', 'CloudSettings']
        self.top_level = False
        self.leaf_entity = True

