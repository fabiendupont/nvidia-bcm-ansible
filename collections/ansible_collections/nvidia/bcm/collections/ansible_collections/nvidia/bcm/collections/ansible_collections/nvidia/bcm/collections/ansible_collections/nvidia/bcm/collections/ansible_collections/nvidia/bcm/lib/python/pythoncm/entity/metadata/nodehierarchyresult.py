from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class NodeHierarchyResult(Entity):
    class Responsibility(Enum):
        LDAP = auto()
        BIOS = auto()
        DHCP = auto()
        DNS = auto()
        NTP = auto()
        VPN = auto()
        RSYSLOG = auto()
        PROVISIONING = auto()
        DIRECTOR = auto()
        MOUNT = auto()
        SSH_PROXY = auto()
        CMDAEMON_CONFIGURATION = auto()
        CMDAEMON_RPC_FORWARD = auto()
        CMDAEMON_EVENTS = auto()
        CMDAEMON_STATUS = auto()
        CMDAEMON_WEB_SOCKET = auto()
        MONITORING_OFFLOAD = auto()
        UNDEFINED = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="responsibility",
                kind=MetaData.Type.ENUM,
                description="Responsibility",
                options=[
                    self.Responsibility.LDAP,
                    self.Responsibility.BIOS,
                    self.Responsibility.DHCP,
                    self.Responsibility.DNS,
                    self.Responsibility.NTP,
                    self.Responsibility.VPN,
                    self.Responsibility.RSYSLOG,
                    self.Responsibility.PROVISIONING,
                    self.Responsibility.DIRECTOR,
                    self.Responsibility.MOUNT,
                    self.Responsibility.SSH_PROXY,
                    self.Responsibility.CMDAEMON_CONFIGURATION,
                    self.Responsibility.CMDAEMON_RPC_FORWARD,
                    self.Responsibility.CMDAEMON_EVENTS,
                    self.Responsibility.CMDAEMON_STATUS,
                    self.Responsibility.CMDAEMON_WEB_SOCKET,
                    self.Responsibility.MONITORING_OFFLOAD,
                    self.Responsibility.UNDEFINED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Responsibility,
                default=self.Responsibility.UNDEFINED,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.UUID,
                description="Node",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="rules",
                kind=MetaData.Type.UUID,
                description="Rules from which nodes were derived",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="responsible",
                kind=MetaData.Type.UUID,
                description="List of nodes that are responsible for the node",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'NodeHierarchyResult'
        self.service_type = self.baseType
        self.allTypes = ['NodeHierarchyResult']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

