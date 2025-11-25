from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.role import Role


class PRSServerRole(Role):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="configServerPort",
                kind=MetaData.Type.UINT,
                description="Port for the PRS config service",
                default=8880,
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobSchedulerServerPort",
                kind=MetaData.Type.UINT,
                description="Port for the job scheduler serverv",
                default=8881,
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeout",
                kind=MetaData.Type.UINT,
                description="Service pythoncm RPC timeout",
                default=10,
            )
        )
        self.meta.add(
            MetaDataField(
                name="interval",
                kind=MetaData.Type.UINT,
                description="Service loop interval",
                default=30,
            )
        )
        self.meta.add(
            MetaDataField(
                name="window",
                kind=MetaData.Type.UINT,
                description="Number of samples in the history taken into account",
                default=5,
            )
        )
        self.meta.add(
            MetaDataField(
                name="serverCertificatePath",
                kind=MetaData.Type.STRING,
                description="PRS certificate path for the web server",
                default="/cm/local/apps/prs/etc/server.pem",
            )
        )
        self.meta.add(
            MetaDataField(
                name="serverPrivateKeyPath",
                kind=MetaData.Type.STRING,
                description="PRS private key path for the web server",
                default="/cm/local/apps/prs/etc/server.key",
            )
        )
        self.meta.add(
            MetaDataField(
                name="serverCACertificatePath",
                kind=MetaData.Type.STRING,
                description="CA certificate path",
                default="/cm/local/apps/prs/etc/ca.pem",
            )
        )
        self.meta.add(
            MetaDataField(
                name="serverCAPrivateKeyPath",
                kind=MetaData.Type.STRING,
                description="CA certificate path",
                default="/cm/local/apps/prs/etc/ca.key",
            )
        )
        self.meta.add(
            MetaDataField(
                name="cmdCertificatePath",
                kind=MetaData.Type.STRING,
                description="Certificate path for CMD to call the PRS server",
                default="/cm/local/apps/prs/etc/cmd.pem",
            )
        )
        self.meta.add(
            MetaDataField(
                name="cmdPrivateKeyPath",
                kind=MetaData.Type.STRING,
                description="Private key path for CMD to call the PRS server",
                default="/cm/local/apps/prs/etc/cmd.key",
            )
        )
        self.meta.add(
            MetaDataField(
                name="clientCertificatePath",
                kind=MetaData.Type.STRING,
                description="PRS client certificate path to call CMD",
                default="/cm/local/apps/prs/etc/prs.pem",
            )
        )
        self.meta.add(
            MetaDataField(
                name="clientPrivateKeyPath",
                kind=MetaData.Type.STRING,
                description="PRS client private key path to call CMD",
                default="/cm/local/apps/prs/etc/prs.key",
            )
        )
        self.meta.add(
            MetaDataField(
                name="clientCACertificatePath",
                kind=MetaData.Type.STRING,
                description="CA certificate path of CMD",
                default="/cm/local/apps/cmd/pythoncm/lib/python3.12/site-packages/pythoncm/etc/cacert.pem",
            )
        )
        self.meta.add(
            MetaDataField(
                name="domains",
                kind=MetaData.Type.ENTITY,
                description="Domains",
                instance='PRSDomain',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Role'
        self.childType = 'PRSServerRole'
        self.service_type = self.baseType
        self.allTypes = ['PRSServerRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

