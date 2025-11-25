from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.device import Device


class PowerDistributionUnit(Device):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="model",
                kind=MetaData.Type.STRING,
                description="PowerDistributionUnit model name",
                readonly=True,
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ports",
                kind=MetaData.Type.INT,
                description="Number of outlets",
                readonly=True,
                clone=False,
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="banks",
                kind=MetaData.Type.INT,
                description="Number of banks",
                readonly=True,
                clone=False,
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="phases",
                kind=MetaData.Type.INT,
                description="Number of phases",
                readonly=True,
                clone=False,
                default=-1,
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
                name="firmware",
                kind=MetaData.Type.STRING,
                description="Firmware revision",
                readonly=True,
                clone=False,
                default='',
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
                name="controlScript",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="controlScriptTimeout",
                kind=MetaData.Type.UINT,
                default=5,
            )
        )
        self.baseType = 'Device'
        self.childType = 'PowerDistributionUnit'
        self.service_type = self.baseType
        self.allTypes = ['PowerDistributionUnit', 'Device']
        self.top_level = True
        self.leaf_entity = True

