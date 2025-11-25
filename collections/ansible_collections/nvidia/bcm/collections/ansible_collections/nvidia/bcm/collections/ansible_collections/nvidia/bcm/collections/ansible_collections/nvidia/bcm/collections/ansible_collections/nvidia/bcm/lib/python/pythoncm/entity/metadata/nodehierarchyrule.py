from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class NodeHierarchyRule(Entity):
    class Distribution(Enum):
        ANY = auto()
        ALL = auto()
        BALANCED = auto()
        FIRST = auto()
        HA = auto()
        SELF = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="description",
                kind=MetaData.Type.STRING,
                description="description",
                default='',
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
                name="priority",
                kind=MetaData.Type.UINT,
                description="Priority",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowSelf",
                kind=MetaData.Type.BOOL,
                description="Allow node to serve itself",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="locationMatch",
                kind=MetaData.Type.BOOL,
                description="Source and target node locations need to match",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="sources",
                kind=MetaData.Type.ENTITY,
                description="Source selection",
                instance='NodeHierarchyRuleSelection',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="targets",
                kind=MetaData.Type.ENTITY,
                description="Target selection",
                instance='NodeHierarchyRuleSelection',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="director",
                kind=MetaData.Type.BOOL,
                description="Director",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dhcp",
                kind=MetaData.Type.BOOL,
                description="DHCP",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dns",
                kind=MetaData.Type.BOOL,
                description="DNS",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ntp",
                kind=MetaData.Type.BOOL,
                description="NTP",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="vpn",
                kind=MetaData.Type.BOOL,
                description="VPN",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rsyslog",
                kind=MetaData.Type.BOOL,
                description="rsyslog",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ldap",
                kind=MetaData.Type.BOOL,
                description="LDAP",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="bios",
                kind=MetaData.Type.BOOL,
                description="BIOS",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="provisioning",
                kind=MetaData.Type.BOOL,
                description="Provisioning",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mount",
                kind=MetaData.Type.BOOL,
                description="Mount",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="sshProxy",
                kind=MetaData.Type.BOOL,
                description="SSH proxy",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cmdaemonConfiguration",
                kind=MetaData.Type.BOOL,
                description="Configuration",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cmdaemonRpcForward",
                kind=MetaData.Type.BOOL,
                description="RPC forward",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cmdaemonEvents",
                kind=MetaData.Type.BOOL,
                description="Events",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cmdaemonStatus",
                kind=MetaData.Type.BOOL,
                description="Status",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cmdaemonWebSocket",
                kind=MetaData.Type.BOOL,
                description="Web socket for lite nodes",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="monitoringOffload",
                kind=MetaData.Type.BOOL,
                description="Monitoring offload",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="distribution",
                kind=MetaData.Type.ENUM,
                description="Distribution",
                options=[
                    self.Distribution.ANY,
                    self.Distribution.ALL,
                    self.Distribution.BALANCED,
                    self.Distribution.FIRST,
                    self.Distribution.HA,
                    self.Distribution.SELF,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Distribution,
                default=self.Distribution.ANY,
            )
        )
        self.baseType = 'NodeHierarchyRule'
        self.service_type = self.baseType
        self.allTypes = ['NodeHierarchyRule']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

