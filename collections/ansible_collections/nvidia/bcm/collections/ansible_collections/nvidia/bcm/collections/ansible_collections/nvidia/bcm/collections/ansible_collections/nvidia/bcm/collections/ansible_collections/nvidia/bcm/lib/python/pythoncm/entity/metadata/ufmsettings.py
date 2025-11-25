from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class UFMSettings(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="server",
                kind=MetaData.Type.STRING,
                description="UFM server",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="username",
                kind=MetaData.Type.STRING,
                description="Username to use for UFM API calls",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="password",
                kind=MetaData.Type.STRING,
                description="Password to use for UFM API calls",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="port",
                kind=MetaData.Type.UINT,
                description="Port",
                default=443,
            )
        )
        self.meta.add(
            MetaDataField(
                name="verifySSL",
                kind=MetaData.Type.BOOL,
                description="Verify SSL host certificate",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cacert",
                kind=MetaData.Type.STRING,
                description="The CA certificate of the server",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="certificate",
                kind=MetaData.Type.STRING,
                description="The certificate used to connect to the server",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="privateKey",
                kind=MetaData.Type.STRING,
                description="The certificate private key used to connect to the server",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.RESOLVE,
                description="List of nodes that can be used as server",
                instance='Node',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="prometheusMetricForwarders",
                kind=MetaData.Type.ENTITY,
                description="Prometheus metric forwarders",
                instance='PrometheusMetricForwarder',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'UFMSettings'
        self.service_type = self.baseType
        self.allTypes = ['UFMSettings']
        self.top_level = False
        self.leaf_entity = True

