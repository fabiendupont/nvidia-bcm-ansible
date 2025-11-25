from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class DPUSettings(Entity):
    class OperationMode(Enum):
        NIC_MODE = auto()
        DPU_MODE = auto()

    class DisplayLevel(Enum):
        BASIC = auto()
        ADVANCED = auto()
        LOG = auto()

    class BootMode(Enum):
        RSHIM = auto()
        EMMC = auto()
        EMMC_BOOT_SWAP = auto()

    class DropMode(Enum):
        NORMAL = auto()
        DROP = auto()

    class InterfaceMode(Enum):
        IB = auto()
        ETH = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="operation_mode",
                kind=MetaData.Type.ENUM,
                description="Operation mode",
                options=[
                    self.OperationMode.NIC_MODE,
                    self.OperationMode.DPU_MODE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.OperationMode,
                default=self.OperationMode.NIC_MODE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="display_level",
                kind=MetaData.Type.ENUM,
                description="Display level",
                options=[
                    self.DisplayLevel.BASIC,
                    self.DisplayLevel.ADVANCED,
                    self.DisplayLevel.LOG,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.DisplayLevel,
                default=self.DisplayLevel.BASIC,
            )
        )
        self.meta.add(
            MetaDataField(
                name="boot_mode",
                kind=MetaData.Type.ENUM,
                description="Boot mode",
                options=[
                    self.BootMode.RSHIM,
                    self.BootMode.EMMC,
                    self.BootMode.EMMC_BOOT_SWAP,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.BootMode,
                default=self.BootMode.EMMC,
            )
        )
        self.meta.add(
            MetaDataField(
                name="drop_mode",
                kind=MetaData.Type.ENUM,
                description="Drop mode",
                options=[
                    self.DropMode.NORMAL,
                    self.DropMode.DROP,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.DropMode,
                default=self.DropMode.NORMAL,
            )
        )
        self.meta.add(
            MetaDataField(
                name="boot_timeout",
                kind=MetaData.Type.UINT,
                description="Boot timeout",
                default=100,
            )
        )
        self.meta.add(
            MetaDataField(
                name="boot_order",
                kind=MetaData.Type.STRING,
                description="Boot order",
                regex_check=r"^((DISK|UEFI_SHELL|NET-(NIC_P0|NIC_P1|OOB|RSHIM)(\.\w+)?-IPV(4|6)),?)+$",
                vector=True,
                default=["NET-OOB-IPV4","DISK"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="interface_mode_port1",
                kind=MetaData.Type.ENUM,
                description="Interface mode port 1",
                options=[
                    self.InterfaceMode.IB,
                    self.InterfaceMode.ETH,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.InterfaceMode,
                default=self.InterfaceMode.ETH,
            )
        )
        self.meta.add(
            MetaDataField(
                name="interface_mode_port2",
                kind=MetaData.Type.ENUM,
                description="Interface mode port 2",
                options=[
                    self.InterfaceMode.IB,
                    self.InterfaceMode.ETH,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.InterfaceMode,
                default=self.InterfaceMode.ETH,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hw_offload",
                kind=MetaData.Type.BOOL,
                description="Offload OVS to hardware",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="keyValueSettings",
                kind=MetaData.Type.ENTITY,
                description="Key value settings which can be passed to the DPU manage script",
                instance='KeyValueSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.baseType = 'DPUSettings'
        self.service_type = self.baseType
        self.allTypes = ['DPUSettings']
        self.top_level = False
        self.leaf_entity = True

