from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.node import Node


class ComputeNode(Node):
    class BootLoader(Enum):
        SYSLINUX = auto()
        GRUB = auto()
        CATEGORY = auto()

    class BootLoaderProtocol(Enum):
        TFTP = auto()
        HTTP = auto()
        HTTPS = auto()
        CATEGORY = auto()

    class FIPS(Enum):
        YES = auto()
        NO = auto()
        CATEGORY = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="installMode",
                kind=MetaData.Type.STRING,
                description="Installmode to be used by default, if empty use category installMode",
                options=[
                    '',
                    'AUTO',
                    'FULL',
                    'MAIN',
                    'NOSYNC',
                    'SKIP',
                ],
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="nextBootInstallMode",
                kind=MetaData.Type.STRING,
                description="Installmode to be used during the next boot, will be cleared during boot",
                options=[
                    '',
                    'AUTO',
                    'FULL',
                    'MAIN',
                    'NOSYNC',
                    'SKIP',
                ],
                diff_type=MetaDataField.Diff.none,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="blockDevicesClearedOnNextBoot",
                kind=MetaData.Type.STRING,
                description="List of block devices that will be cleared during the next boot",
                diff_type=MetaDataField.Diff.none,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="initialize",
                kind=MetaData.Type.STRING,
                description="Node specific initialize script",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="finalize",
                kind=MetaData.Type.STRING,
                description="Node specific finalize script",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="raidconf",
                kind=MetaData.Type.STRING,
                description="Node specific Hardware RAID configuration",
                function_check=MetaData.check_is_raid_configuration,
                diff_type=MetaDataField.Diff.xml,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="category",
                kind=MetaData.Type.RESOLVE,
                description="Category to which this node belongs",
                instance='Category',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disksetup",
                kind=MetaData.Type.STRING,
                description="Node specific disk setup",
                function_check=MetaData.check_is_disk_setup,
                diff_type=MetaDataField.Diff.xml,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeListFull",
                kind=MetaData.Type.STRING,
                description="Exclude list for full install",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeListSync",
                kind=MetaData.Type.STRING,
                description="Exclude list for sync install",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeListUpdate",
                kind=MetaData.Type.STRING,
                description="Exclude list for update",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeListGrab",
                kind=MetaData.Type.STRING,
                description="Exclude list for grabbing to an existing image",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeListGrabnew",
                kind=MetaData.Type.STRING,
                description="Exclude list for grabbing to a new image",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeInstallerDisk",
                kind=MetaData.Type.BOOL,
                description="The node has its own node installer disk",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="installBootRecord",
                kind=MetaData.Type.BOOL,
                description="Install boot record on local disk",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dataNode",
                kind=MetaData.Type.BOOL,
                description="If enabled the node will never do a FULL install without explicit user confirmation",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowNetworkingRestart",
                kind=MetaData.Type.BOOL,
                description="Allow node to update ifcfg files and restart networking",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="softwareImageProxy",
                kind=MetaData.Type.ENTITY,
                description="Software image used by node",
                instance='SoftwareImageProxy',
                entity_allow_null=True,
                default=None,
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
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="modules",
                kind=MetaData.Type.ENTITY,
                description="Manage kernel modules loaded in this node",
                instance='KernelModule',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="bootLoader",
                kind=MetaData.Type.ENUM,
                description="Boot loader",
                options=[
                    self.BootLoader.SYSLINUX,
                    self.BootLoader.GRUB,
                    self.BootLoader.CATEGORY,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.BootLoader,
                default=self.BootLoader.CATEGORY,
            )
        )
        self.meta.add(
            MetaDataField(
                name="bootLoaderProtocol",
                kind=MetaData.Type.ENUM,
                description="Boot loader protocol for retrieving initrd and vmlinuz",
                options=[
                    self.BootLoaderProtocol.TFTP,
                    self.BootLoaderProtocol.HTTP,
                    self.BootLoaderProtocol.CATEGORY,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.BootLoaderProtocol,
                default=self.BootLoaderProtocol.CATEGORY,
            )
        )
        self.meta.add(
            MetaDataField(
                name="bootLoaderFile",
                kind=MetaData.Type.STRING,
                description="Alternative boot loader file",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="fips",
                kind=MetaData.Type.ENUM,
                description="Federal Information Processing Standard Security Requirements",
                options=[
                    self.FIPS.YES,
                    self.FIPS.NO,
                    self.FIPS.CATEGORY,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.FIPS,
                default=self.FIPS.CATEGORY,
            )
        )
        self.meta.add(
            MetaDataField(
                name="templateNode",
                kind=MetaData.Type.BOOL,
                description="Indicate this is a template node and should not be powered on and booted",
                clone=False,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fromTemplateNode",
                kind=MetaData.Type.UUID,
                description="Indicate from which template node this node was copied",
                clone=False,
                default=self.zero_uuid,
            )
        )
        self.baseType = 'Device'
        self.childType = 'ComputeNode'
        self.service_type = self.baseType
        self.allTypes = ['ComputeNode', 'Node', 'Device']
        self.leaf_entity = False

