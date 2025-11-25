from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class SNMPSettings(Entity):
    """
    SNMP settings
    """
    class Version(Enum):
        V1 = auto()
        V2c = auto()
        V3 = auto()
        File = auto()

    class AuthProtocol(Enum):
        MD5 = auto()
        SHA = auto()

    class PrivProtocol(Enum):
        AES = auto()
        DES = auto()

    class SecurityLevel(Enum):
        noAuthNoPriv = auto()
        authNoPriv = auto()
        authPriv = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="version",
                kind=MetaData.Type.ENUM,
                description="Version of SNMP that should be use to read information from the device",
                options=[
                    self.Version.V1,
                    self.Version.V2c,
                    self.Version.V3,
                    self.Version.File,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Version,
                default=self.Version.V2c,
            )
        )
        self.meta.add(
            MetaDataField(
                name="timeout",
                kind=MetaData.Type.FLOAT,
                description="SNMP timeout, set to 0 for default",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="vlanTimeout",
                kind=MetaData.Type.FLOAT,
                description="SNMP timeout for VLAN calls, set to 0 for default",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="retries",
                kind=MetaData.Type.INT,
                description="SNMP retries, set to -1 for default",
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="readString",
                kind=MetaData.Type.STRING,
                description="SNMP read-only community string",
                default="public",
            )
        )
        self.meta.add(
            MetaDataField(
                name="writeString",
                kind=MetaData.Type.STRING,
                description="SNMP read-write community string",
                default="private",
            )
        )
        self.meta.add(
            MetaDataField(
                name="securityName",
                kind=MetaData.Type.STRING,
                description="SNMP v3 security name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="context",
                kind=MetaData.Type.STRING,
                description="SNMP v3 context",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="authProtocol",
                kind=MetaData.Type.ENUM,
                description="SNMP v3 authentication protocol",
                options=[
                    self.AuthProtocol.MD5,
                    self.AuthProtocol.SHA,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.AuthProtocol,
                default=self.AuthProtocol.MD5,
            )
        )
        self.meta.add(
            MetaDataField(
                name="privProtocol",
                kind=MetaData.Type.ENUM,
                description="SNMP v3 privacy protocol",
                options=[
                    self.PrivProtocol.AES,
                    self.PrivProtocol.DES,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.PrivProtocol,
                default=self.PrivProtocol.DES,
            )
        )
        self.meta.add(
            MetaDataField(
                name="authKey",
                kind=MetaData.Type.STRING,
                description="SNMP v3 authentication key",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="privKey",
                kind=MetaData.Type.STRING,
                description="SNMP v3 private key",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="securityLevel",
                kind=MetaData.Type.ENUM,
                description="SNMP v3 security level",
                options=[
                    self.SecurityLevel.noAuthNoPriv,
                    self.SecurityLevel.authNoPriv,
                    self.SecurityLevel.authPriv,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.SecurityLevel,
                default=self.SecurityLevel.authPriv,
            )
        )
        self.meta.add(
            MetaDataField(
                name="filename",
                kind=MetaData.Type.STRING,
                description="Filename for SNMP testing",
                default='',
            )
        )
        self.baseType = 'SNMPSettings'
        self.service_type = self.baseType
        self.allTypes = ['SNMPSettings']
        self.top_level = False
        self.leaf_entity = True

