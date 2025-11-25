from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.device import Device


class Node(Device):
    class ProvisioningTransport(Enum):
        RSYNCSSH = auto()
        RSYNCDAEMON = auto()

    class AuthenticationService(Enum):
        AUTO = auto()
        SSSD = auto()
        NSLCD = auto()
        CATEGORY = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="cmdaemonUrl",
                kind=MetaData.Type.STRING,
                clone=False,
                default="",
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
                name="pxelabel",
                kind=MetaData.Type.STRING,
                description="PXE Label to be displayed when this node boots",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="customRemoteConsoleScript",
                kind=MetaData.Type.STRING,
                description="Script that will be used to remote console a device",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="customRemoteConsoleScriptArgument",
                kind=MetaData.Type.STRING,
                description="Argument for the custom remote console script",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="provisioningTransport",
                kind=MetaData.Type.ENUM,
                description="Defines what transport protocol should be used for provisioning. Options are RSYNCSSH or RSYNCDAEMON. The latter is the default, is a bit less secure but faster.",
                options=[
                    self.ProvisioningTransport.RSYNCSSH,
                    self.ProvisioningTransport.RSYNCDAEMON,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.ProvisioningTransport,
                default=self.ProvisioningTransport.RSYNCDAEMON,
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
                name="versionConfigFiles",
                kind=MetaData.Type.BOOL,
                description="Keep old versions of all config files for this node",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="forceFullEnvironment",
                kind=MetaData.Type.BOOL,
                description="Force this node to create the environment for all nodes",
                default=False,
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
                    self.AuthenticationService.CATEGORY,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.AuthenticationService,
                default=self.AuthenticationService.CATEGORY,
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
                name="timeZoneSettings",
                kind=MetaData.Type.ENTITY,
                description="Time zone",
                instance='TimeZoneSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.baseType = 'Device'
        self.childType = 'Node'
        self.service_type = self.baseType
        self.allTypes = ['Node', 'Device']
        self.leaf_entity = False

