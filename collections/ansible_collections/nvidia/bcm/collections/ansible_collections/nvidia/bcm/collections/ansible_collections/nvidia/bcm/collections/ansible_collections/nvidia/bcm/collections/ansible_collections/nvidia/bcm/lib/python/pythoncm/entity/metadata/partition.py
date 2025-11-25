from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Partition(Entity):
    """
    Partition
    """
    class AutoSign(Enum):
        AUTO = auto()
        MANUAL = auto()

    class BMS(Enum):
        CRONUS = auto()
        PIPE = auto()
        FILE = auto()
        URL = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Partition name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="clusterName",
                kind=MetaData.Type.STRING,
                description="Cluster name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="clusterReferenceArchitecture",
                kind=MetaData.Type.STRING,
                description="Description of the cluster architecture",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="primaryHeadNode",
                kind=MetaData.Type.RESOLVE,
                description="Primary head node",
                instance='HeadNode',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="failover",
                kind=MetaData.Type.ENTITY,
                description="Manage failover setup for this cluster",
                instance='CMDaemonFailover',
                create_instance=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeZoneSettings",
                kind=MetaData.Type.ENTITY,
                description="Time zone",
                instance='TimeZoneSettings',
                create_instance=True,
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="adminEmail",
                kind=MetaData.Type.STRING,
                description="Administrator email",
                function_check=MetaData.check_isEmail,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="slaveName",
                kind=MetaData.Type.STRING,
                description="Default prefix to identify nodes. eg node003 (basename = node)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="slaveDigits",
                kind=MetaData.Type.UINT,
                description="Number of digits used to identify nodes. eg node003 (digits = 3)",
                default=3,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nameServers",
                kind=MetaData.Type.STRING,
                description="Name servers",
                function_check=MetaData.check_isIPv4or6,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="nameServersFromDhcp",
                kind=MetaData.Type.STRING,
                description="Name servers provided by DHCP, edit the name servers property instead",
                function_check=MetaData.check_isIPv4or6,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeServers",
                kind=MetaData.Type.STRING,
                description="NTP time servers",
                function_check=MetaData.check_isIPv4or6orHostname,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="searchDomains",
                kind=MetaData.Type.STRING,
                description="DNS search domains",
                function_check=MetaData.check_isDomainWithIndex,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="externallyVisibleIp",
                kind=MetaData.Type.STRING,
                description="IP that external sites see when headnode connects",
                function_check=MetaData.check_isIPv4or6,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="externalNetwork",
                kind=MetaData.Type.RESOLVE,
                description="The external network",
                instance='Network',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultCategory",
                kind=MetaData.Type.RESOLVE,
                description="Default category for new nodes",
                instance='Category',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="archOS",
                kind=MetaData.Type.ENTITY,
                description="Architecture operating system",
                instance='ArchOS',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="burnConfigs",
                kind=MetaData.Type.ENTITY,
                description="Burn configurations",
                instance='BurnConfig',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="failoverGroups",
                kind=MetaData.Type.ENTITY,
                description="Failover group configurations",
                instance='CMDaemonFailoverGroup',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="resourcePools",
                kind=MetaData.Type.ENTITY,
                description="Resource pools",
                instance='ResourcePool',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultBurnConfig",
                kind=MetaData.Type.ELEMENT_OF,
                description="Default burn configuration",
                element_of="burnConfigs",
                instance='BurnConfig',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="bmcSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the baseboard management controller settings",
                instance='BMCSettings',
                create_instance=True,
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="snmpSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the cluster wide SNMP settings",
                instance='SNMPSettings',
                create_instance=True,
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dpuSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the DPU settings",
                instance='DPUSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ztpSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the ZTP settings",
                instance='ZTPSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ztpNewSwitchSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the ZTP settings",
                instance='ZTPNewSwitchSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="seLinuxSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the SELinux settings",
                instance='SELinuxSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="accessSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the cluster wide Access settings",
                instance='AccessSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="netQSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure NetQ settings",
                instance='NetQSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ufmSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure UFM settings",
                instance='UFMSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nmxmSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure NMX Manager settings",
                instance='NMXMSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="managementNetwork",
                kind=MetaData.Type.RESOLVE,
                description="Determines what network should be used for management traffic.",
                instance='Network',
                default=None,
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
                name="provisioningSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the provisioning settings",
                instance='ProvisioningSettings',
                create_instance=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="relayHost",
                kind=MetaData.Type.STRING,
                description="SMTP mail relay host",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="noZeroConf",
                kind=MetaData.Type.BOOL,
                description="Add nozeroconf to network configuration",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="proxySettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the proxy server settings",
                instance='ProxySettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="wlmJobPowerUsageSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the Wlm job power usage settings",
                instance='WlmJobPowerUsageSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="leakActionPolicies",
                kind=MetaData.Type.ENTITY,
                description="Leak action policies",
                instance='LeakActionPolicy',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="activeLeakActionPolicy",
                kind=MetaData.Type.ELEMENT_OF,
                description="Active leak action policy",
                element_of="leakActionPolicies",
                instance='LeakActionPolicy',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="autosign",
                kind=MetaData.Type.ENUM,
                description="Sign certificates for node installer request according to network settings.",
                options=[
                    self.AutoSign.AUTO,
                    self.AutoSign.MANUAL,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.AutoSign,
                default=self.AutoSign.AUTO,
            )
        )
        self.meta.add(
            MetaDataField(
                name="bms",
                kind=MetaData.Type.ENUM,
                description="Specify the type of BMS",
                options=[
                    self.BMS.CRONUS,
                    self.BMS.PIPE,
                    self.BMS.FILE,
                    self.BMS.URL,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.BMS,
                default=self.BMS.CRONUS,
            )
        )
        self.meta.add(
            MetaDataField(
                name="bmsPath",
                kind=MetaData.Type.STRING,
                description="The path/url used to push information to BMS",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="bmsCertificate",
                kind=MetaData.Type.STRING,
                description="The certificate used to push information to BMS url",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="bmsPrivateKey",
                kind=MetaData.Type.STRING,
                description="The private key used to push information to BMS url",
                default='',
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
        self.baseType = 'Partition'
        self.service_type = self.baseType
        self.allTypes = ['Partition']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

