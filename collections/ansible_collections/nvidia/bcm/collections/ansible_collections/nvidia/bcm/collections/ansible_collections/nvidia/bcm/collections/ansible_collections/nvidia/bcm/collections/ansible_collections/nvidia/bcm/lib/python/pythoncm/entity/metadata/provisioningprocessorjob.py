from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ProvisioningProcessorJob(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="job_uuid",
                kind=MetaData.Type.UUID,
                description="Internal provisioning system job UUID.",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="request_uuid",
                kind=MetaData.Type.UUID,
                description="Provisioning request UUID.",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="source",
                kind=MetaData.Type.RESOLVE,
                description="Source node.",
                instance='Node',
                default=None,
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
                name="destination",
                kind=MetaData.Type.RESOLVE,
                description="Destination node.",
                instance='Node',
                default=None,
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
                name="isFromNodeInstaller",
                kind=MetaData.Type.BOOL,
                description="Set if the request came from the node-installer.",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="isBackupFromBackup",
                kind=MetaData.Type.BOOL,
                description="Set if the request came a backup of a backup.",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="userName",
                kind=MetaData.Type.STRING,
                description="Rsync username.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="password",
                kind=MetaData.Type.STRING,
                description="Rsync password.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="rsyncdPort",
                kind=MetaData.Type.UINT,
                description="Rsync port.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="includelist",
                kind=MetaData.Type.STRING,
                description="Rsync include list.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludelist",
                kind=MetaData.Type.STRING,
                description="Rsync exclude list.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="dryrun",
                kind=MetaData.Type.BOOL,
                description="If set, a dry run will be performed, no data is written.",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="syncMode",
                kind=MetaData.Type.UINT,
                description="Sync mode.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="state",
                kind=MetaData.Type.UINT,
                description="Job state.",
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
                description="Error details.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="fspart",
                kind=MetaData.Type.RESOLVE,
                description="FSPart",
                instance='FSPart',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="index",
                kind=MetaData.Type.UINT,
                description="Index",
                default=0,
            )
        )
        self.baseType = 'ProvisioningProcessorJob'
        self.service_type = self.baseType
        self.allTypes = ['ProvisioningProcessorJob']
        self.top_level = False
        self.leaf_entity = True

