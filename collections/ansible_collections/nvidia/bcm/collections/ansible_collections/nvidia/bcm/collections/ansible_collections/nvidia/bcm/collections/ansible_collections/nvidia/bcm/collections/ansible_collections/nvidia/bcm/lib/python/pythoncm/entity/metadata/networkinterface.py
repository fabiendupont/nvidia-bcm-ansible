from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class NetworkInterface(Entity):
    """
    Network interface
    """
    class StartCondition(Enum):
        ALWAYS = auto()
        ACTIVE = auto()
        PASSIVE = auto()
        PREFERPASSIVE = auto()

    class BringUpDuringInstall(Enum):
        NO = auto()
        YES = auto()
        YESANDKEEP = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="The network interface device name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ip",
                kind=MetaData.Type.STRING,
                description="The interfaces IP address",
                function_check=MetaData.check_isIP,
                conditional_clone=lambda interface: not interface.dhcp,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ipv6Ip",
                kind=MetaData.Type.STRING,
                description="The interfaces IPv6 IP address",
                function_check=MetaData.check_isIP,
                conditional_clone=lambda interface: not interface.ipv6Dhcp,
                default="::0",
            )
        )
        self.meta.add(
            MetaDataField(
                name="dhcp",
                kind=MetaData.Type.BOOL,
                description="Get the ip via DHCP, leave ip blank",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ipv6Dhcp",
                kind=MetaData.Type.BOOL,
                description="Get the IPv6IP via DHCP, leave IPv6IP blank",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="bringupduringinstall",
                kind=MetaData.Type.ENUM,
                description="Brings up interface during install if on",
                options=[
                    self.BringUpDuringInstall.NO,
                    self.BringUpDuringInstall.YES,
                    self.BringUpDuringInstall.YESANDKEEP,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.BringUpDuringInstall,
                default=self.BringUpDuringInstall.NO,
            )
        )
        self.meta.add(
            MetaDataField(
                name="network",
                kind=MetaData.Type.RESOLVE,
                description="Network the interface is connected to",
                instance='Network',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="alternativeHostname",
                kind=MetaData.Type.STRING,
                description="An alternative hostname to use if this is second (startif != always) IP address on the same network",
                regex_check=r"(?!^[0-9]+$)^(|[a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9])$",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="additionalHostnames",
                kind=MetaData.Type.STRING,
                description="List of additional hostnames that should resolve to the interfaces IP address",
                regex_check=r"(?!^[0-9]+$)^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9])$",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="startIf",
                kind=MetaData.Type.ENUM,
                description="Only run this service in the specified state",
                options=[
                    self.StartCondition.ALWAYS,
                    self.StartCondition.ACTIVE,
                    self.StartCondition.PASSIVE,
                    self.StartCondition.PREFERPASSIVE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.StartCondition,
                default=self.StartCondition.ALWAYS,
            )
        )
        self.meta.add(
            MetaDataField(
                name="connectedMode",
                kind=MetaData.Type.BOOL,
                description="IB connected mode",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="bootable",
                kind=MetaData.Type.BOOL,
                description="Mark the interface bootable and write a DHCP entry with file information",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeFromDhcpd",
                kind=MetaData.Type.BOOL,
                description="Exclude from being added in dhcpd, use when both the members of a bond request an IP",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="switchPorts",
                kind=MetaData.Type.ENTITY,
                description="Switch ports",
                clone=False,
                instance='SwitchPort',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'NetworkInterface'
        self.service_type = self.baseType
        self.allTypes = ['NetworkInterface']
        self.leaf_entity = False
        self.resolve_field_name = 'name'

