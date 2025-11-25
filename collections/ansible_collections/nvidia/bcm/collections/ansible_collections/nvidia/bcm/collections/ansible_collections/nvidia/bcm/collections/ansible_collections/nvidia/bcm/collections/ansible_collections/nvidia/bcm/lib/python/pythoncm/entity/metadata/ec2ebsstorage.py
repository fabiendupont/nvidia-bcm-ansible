from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.ec2storage import EC2Storage


class EC2EBSStorage(EC2Storage):
    class VolumeType(Enum):
        ST1 = auto()
        SC1 = auto()
        STANDARD = auto()
        IO1 = auto()
        IO2 = auto()
        GP2 = auto()
        GP3 = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="volumeId",
                kind=MetaData.Type.STRING,
                description="Volume ID assigned by EC2 EC2",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="size",
                kind=MetaData.Type.UINT,
                description="Size",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="persistent",
                kind=MetaData.Type.BOOL,
                description="Persistent storage will not be removed when instance is removed",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="availabilityZone",
                kind=MetaData.Type.STRING,
                description="Availability zone set by EC2",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="creationTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Time of creation in EC2",
                readonly=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="status",
                kind=MetaData.Type.STRING,
                description="Status of EBS volume in EC2",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="volumeType",
                kind=MetaData.Type.ENUM,
                description="Specifies what type of EBS volume to use",
                options=[
                    self.VolumeType.ST1,
                    self.VolumeType.SC1,
                    self.VolumeType.STANDARD,
                    self.VolumeType.IO1,
                    self.VolumeType.IO2,
                    self.VolumeType.GP2,
                    self.VolumeType.GP3,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.VolumeType,
                default=self.VolumeType.GP2,
            )
        )
        self.meta.add(
            MetaDataField(
                name="iops",
                kind=MetaData.Type.UINT,
                description="Specifies the IOPS rate for the provisioned IOPS volume type",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="encrypted",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="snapshotId",
                kind=MetaData.Type.STRING,
                description="ID of the snapshot which should be used to instantiate the new disk. This field can be used to speed up node provisioning by first provisioning a cloud compute node, creating a snapshot of its volumes, and then setting that snapshot ID in this field for remaining cloud compute nodes.",
                default='',
            )
        )
        self.baseType = 'EC2Storage'
        self.childType = 'EC2EBSStorage'
        self.service_type = self.baseType
        self.allTypes = ['EC2EBSStorage', 'EC2Storage']
        self.top_level = False
        self.leaf_entity = True

