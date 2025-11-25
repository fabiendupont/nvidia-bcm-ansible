from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class JupyterHubRole(Role):
    """
    JupyterHub service
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="version",
                kind=MetaData.Type.STRING,
                description="JupyterHub version",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="port",
                kind=MetaData.Type.UINT,
                description="Port for proxy (JupyterHub.port)",
                default=8000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hubPort",
                kind=MetaData.Type.UINT,
                description="Port for hub (JupyterHub.hub_port)",
                default=8082,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hubIp",
                kind=MetaData.Type.STRING,
                description="The ip address or hostname for the Hub process to bind to (JupyterHub.hub_ip)",
                default="0.0.0.0",
            )
        )
        self.meta.add(
            MetaDataField(
                name="proxyApiUrl",
                kind=MetaData.Type.STRING,
                description="The URL which the hub uses to connect to the proxy's API (c.ConfigurableHTTPProxy.api_url)",
                default="http://127.0.0.1:8902",
            )
        )
        self.meta.add(
            MetaDataField(
                name="dataFilesPath",
                kind=MetaData.Type.STRING,
                description="The location of jupyterhub data files (JupyterHub.data_files_path)",
                default="/cm/shared/apps/jupyter/current/share/jupyterhub",
            )
        )
        self.meta.add(
            MetaDataField(
                name="pamOpenSessions",
                kind=MetaData.Type.BOOL,
                description="Enable SSL communication with HTTPS (PAMAuthenticator.open_sessions)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ca",
                kind=MetaData.Type.STRING,
                description="Filename containing the PEM-encoded certificate used for the Certification authority (CA) ",
                default="/cm/local/apps/jupyter/conf/certs/my_sslca.cert",
            )
        )
        self.meta.add(
            MetaDataField(
                name="cakey",
                kind=MetaData.Type.STRING,
                description="Filename containing the corresponding PEM-encoded private key used for the Certification authority (CA)",
                default="/cm/local/apps/jupyter/conf/certs/my_sslca.key",
            )
        )
        self.meta.add(
            MetaDataField(
                name="cert",
                kind=MetaData.Type.STRING,
                description="Path to the ssl certificate file (JupyterHub.ssl_cert)",
                default="/cm/local/apps/jupyter/conf/certs/my_ssl.cert",
            )
        )
        self.meta.add(
            MetaDataField(
                name="key",
                kind=MetaData.Type.STRING,
                description="Path to the ssl key file (JupyterHub.ssl_key)",
                default="/cm/local/apps/jupyter/conf/certs/my_ssl.key",
            )
        )
        self.meta.add(
            MetaDataField(
                name="adminUsers",
                kind=MetaData.Type.STRING,
                description="User with administrator privileges (Authenticator.admin_users)",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="userForService",
                kind=MetaData.Type.STRING,
                description="User for running cm-jupyterhub service (defined as User in /usr/lib/systemd/system/cm-jupyterhub.service)",
                default="root",
            )
        )
        self.meta.add(
            MetaDataField(
                name="trustedDomains",
                kind=MetaData.Type.STRING,
                description="Trusted domains to be included in JupyterHub certificates as Alt Subjects.",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="configs",
                kind=MetaData.Type.ENTITY,
                description="Configuration options JupyterHub",
                instance='JupyterHubConfig',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'JupyterHubRole'
        self.service_type = self.baseType
        self.allTypes = ['JupyterHubRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

