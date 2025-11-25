from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Network(Entity):
    """
    Network
    """
    class Type(Enum):
        INTERNAL = auto()
        EXTERNAL = auto()
        TUNNEL = auto()
        GLOBAL = auto()
        CLOUD = auto()
        NETMAP = auto()
        EDGE_INTERNAL = auto()
        EDGE_EXTERNAL = auto()
        EDGE_VIRTUAL = auto()

    class Route(Enum):
        NONE = auto()
        STATIC = auto()
        DEFAULT = auto()

    class Autosign(Enum):
        AUTOMATIC = auto()
        ALWAYS = auto()
        NEVER = auto()
        SECRET = auto()

    class DNSZoneGeneration(Enum):
        BOTH = auto()
        FORWARD = auto()
        REVERSE = auto()
        NEITHER = auto()

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
                name="IPv6",
                kind=MetaData.Type.BOOL,
                description="IPv6 enabled",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ipv6NetmaskBits",
                kind=MetaData.Type.UINT,
                description="Netmask or Classless Inter-Domain Routing for IPv6",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="netmaskBits",
                kind=MetaData.Type.UINT,
                description="Netmask or Classless Inter-Domain Routing",
                default=16,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ipv6BaseAddress",
                kind=MetaData.Type.STRING,
                description="Base IP address for Ipv6",
                function_check=MetaData.check_isIP,
                default="::0",
            )
        )
        self.meta.add(
            MetaDataField(
                name="baseAddress",
                kind=MetaData.Type.STRING,
                description="Base IP address",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="domainName",
                kind=MetaData.Type.STRING,
                description="Domain name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="type",
                kind=MetaData.Type.ENUM,
                description="Type of network, internal: local cluster network, external: connection to outside world, global: unique network accros the cloud, tunnel: cloud network, netmap: virtual network user by cloud nodes to connect to nodes inside the cluster",
                options=[
                    self.Type.INTERNAL,
                    self.Type.EXTERNAL,
                    self.Type.TUNNEL,
                    self.Type.GLOBAL,
                    self.Type.CLOUD,
                    self.Type.NETMAP,
                    self.Type.EDGE_INTERNAL,
                    self.Type.EDGE_EXTERNAL,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Type,
                default=self.Type.INTERNAL,
            )
        )
        self.meta.add(
            MetaDataField(
                name="mtu",
                kind=MetaData.Type.UINT,
                description="The maximum transmission unit.",
                default=1500,
            )
        )
        self.meta.add(
            MetaDataField(
                name="bootable",
                kind=MetaData.Type.BOOL,
                description="If set compute nodes can boot using this network",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dynamicRangeStart",
                kind=MetaData.Type.STRING,
                description="First IP address in the networks dynamic range",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="dynamicRangeEnd",
                kind=MetaData.Type.STRING,
                description="Last IP address in the networks dynamic range",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="lockDownDhcpd",
                kind=MetaData.Type.BOOL,
                description="Don't respond to dhcp request of new nodes via this network",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="management",
                kind=MetaData.Type.BOOL,
                description="If set, the network can be used as a management network",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gateway",
                kind=MetaData.Type.STRING,
                description="Gateway",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="gatewayMetric",
                kind=MetaData.Type.UINT,
                description="Gateway metric",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ipv6Gateway",
                kind=MetaData.Type.STRING,
                description="IPv6 Gateway",
                function_check=MetaData.check_isIP,
                default="::0",
            )
        )
        self.meta.add(
            MetaDataField(
                name="layer3",
                kind=MetaData.Type.BOOL,
                description="Create a network routed on layer3 with /31 netmask",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="layer3route",
                kind=MetaData.Type.ENUM,
                description="Layer3 routing",
                options=[
                    self.Route.NONE,
                    self.Route.STATIC,
                    self.Route.DEFAULT,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Route,
                default=self.Route.NONE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="layer3ecmp",
                kind=MetaData.Type.BOOL,
                description="Create a layer3 network with equal-cost multi-path",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="layer3splitStaticRoute",
                kind=MetaData.Type.BOOL,
                description="Create a layer3 network with equal-cost multi-path",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="notes",
                kind=MetaData.Type.STRING,
                description="Administrator notes",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="cloudSubnetID",
                kind=MetaData.Type.STRING,
                description="The Cloud ID of the subnet",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="EC2AvailabilityZone",
                kind=MetaData.Type.STRING,
                description="The AWS availability zone inside which the subnet exists",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowAutosign",
                kind=MetaData.Type.ENUM,
                description="Specify if certificate request from node installers can be signed automatically",
                options=[
                    self.Autosign.AUTOMATIC,
                    self.Autosign.ALWAYS,
                    self.Autosign.NEVER,
                    self.Autosign.SECRET,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Autosign,
                default=self.Autosign.AUTOMATIC,
            )
        )
        self.meta.add(
            MetaDataField(
                name="generateDNSZone",
                kind=MetaData.Type.ENUM,
                description="Specify which DNS zones should be written",
                options=[
                    self.DNSZoneGeneration.BOTH,
                    self.DNSZoneGeneration.FORWARD,
                    self.DNSZoneGeneration.REVERSE,
                    self.DNSZoneGeneration.NEITHER,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.DNSZoneGeneration,
                default=self.DNSZoneGeneration.BOTH,
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeFromSearchDomain",
                kind=MetaData.Type.BOOL,
                description="Exlude from search domain in /etc/resolv.conf file",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="searchDomainIndex",
                kind=MetaData.Type.UINT,
                description="Search domain index in /etc/resolv.conf file, set to 0 for automatic",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disableAutomaticExports",
                kind=MetaData.Type.BOOL,
                description="Disable creation of automatic filesystem exports",
                default=False,
            )
        )
        self.baseType = 'Network'
        self.service_type = self.baseType
        self.allTypes = ['Network']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

