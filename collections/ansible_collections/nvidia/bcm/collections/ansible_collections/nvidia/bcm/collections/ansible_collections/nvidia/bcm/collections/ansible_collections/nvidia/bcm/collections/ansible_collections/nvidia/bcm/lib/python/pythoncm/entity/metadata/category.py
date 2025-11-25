from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Category(Entity):
    class InteractiveUser(Enum):
        ALWAYS = auto()
        ONLYWHENJOB = auto()
        NEVER = auto()

    class BootLoader(Enum):
        SYSLINUX = auto()
        GRUB = auto()

    class BootLoaderProtocol(Enum):
        TFTP = auto()
        HTTP = auto()
        HTTPS = auto()

    class FIPS(Enum):
        YES = auto()
        NO = auto()

    class AuthenticationService(Enum):
        AUTO = auto()
        SSSD = auto()
        NSLCD = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name of category",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="fsmounts",
                kind=MetaData.Type.ENTITY,
                description="Configure the entries placed in /etc/fstab",
                instance='FSMount',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="staticRoutes",
                kind=MetaData.Type.ENTITY,
                description="Configure static routes for the interfaces",
                instance='StaticRoute',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="roles",
                kind=MetaData.Type.ENTITY,
                description="Assign the roles the node should play",
                instance='Role',
                vector=True,
                default=[],
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
                name="gpuSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the GPUs",
                instance='GPUSettings',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="softwareImageProxy",
                kind=MetaData.Type.ENTITY,
                description="Software image the category will use",
                instance='SoftwareImageProxy',
                create_instance=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultGateway",
                kind=MetaData.Type.STRING,
                description="Default gateway for the category",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultGatewayMetric",
                kind=MetaData.Type.UINT,
                description="Default gateway metric",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nameServers",
                kind=MetaData.Type.STRING,
                description="List of name servers the category will use",
                function_check=MetaData.check_isIPv4or6,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeServers",
                kind=MetaData.Type.STRING,
                description="List of time servers the category will use",
                function_check=MetaData.check_isIPv4or6orHostname,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="searchDomains",
                kind=MetaData.Type.STRING,
                description="Search domains for the category",
                function_check=MetaData.check_isDomainWithIndex,
                vector=True,
                default=[],
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
                name="biosSetup",
                kind=MetaData.Type.JSON,
                description="BIOS setup",
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="installMode",
                kind=MetaData.Type.STRING,
                description="Installmode to be used by default, if none is specified in the node",
                options=[
                    'AUTO',
                    'FULL',
                    'MAIN',
                    'NOSYNC',
                    'SKIP',
                ],
                default="AUTO",
            )
        )
        self.meta.add(
            MetaDataField(
                name="newNodeInstallMode",
                kind=MetaData.Type.STRING,
                description="Installmode to be used by default, for new nodes",
                options=[
                    'AUTO',
                    'FULL',
                    'MAIN',
                    'NOSYNC',
                ],
                default="FULL",
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
                name="initialize",
                kind=MetaData.Type.STRING,
                description="Initialize script to be used for category",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="finalize",
                kind=MetaData.Type.STRING,
                description="Finalize script to be used for category",
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
                name="fsexports",
                kind=MetaData.Type.ENTITY,
                description="Configure the entries placed in /etc/exports",
                instance='FSExport',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="services",
                kind=MetaData.Type.ENTITY,
                description="Manage operating system services",
                instance='OSServiceConfig',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="bmcSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the baseboard management controller settings",
                instance='BMCSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="seLinuxSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the SELinux settings",
                instance='SELinuxSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dpuSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the DPU settings",
                instance='DPUSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="proxySettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the proxy server settings",
                instance='ProxySettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="accessSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the cluster wide Access settings",
                instance='AccessSettings',
                entity_allow_null=True,
                default=None,
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
                name="managementNetwork",
                kind=MetaData.Type.RESOLVE,
                description="Determines what network should be used for management traffic. If not set, partition setting is used.",
                instance='Network',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="interactiveUser",
                kind=MetaData.Type.ENUM,
                description="Allow user login on node",
                options=[
                    self.InteractiveUser.ALWAYS,
                    self.InteractiveUser.ONLYWHENJOB,
                    self.InteractiveUser.NEVER,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.InteractiveUser,
                default=self.InteractiveUser.ALWAYS,
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
                description="Allow nodes to update ifcfg files and restart networking",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeListManipulateScript",
                kind=MetaData.Type.STRING,
                description="A user defined script that can be used to do custom last minute changes to the exclude lists used by cmdaemon to rsync",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ioScheduler",
                kind=MetaData.Type.STRING,
                description="The I/O scheduler for the disks",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="useExclusivelyFor",
                kind=MetaData.Type.STRING,
                description="Use node exclusively for desired function: stop all other services",
                options=[
                    '',
                    'HPC',
                    'Nothing',
                ],
                default='',
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
                description="Manage kernel modules loaded in this image",
                instance='KernelModule',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="versionConfigFiles",
                kind=MetaData.Type.BOOL,
                description="Keep old versions of all config files for all nodes in this category",
                default=False,
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
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.BootLoader,
                default=self.BootLoader.SYSLINUX,
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
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.BootLoaderProtocol,
                default=self.BootLoaderProtocol.HTTP,
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
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.FIPS,
                default=self.FIPS.NO,
            )
        )
        self.meta.add(
            MetaDataField(
                name="authenticationService",
                kind=MetaData.Type.ENUM,
                description="Authentication service",
                options=[
                    self.AuthenticationService.AUTO,
                    self.AuthenticationService.SSSD,
                    self.AuthenticationService.NSLCD,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.AuthenticationService,
                default=self.AuthenticationService.AUTO,
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeZoneSettings",
                kind=MetaData.Type.ENTITY,
                description="Time zone",
                instance='TimeZoneSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ztpSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the ZTP settings",
                instance='ZTPSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.baseType = 'Category'
        self.service_type = self.baseType
        self.allTypes = ['Category']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

