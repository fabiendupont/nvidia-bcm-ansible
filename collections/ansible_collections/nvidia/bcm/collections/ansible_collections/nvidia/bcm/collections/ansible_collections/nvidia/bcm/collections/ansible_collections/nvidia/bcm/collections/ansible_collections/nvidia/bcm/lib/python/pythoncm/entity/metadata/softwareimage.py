from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SoftwareImage(Entity):
    """
    Software image
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="path",
                kind=MetaData.Type.STRING,
                description="Base directory of the image",
                regex_check=r"^(/[-+_.a-zA-Z0-9]+)+/?(@\d+)?$",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="originalImage",
                kind=MetaData.Type.UUID,
                description="Image from which this one will be cloned",
                diff_type=MetaDataField.Diff.none,
                internal=True,
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fileOperationInProgress",
                kind=MetaData.Type.BOOL,
                diff_type=MetaDataField.Diff.none,
                internal=True,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="kernelVersion",
                kind=MetaData.Type.STRING,
                description="Kernel version used",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="kernelParameters",
                kind=MetaData.Type.STRING,
                description="Kernel parameters passed to the kernel at boot time",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="kernelOutputConsole",
                kind=MetaData.Type.STRING,
                description="Kernel output console used at boot time",
                default="tty0",
            )
        )
        self.meta.add(
            MetaDataField(
                name="creationTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Creation time",
                readonly=True,
                clone=False,
                diff_type=MetaDataField.Diff.none,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="modules",
                kind=MetaData.Type.ENTITY,
                description="Manage kernel modules loaded in this image",
                instance='KernelModule',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="enableSOL",
                kind=MetaData.Type.BOOL,
                description="Enable Serial console Over LAN",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="SOLPort",
                kind=MetaData.Type.STRING,
                description="Serial port to use for SOL, usually ttyS0 or ttyS1",
                default="ttyS1",
            )
        )
        self.meta.add(
            MetaDataField(
                name="SOLSpeed",
                kind=MetaData.Type.STRING,
                description="Baud rate to use for SOL",
                options=[
                    '115200',
                    '57600',
                    '38400',
                    '19200',
                    '9600',
                    '4800',
                    '2400',
                    '1200',
                ],
                default="115200",
            )
        )
        self.meta.add(
            MetaDataField(
                name="SOLFlowControl",
                kind=MetaData.Type.BOOL,
                description="Enable to use hardware flow control for SOL",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="notes",
                kind=MetaData.Type.STRING,
                description="Administrator notes",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="fspart",
                kind=MetaData.Type.RESOLVE,
                description="Internal pointer to the FSPart associated with this image",
                clone=False,
                internal=True,
                instance='FSPart',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="bootfspart",
                kind=MetaData.Type.RESOLVE,
                description="Internal pointer to the FSPart associated with the boot directory of this image",
                clone=False,
                internal=True,
                instance='FSPart',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="revisionID",
                kind=MetaData.Type.INT,
                clone=False,
                diff_type=MetaDataField.Diff.none,
                internal=True,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="parentSoftwareImage",
                kind=MetaData.Type.RESOLVE,
                clone=False,
                internal=True,
                instance='SoftwareImage',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="revisionHistory",
                kind=MetaData.Type.ENTITY,
                clone=False,
                diff_type=MetaDataField.Diff.none,
                internal=True,
                instance='SoftwareImageRevisionInfo',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'SoftwareImage'
        self.service_type = self.baseType
        self.allTypes = ['SoftwareImage']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

