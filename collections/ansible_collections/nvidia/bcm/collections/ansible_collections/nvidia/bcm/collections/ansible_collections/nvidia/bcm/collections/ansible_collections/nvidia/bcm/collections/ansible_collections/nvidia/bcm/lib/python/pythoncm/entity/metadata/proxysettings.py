from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ProxySettings(Entity):
    """
    Proxy server settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="proxyHttp",
                kind=MetaData.Type.STRING,
                description="HTTP proxy address which will be used for the node connections to HTTP resources",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="proxyHttpUser",
                kind=MetaData.Type.STRING,
                description="HTTP proxy username for authentication",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="proxyHttpPass",
                kind=MetaData.Type.STRING,
                description="HTTP proxy password for authentication",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="proxyHttps",
                kind=MetaData.Type.STRING,
                description="HTTPS proxy address which will be used for the node connections to HTTPS resources",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="proxyHttpsUser",
                kind=MetaData.Type.STRING,
                description="HTTPS proxy username for authentication",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="proxyHttpsPass",
                kind=MetaData.Type.STRING,
                description="HTTPS proxy password for authentication",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="proxyFtp",
                kind=MetaData.Type.STRING,
                description="FTP proxy address which will be used for the node connections to FTP resources",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="proxyFtpUser",
                kind=MetaData.Type.STRING,
                description="FTP proxy username for authentication",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="proxyFtpPass",
                kind=MetaData.Type.STRING,
                description="FTP proxy password for authentication",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="noProxy",
                kind=MetaData.Type.STRING,
                description="Hosts to be accessed without proxy",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'ProxySettings'
        self.service_type = self.baseType
        self.allTypes = ['ProxySettings']
        self.top_level = False
        self.leaf_entity = True

