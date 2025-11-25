from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class FSMount(Entity):
    """
    Filesystem mount
    """
    class FileSystemCheck(Enum):
        NONE = auto()
        ROOT = auto()
        OTHER = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="device",
                kind=MetaData.Type.STRING,
                description="What to mount.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mountpoint",
                kind=MetaData.Type.STRING,
                description="Where to mount.",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="filesystem",
                kind=MetaData.Type.STRING,
                description="The file system type.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mountoptions",
                kind=MetaData.Type.STRING,
                description="What options to use for mounting.",
                default="defaults",
            )
        )
        self.meta.add(
            MetaDataField(
                name="dump",
                kind=MetaData.Type.BOOL,
                description="Dump field in fstab, see man fstab.",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fsck",
                kind=MetaData.Type.ENUM,
                description="Filesystem check field in fstab, see man fstab.",
                options=[
                    self.FileSystemCheck.NONE,
                    self.FileSystemCheck.ROOT,
                    self.FileSystemCheck.OTHER,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.FileSystemCheck,
                default=self.FileSystemCheck.NONE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rdma",
                kind=MetaData.Type.BOOL,
                description="Enable NFS over RDMA.",
                default=False,
            )
        )
        self.baseType = 'FSMount'
        self.service_type = self.baseType
        self.allTypes = ['FSMount']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'mountpoint'

