from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class LicenseInfo(Entity):
    """
    License info
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_partition_uuid",
                kind=MetaData.Type.UUID,
                description="Partition",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="macAddress",
                kind=MetaData.Type.STRING,
                description="MAC address linked to the license",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="licensedNodes",
                kind=MetaData.Type.UINT,
                description="License count",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="licensedBurstNodes",
                kind=MetaData.Type.INT,
                description="Number of ondemand nodes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="version",
                kind=MetaData.Type.STRING,
                description="Version",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="edition",
                kind=MetaData.Type.STRING,
                description="Edition",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="startTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Time from which the license is active",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="endTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Time at which the license stops being valid",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="serial",
                kind=MetaData.Type.INT,
                description="Serial",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="licensee",
                kind=MetaData.Type.STRING,
                description="Licensee",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeCount",
                kind=MetaData.Type.UINT,
                description="Nodes count with a MAC / cloud-identifier set",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="acceleratorCount",
                kind=MetaData.Type.UINT,
                description="Accelerators count inside nodes with a MAC / cloud-identifier set",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="burstNodeCount",
                kind=MetaData.Type.UINT,
                description="Bursted nodes count",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="accountingAndReporting",
                kind=MetaData.Type.BOOL,
                description="Accounting and reporting enabled/disabled",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="edgeSites",
                kind=MetaData.Type.BOOL,
                description="Edge sites enabled/disabled",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="message",
                kind=MetaData.Type.STRING,
                description="License count message",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="licenseType",
                kind=MetaData.Type.STRING,
                description="License type",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="information",
                kind=MetaData.Type.JSON,
                description="Information",
                default=None,
            )
        )
        self.baseType = 'LicenseInfo'
        self.service_type = self.baseType
        self.allTypes = ['LicenseInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

