from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class FirewallOpenPort(Entity):
    class Action(Enum):
        ACCEPT = auto()
        DNAT = auto()
        DROP = auto()
        REJECT = auto()

    class Protocol(Enum):
        Any = auto()
        TCP = auto()
        UDP = auto()
        ICMP = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="action",
                kind=MetaData.Type.ENUM,
                description="Specifies the action to be taken if the connection request matches the rule",
                options=[
                    self.Action.ACCEPT,
                    self.Action.DNAT,
                    self.Action.DROP,
                    self.Action.REJECT,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Action,
                default=self.Action.ACCEPT,
            )
        )
        self.meta.add(
            MetaDataField(
                name="network",
                kind=MetaData.Type.STRING,
                description="Network",
                default="net",
            )
        )
        self.meta.add(
            MetaDataField(
                name="port",
                kind=MetaData.Type.UINT,
                description="Port",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="count",
                kind=MetaData.Type.UINT,
                description="Number of ports starting from port",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="protocol",
                kind=MetaData.Type.ENUM,
                description="Protocol, any implies TCP and UDP",
                options=[
                    self.Protocol.Any,
                    self.Protocol.TCP,
                    self.Protocol.UDP,
                    self.Protocol.ICMP,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Protocol,
                default=self.Protocol.Any,
            )
        )
        self.meta.add(
            MetaDataField(
                name="address",
                kind=MetaData.Type.STRING,
                description="Network Address",
                function_check=MetaData.check_isCIDR,
                default="0.0.0.0/0",
            )
        )
        self.meta.add(
            MetaDataField(
                name="destination",
                kind=MetaData.Type.STRING,
                description="Destination hosts to which the rule applies",
                default="fw",
            )
        )
        self.meta.add(
            MetaDataField(
                name="description",
                kind=MetaData.Type.STRING,
                description="Description",
                default="",
            )
        )
        self.baseType = 'FirewallOpenPort'
        self.service_type = self.baseType
        self.allTypes = ['FirewallOpenPort']
        self.top_level = False
        self.leaf_entity = True

