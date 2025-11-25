from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BMCSettings(Entity):
    """
    Baseboard Management Controller settings
    """
    class Type(Enum):
        IPMI = auto()
        ILO = auto()
        CIMC = auto()
        DRAC = auto()
        REDFISH = auto()
        UNKNOWN = auto()

    class Privilege(Enum):
        CALLBACK = auto()
        USER = auto()
        OPERATOR = auto()
        ADMINISTRATOR = auto()
        OEM_PROPRIETARY = auto()
        NO_ACCESS = auto()

    class FirmwareManageMode(Enum):
        NONE = auto()
        AUTO = auto()
        FAKE = auto()
        ILO = auto()
        H100 = auto()
        GH200 = auto()
        FAKE_H100 = auto()
        FAKE_GH200 = auto()
        B200 = auto()
        GB200 = auto()
        GB200SW = auto()
        DELTA_POWER_SHELF = auto()
        NVIDIA_POWER_SHELF = auto()

    class LeakPolicy(Enum):
        NONE = auto()
        ENABLED = auto()
        DISABLED = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="userName",
                kind=MetaData.Type.STRING,
                description="Username used to send BMC commands",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="userID",
                kind=MetaData.Type.INT,
                description="User ID to send BMC commands",
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="password",
                kind=MetaData.Type.STRING,
                description="Password used to send BMC commands",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerResetDelay",
                kind=MetaData.Type.UINT,
                description="Delay used for BMC power reset, if set to > 0 power off; sleep X; power on is used",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="extraArguments",
                kind=MetaData.Type.STRING,
                description="Extra arguments passed to BMC commands",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="privilege",
                kind=MetaData.Type.ENUM,
                description="Privilege given to the user",
                options=[
                    self.Privilege.CALLBACK,
                    self.Privilege.USER,
                    self.Privilege.OPERATOR,
                    self.Privilege.ADMINISTRATOR,
                    self.Privilege.OEM_PROPRIETARY,
                    self.Privilege.NO_ACCESS,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Privilege,
                default=self.Privilege.ADMINISTRATOR,
            )
        )
        self.meta.add(
            MetaDataField(
                name="firmwareManageMode",
                kind=MetaData.Type.ENUM,
                description="Firmware management mode for devices",
                options=[
                    self.FirmwareManageMode.NONE,
                    self.FirmwareManageMode.AUTO,
                    self.FirmwareManageMode.ILO,
                    self.FirmwareManageMode.H100,
                    self.FirmwareManageMode.B200,
                    self.FirmwareManageMode.GB200,
                    self.FirmwareManageMode.GB200SW,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.FirmwareManageMode,
                default=self.FirmwareManageMode.AUTO,
            )
        )
        self.meta.add(
            MetaDataField(
                name="leakPolicy",
                kind=MetaData.Type.ENUM,
                description="Leak policy inside the BMC itself",
                options=[
                    self.LeakPolicy.NONE,
                    self.LeakPolicy.ENABLED,
                    self.LeakPolicy.DISABLED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.LeakPolicy,
                default=self.LeakPolicy.NONE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="leakReactionDelay",
                kind=MetaData.Type.FLOAT,
                default=0.0,
            )
        )
        self.baseType = 'BMCSettings'
        self.service_type = self.baseType
        self.allTypes = ['BMCSettings']
        self.top_level = False
        self.leaf_entity = True

