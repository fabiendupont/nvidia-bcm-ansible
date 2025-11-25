from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Device(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="hostname",
                kind=MetaData.Type.STRING,
                description="Hostname",
                regex_check=r"(?!^[0-9]+$)^([a-zA-Z0-9]|[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9])$",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mac",
                kind=MetaData.Type.STRING,
                description="MAC address",
                function_check=MetaData.check_isMAC,
                clone=False,
                default='00:00:00:00:00:00',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultGateway",
                kind=MetaData.Type.STRING,
                description="Default gateway for the device",
                function_check=MetaData.check_isIP,
                default='0.0.0.0',
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultGatewayMetric",
                kind=MetaData.Type.UINT,
                description="Default gateway metric",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="creationTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Date on which node was defined",
                readonly=True,
                clone=False,
                diff_type=MetaDataField.Diff.none,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="partition",
                kind=MetaData.Type.RESOLVE,
                description="Partition to which this device belongs",
                instance='Partition',
                default=None,
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
        self.meta.add(
            MetaDataField(
                name="powerDistributionUnits",
                kind=MetaData.Type.ENTITY,
                description="List of outlets on powerdistributionunits",
                clone=False,
                instance='PDUPort',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="rackPosition",
                kind=MetaData.Type.ENTITY,
                description="Name of the rack in which the device resides",
                clone=False,
                instance='RackPosition',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="chassisPosition",
                kind=MetaData.Type.ENTITY,
                description="Chassis position in which the device resides",
                clone=False,
                instance='ChassisPosition',
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
                name="bmcSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the baseboard management controller settings",
                instance='BMCSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerControl",
                kind=MetaData.Type.STRING,
                description="Specifies which type of power control feature is being used (values: none, apc, custom, cloud, ipmi0, ilo0, drac0, rf0, cimc0 or rshim0)",
                regex_check=r"(none|apc|custom|cloud|ipmi[0-9]*|ilo[0-9]*|cimc[0-9]*|drac[0-9]*|rf[0-9]*|rshim[0-9]+)",
                default="none",
            )
        )
        self.meta.add(
            MetaDataField(
                name="customPowerScript",
                kind=MetaData.Type.STRING,
                description="Script that will be used to perform power on/off/reset/status operations",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="customPowerScriptArgument",
                kind=MetaData.Type.STRING,
                description="Argument for the custom power script",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="customPingScript",
                kind=MetaData.Type.STRING,
                description="Script that will be used to ping a device",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="customPingScriptArgument",
                kind=MetaData.Type.STRING,
                description="Argument for the custom ping script",
                default='',
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
                name="interfaces",
                kind=MetaData.Type.ENTITY,
                description="IP on the management network",
                instance='NetworkInterface',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="provisioningInterface",
                kind=MetaData.Type.ELEMENT_OF,
                description="Network interface on which the node will receive software image updates",
                element_of="interfaces",
                instance='NetworkInterface',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="managementNetwork",
                kind=MetaData.Type.RESOLVE,
                description="Determines what network should be used for management traffic. If not set, category or partition setting is used.",
                instance='Network',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="userdefined1",
                kind=MetaData.Type.STRING,
                description="A free text field passed to custom scripts",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="userdefined2",
                kind=MetaData.Type.STRING,
                description="A free text field passed to custom scripts",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="userDefinedResources",
                kind=MetaData.Type.STRING,
                description="User defined resources used to filter monitoring data producers",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="supportsGNSS",
                kind=MetaData.Type.BOOL,
                description="Supports GNSS location",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="partNumber",
                kind=MetaData.Type.STRING,
                description="Part number",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="serialNumber",
                kind=MetaData.Type.STRING,
                description="Serial number",
                clone=False,
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
        self.baseType = 'Device'
        self.service_type = self.baseType
        self.allTypes = ['Device']
        self.leaf_entity = False
        self.resolve_field_name = 'hostname'

