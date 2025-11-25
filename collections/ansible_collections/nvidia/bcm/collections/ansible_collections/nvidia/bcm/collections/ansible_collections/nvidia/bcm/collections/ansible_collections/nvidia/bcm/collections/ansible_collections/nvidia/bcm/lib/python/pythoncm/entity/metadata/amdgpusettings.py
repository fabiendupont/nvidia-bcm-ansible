from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.gpusettings import GPUSettings


class AMDGPUSettings(GPUSettings):
    class PowerPlay(Enum):
        DEFAULT = auto()
        AUTO = auto()
        LOW = auto()
        HIGH = auto()
        MANUAL = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="gpuClockLevel",
                kind=MetaData.Type.UINT,
                description="Set the GPU clock frequency level",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryClockLevel",
                kind=MetaData.Type.UINT,
                description="Set the GPU memory clock frequency level",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerPlay",
                kind=MetaData.Type.ENUM,
                description="Set powerplay level",
                options=[
                    self.PowerPlay.DEFAULT,
                    self.PowerPlay.AUTO,
                    self.PowerPlay.LOW,
                    self.PowerPlay.HIGH,
                    self.PowerPlay.MANUAL,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.PowerPlay,
                default=self.PowerPlay.DEFAULT,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gpuOverDrive",
                kind=MetaData.Type.FLOAT,
                description="This sets the percentage above maximum for the max performance Level",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryOverDrive",
                kind=MetaData.Type.FLOAT,
                description="This sets the percentage above maximum for the max performance Level",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fanSpeed",
                kind=MetaData.Type.UINT,
                description="Fan speed value",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="minimalGPUClock",
                kind=MetaData.Type.UINT,
                description="Minimum GPU clock speed",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="minimalMemoryClock",
                kind=MetaData.Type.UINT,
                description="Minimum GPU Memory clock speed",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="activityThreshold",
                kind=MetaData.Type.FLOAT,
                description="Workload required before clock levels change",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hysteresisUp",
                kind=MetaData.Type.FLOAT,
                description="Delay before clock level is increased",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hysteresisDown",
                kind=MetaData.Type.FLOAT,
                description="Delay before clock level is decreased",
                default=0.0,
            )
        )
        self.baseType = 'GPUSettings'
        self.childType = 'AMDGPUSettings'
        self.service_type = self.baseType
        self.allTypes = ['AMDGPUSettings', 'GPUSettings']
        self.top_level = False
        self.leaf_entity = True

