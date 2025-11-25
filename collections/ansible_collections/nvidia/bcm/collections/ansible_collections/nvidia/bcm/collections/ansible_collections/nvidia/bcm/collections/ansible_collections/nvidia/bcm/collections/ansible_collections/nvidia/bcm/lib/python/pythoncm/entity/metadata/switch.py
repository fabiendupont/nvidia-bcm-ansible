from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.device import Device


class Switch(Device):
    class Kind(Enum):
        UNDEFINED = auto()
        ETHERNET = auto()
        INFINIBAND = auto()
        NVLINK = auto()

    class CiscoMode(Enum):
        UNKNOWN = auto()
        YES = auto()
        NO = auto()

    class NVConfigurationMode(Enum):
        AUTO = auto()
        MANUAL = auto()
        FILE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ports",
                kind=MetaData.Type.INT,
                description="Number of ports",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="kind",
                kind=MetaData.Type.ENUM,
                description="Kind",
                options=[
                    self.Kind.UNDEFINED,
                    self.Kind.ETHERNET,
                    self.Kind.INFINIBAND,
                    self.Kind.NVLINK,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Kind,
                default=self.Kind.UNDEFINED,
            )
        )
        self.meta.add(
            MetaDataField(
                name="model",
                kind=MetaData.Type.STRING,
                description="The switch model",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="snmpSettings",
                kind=MetaData.Type.ENTITY,
                description="Configure the cluster wide SNMP settings",
                instance='SNMPSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="members",
                kind=MetaData.Type.RESOLVE,
                description="List of switches belonging to this stack",
                clone=False,
                instance='Switch',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="controlScript",
                kind=MetaData.Type.STRING,
                description="Custom control script that provides switch functionality",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="controlScriptTimeout",
                kind=MetaData.Type.UINT,
                description="Control script timeout",
                default=5,
            )
        )
        self.meta.add(
            MetaDataField(
                name="priority",
                kind=MetaData.Type.UINT,
                description="Devices on multiple switches will be listed under the switch with the largest priority",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="category",
                kind=MetaData.Type.RESOLVE,
                description="Category to which this node belongs",
                instance='Category',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="lowestPort",
                kind=MetaData.Type.INT,
                description="Lowest port",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="uplinks",
                kind=MetaData.Type.INT,
                description="List of ports connected to other switches.",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="disablePortDetection",
                kind=MetaData.Type.BOOL,
                description="Disable port detection for this switch",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disablePortMapping",
                kind=MetaData.Type.BOOL,
                description="Disable port index mapping",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="vlanCacheTime",
                kind=MetaData.Type.UINT,
                description="Time to cache VLAN information",
                default=300,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hasClientDaemon",
                kind=MetaData.Type.BOOL,
                description="Switch runs a python cluster manager client daemon",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="vrf",
                kind=MetaData.Type.STRING,
                description="Force a specific VRF to be used by the cluster manager client daemon",
                default='',
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
                name="guid",
                kind=MetaData.Type.UUID,
                description="The switch GUID",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="bootFile",
                kind=MetaData.Type.STRING,
                description="Boot for Infiniband switches",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="subnetManager",
                kind=MetaData.Type.BOOL,
                description="Indicate the subnet manager is running",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disableSNMP",
                kind=MetaData.Type.BOOL,
                description="Disable SNMP calls",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="services",
                kind=MetaData.Type.ENTITY,
                description="Manage operating system services",
                instance='OSServiceConfig',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="nvConfigurationMode",
                kind=MetaData.Type.ENUM,
                description="NV configuration mode",
                options=[
                    self.NVConfigurationMode.AUTO,
                    self.NVConfigurationMode.MANUAL,
                    self.NVConfigurationMode.FILE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.NVConfigurationMode,
                default=self.NVConfigurationMode.AUTO,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nvConfigurationFile",
                kind=MetaData.Type.STRING,
                description="NV configuration file",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="nvConfiguration",
                kind=MetaData.Type.JSON,
                description="Manual NV configuration",
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fmConfigFile",
                kind=MetaData.Type.STRING,
                description="FM config file",
                default='',
            )
        )
        self.baseType = 'Device'
        self.childType = 'Switch'
        self.service_type = self.baseType
        self.allTypes = ['Switch', 'Device']
        self.top_level = True
        self.leaf_entity = True

