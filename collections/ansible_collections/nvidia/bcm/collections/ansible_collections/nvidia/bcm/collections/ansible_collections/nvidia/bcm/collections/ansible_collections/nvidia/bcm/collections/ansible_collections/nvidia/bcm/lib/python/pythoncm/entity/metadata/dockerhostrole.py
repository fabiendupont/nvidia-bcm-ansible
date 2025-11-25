from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class DockerHostRole(Role):
    """
    Role providing docker daemon and cli capability
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="spool",
                kind=MetaData.Type.STRING,
                description="Root of the Docker runtime",
                default="/var/lib/docker",
            )
        )
        self.meta.add(
            MetaDataField(
                name="tmpDir",
                kind=MetaData.Type.STRING,
                description="Location used for temporary files (token $spool is replaced to path to docker runtime root directory)",
                default="$spool/tmp",
            )
        )
        self.meta.add(
            MetaDataField(
                name="enableSelinux",
                kind=MetaData.Type.BOOL,
                description="Enable selinux support in docker daemon",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultUlimits",
                kind=MetaData.Type.STRING,
                description="Set the default ulimit options to use for all containers",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="debug",
                kind=MetaData.Type.BOOL,
                description="Enable debug mode",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="logLevel",
                kind=MetaData.Type.STRING,
                description="Set the logging level",
                options=[
                    '',
                    'debug',
                    'info',
                    'warn',
                    'error',
                    'fatal',
                ],
                default="info",
            )
        )
        self.meta.add(
            MetaDataField(
                name="bridgeIp",
                kind=MetaData.Type.STRING,
                description="Network bridge IP",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="bridge",
                kind=MetaData.Type.STRING,
                description="Attach containers to a network bridge",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="mtu",
                kind=MetaData.Type.UINT,
                description="Set the containers network MTU (in bytes)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="apiSockets",
                kind=MetaData.Type.STRING,
                description="Daemon socket(s) to connect to (-H docker daemon option)",
                vector=True,
                default=["unix:///var/run/docker.sock"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="iptables",
                kind=MetaData.Type.BOOL,
                description="Enable addition of iptables rules",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="userNamespaceRemap",
                kind=MetaData.Type.STRING,
                description="User/Group setting for user namespaces",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="insecureRegistries",
                kind=MetaData.Type.STRING,
                description="If you have a registry secured with https but do not have proper certs distributed, you can tell docker to not look for full authorization by adding the registry to this list. Accepted Format : CIDR or hostname:port",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="enableTls",
                kind=MetaData.Type.BOOL,
                description="Use TLS",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="verifyTls",
                kind=MetaData.Type.BOOL,
                description="Use TLS and verify the remote",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="tlsCa",
                kind=MetaData.Type.STRING,
                description="Trust certs signed only by this CA",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="tlsCertificate",
                kind=MetaData.Type.STRING,
                description="Path to TLS certificate file",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="tlsKey",
                kind=MetaData.Type.STRING,
                description="Path to TLS key file",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="certificatesPath",
                kind=MetaData.Type.STRING,
                description="Path to docker certificates",
                default="/etc/docker",
            )
        )
        self.meta.add(
            MetaDataField(
                name="storageBackends",
                kind=MetaData.Type.ENTITY,
                description="Docker storage backends",
                instance='DockerStorageBackend',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="containerdSocket",
                kind=MetaData.Type.STRING,
                description="Path to containerd socket",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="runtime",
                kind=MetaData.Type.STRING,
                description="Docker runtime",
                default="runc",
            )
        )
        self.meta.add(
            MetaDataField(
                name="options",
                kind=MetaData.Type.STRING,
                description="Additional parameters for docker daemon",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'DockerHostRole'
        self.service_type = self.baseType
        self.allTypes = ['DockerHostRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

