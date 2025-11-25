from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class NetworkConnection(Entity):
    class Type(Enum):
        TCP = auto()
        UDP = auto()
        TCP6 = auto()
        UDP6 = auto()

    class State(Enum):
        UNDEFINED = auto()
        TCP_ESTABLISHED = auto()
        TCP_SYN_SENT = auto()
        TCP_SYN_RECV = auto()
        TCP_FIN_WAIT1 = auto()
        TCP_FIN_WAIT2 = auto()
        TCP_TIME_WAIT = auto()
        TCP_CLOSE = auto()
        TCP_CLOSE_WAIT = auto()
        TCP_LAST_ACK = auto()
        TCP_LISTEN = auto()
        TCP_CLOSING = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_node_uuid",
                kind=MetaData.Type.UUID,
                description="Node",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="source",
                kind=MetaData.Type.STRING,
                description="The source IP address",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="sourcePort",
                kind=MetaData.Type.UINT,
                description="The source port",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="destination",
                kind=MetaData.Type.STRING,
                description="The destination IP address",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="destinationPort",
                kind=MetaData.Type.UINT,
                description="The destination port",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="type",
                kind=MetaData.Type.ENUM,
                description="The connection type",
                options=[
                    self.Type.TCP,
                    self.Type.UDP,
                    self.Type.TCP6,
                    self.Type.UDP6,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Type,
                default=self.Type.TCP,
            )
        )
        self.meta.add(
            MetaDataField(
                name="state",
                kind=MetaData.Type.ENUM,
                description="The connection state",
                options=[
                    self.State.UNDEFINED,
                    self.State.TCP_ESTABLISHED,
                    self.State.TCP_SYN_SENT,
                    self.State.TCP_SYN_RECV,
                    self.State.TCP_FIN_WAIT1,
                    self.State.TCP_FIN_WAIT2,
                    self.State.TCP_TIME_WAIT,
                    self.State.TCP_CLOSE,
                    self.State.TCP_CLOSE_WAIT,
                    self.State.TCP_LAST_ACK,
                    self.State.TCP_LISTEN,
                    self.State.TCP_CLOSING,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.State,
                default=self.State.UNDEFINED,
            )
        )
        self.baseType = 'NetworkConnection'
        self.service_type = self.baseType
        self.allTypes = ['NetworkConnection']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

