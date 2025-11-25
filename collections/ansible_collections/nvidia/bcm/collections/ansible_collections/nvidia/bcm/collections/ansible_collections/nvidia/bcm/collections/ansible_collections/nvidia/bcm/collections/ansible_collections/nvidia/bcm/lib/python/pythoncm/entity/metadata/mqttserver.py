from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MQTTServer(Entity):
    class Transport(Enum):
        TCP = auto()
        WEBSOCKETS = auto()

    class Protocol(Enum):
        V311 = auto()
        V5 = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="server",
                kind=MetaData.Type.STRING,
                description="Server",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="port",
                kind=MetaData.Type.UINT,
                description="Port",
                default=1883,
            )
        )
        self.meta.add(
            MetaDataField(
                name="topic",
                kind=MetaData.Type.STRING,
                description="Server",
                default="BCM/#",
            )
        )
        self.meta.add(
            MetaDataField(
                name="disabled",
                kind=MetaData.Type.BOOL,
                description="Disabled",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="username",
                kind=MetaData.Type.STRING,
                description="Username",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="password",
                kind=MetaData.Type.STRING,
                description="Password",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="transport",
                kind=MetaData.Type.ENUM,
                description="Transport",
                options=[
                    self.Transport.TCP,
                    self.Transport.WEBSOCKETS,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Transport,
                default=self.Transport.TCP,
            )
        )
        self.meta.add(
            MetaDataField(
                name="protocol",
                kind=MetaData.Type.ENUM,
                description="Protocol",
                options=[
                    self.Protocol.V311,
                    self.Protocol.V5,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Protocol,
                default=self.Protocol.V311,
            )
        )
        self.meta.add(
            MetaDataField(
                name="certRequired",
                kind=MetaData.Type.BOOL,
                description="Server certificate required",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="checkHostname",
                kind=MetaData.Type.BOOL,
                description="Check hostname",
                default=True,
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
        self.baseType = 'MQTTServer'
        self.service_type = self.baseType
        self.allTypes = ['MQTTServer']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'server'

