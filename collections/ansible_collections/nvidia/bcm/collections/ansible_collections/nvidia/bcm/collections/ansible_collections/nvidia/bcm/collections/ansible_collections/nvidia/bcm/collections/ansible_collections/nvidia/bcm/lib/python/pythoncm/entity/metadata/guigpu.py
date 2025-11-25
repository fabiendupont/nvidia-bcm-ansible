from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiGPU(Entity):
    class FabricStatus(Enum):
        NOT_SUPPORTED = auto()
        NOT_STARTED = auto()
        IN_PROGRESS = auto()
        SUCCESS = auto()
        FAILURE = auto()
        UNRECOGNIZED = auto()
        NVLM_TOO_OLD = auto()
        UNDEFINED = auto()

    class HealthOverall(Enum):
        PASS = auto()
        UNKNOWN = auto()
        FAIL = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_device_uuid",
                kind=MetaData.Type.UUID,
                description="Device",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryUsed",
                kind=MetaData.Type.UINT,
                description="Memory used",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryFree",
                kind=MetaData.Type.UINT,
                description="Memory free",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="utilization",
                kind=MetaData.Type.FLOAT,
                description="GPU Utilization",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerUsage",
                kind=MetaData.Type.FLOAT,
                description="Power usage",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="temperature",
                kind=MetaData.Type.FLOAT,
                description="Temperature",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="smClock",
                kind=MetaData.Type.FLOAT,
                description="Streaming multiprocessor clock speed",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryClock",
                kind=MetaData.Type.FLOAT,
                description="Memory clock speed",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fabricStatus",
                kind=MetaData.Type.ENUM,
                description="Fabric status",
                options=[
                    self.FabricStatus.NOT_SUPPORTED,
                    self.FabricStatus.NOT_STARTED,
                    self.FabricStatus.IN_PROGRESS,
                    self.FabricStatus.SUCCESS,
                    self.FabricStatus.FAILURE,
                    self.FabricStatus.UNRECOGNIZED,
                    self.FabricStatus.NVLM_TOO_OLD,
                    self.FabricStatus.UNDEFINED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.FabricStatus,
                default=self.FabricStatus.UNDEFINED,
            )
        )
        self.meta.add(
            MetaDataField(
                name="healthOverall",
                kind=MetaData.Type.ENUM,
                description="Health overal",
                options=[
                    self.HealthOverall.PASS,
                    self.HealthOverall.UNKNOWN,
                    self.HealthOverall.FAIL,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.HealthOverall,
                default=self.HealthOverall.UNKNOWN,
            )
        )
        self.baseType = 'GuiGPU'
        self.service_type = self.baseType
        self.allTypes = ['GuiGPU']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

