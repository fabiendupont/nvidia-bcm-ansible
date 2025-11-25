from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.cloudtype import CloudType


class GCPMachineType(CloudType):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="architecture",
                kind=MetaData.Type.STRING,
                description="CPU Architecture.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="isSharedCPU",
                kind=MetaData.Type.BOOL,
                description="Whether this machine type has a shared CPU.",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maximumPersistentDisksSizeGb",
                kind=MetaData.Type.UINT,
                description="Maximum total persistent disks size (GB) allowed.",
                default=0,
            )
        )
        self.baseType = 'CloudType'
        self.childType = 'GCPMachineType'
        self.service_type = self.baseType
        self.allTypes = ['GCPMachineType', 'CloudType']
        self.top_level = True
        self.leaf_entity = True
        self.allow_commit = False

