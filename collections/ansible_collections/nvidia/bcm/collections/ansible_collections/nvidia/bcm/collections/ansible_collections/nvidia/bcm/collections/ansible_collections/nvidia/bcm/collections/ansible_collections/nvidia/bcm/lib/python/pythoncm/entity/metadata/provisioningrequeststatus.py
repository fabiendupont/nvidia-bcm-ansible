from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ProvisioningRequestStatus(Entity):
    """
    Provisioning request status
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="request_uuids",
                kind=MetaData.Type.UUID,
                description="Provisioning request UUIDs.",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="sourceNode",
                kind=MetaData.Type.UUID,
                description="Source node handling the provisioning request.",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="sourcePath",
                kind=MetaData.Type.STRING,
                description="Path on the source node.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="destinationNode",
                kind=MetaData.Type.UUID,
                description="Destination node for the provisioning request.",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="destinationPath",
                kind=MetaData.Type.STRING,
                description="Path on the destination node.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="dryRun",
                kind=MetaData.Type.BOOL,
                description="In dry-run mode no data is actually written. See provisioning log for results.",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="syncMode",
                kind=MetaData.Type.UINT,
                description="Sync mode used for the provisioning request.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="state",
                kind=MetaData.Type.UINT,
                description="State of the provisioning request.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="errorMessage",
                kind=MetaData.Type.STRING,
                description="Error message.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="errorDetails",
                kind=MetaData.Type.STRING,
                description="Detailed error message.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobFailureCounter",
                kind=MetaData.Type.UINT,
                description="Number of times the provisioning job has failed.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="isFromNodeInstaller",
                kind=MetaData.Type.BOOL,
                description="Set if the request came from the node-installer.",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="requesterSessions",
                kind=MetaData.Type.UUID,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="schedulerInfo",
                kind=MetaData.Type.STRING,
                description="Details on how the provisioning request was scheduled.",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'ProvisioningRequestStatus'
        self.service_type = self.baseType
        self.allTypes = ['ProvisioningRequestStatus']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

