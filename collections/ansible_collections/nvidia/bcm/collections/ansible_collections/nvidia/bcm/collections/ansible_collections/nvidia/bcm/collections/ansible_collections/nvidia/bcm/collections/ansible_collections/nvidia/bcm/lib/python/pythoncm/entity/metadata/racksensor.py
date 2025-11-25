from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.device import Device


class RackSensor(Device):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="model",
                kind=MetaData.Type.STRING,
                description="RackSensor model name",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="sensors",
                kind=MetaData.Type.ENTITY,
                description="Sensors in the rackmon kit",
                readonly=True,
                instance='Sensor',
                vector=True,
                default=[],
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
                name="disableSNMP",
                kind=MetaData.Type.BOOL,
                description="Disable SNMP calls",
                default=False,
            )
        )
        self.baseType = 'Device'
        self.childType = 'RackSensor'
        self.service_type = self.baseType
        self.allTypes = ['RackSensor', 'Device']
        self.top_level = True
        self.leaf_entity = True

