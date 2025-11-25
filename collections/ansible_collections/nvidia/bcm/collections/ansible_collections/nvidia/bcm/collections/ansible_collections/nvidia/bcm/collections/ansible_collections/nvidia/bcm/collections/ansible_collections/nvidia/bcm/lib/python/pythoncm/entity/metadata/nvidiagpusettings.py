from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.gpusettings import GPUSettings


class NvidiaGPUSettings(GPUSettings):
    """
    Nvidia GPU settings
    """
    class EccMode(Enum):
        DISABLED = auto()
        ENABLED = auto()
        NONE = auto()

    class ComputeMode(Enum):
        UNRESTRICTED = auto()
        PROHIBITED = auto()
        EXCLUSIVE_PROCESS = auto()
        NONE = auto()

    class ClockSyncBoostMode(Enum):
        DISABLED = auto()
        ENABLED = auto()
        NONE = auto()

    class WorkloadPowerProfile(Enum):
        MAX_P = auto()
        MAX_Q = auto()
        COMPUTE = auto()
        MEMORY_BOUND = auto()
        NETWORK = auto()
        BALANCED = auto()
        LLM_INFERENCE = auto()
        LLM_TRAINING = auto()
        RBM = auto()
        DCPCIE = auto()
        HMMA_SPARSE = auto()
        HMMA_DENSE = auto()
        SYNC_BALANCED = auto()
        HPC = auto()
        MIG = auto()
        UNDEFINED = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="powerLimit",
                kind=MetaData.Type.UINT,
                description="An upper limit on how much power a GPU can use",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="eccMode",
                kind=MetaData.Type.ENUM,
                description="Set the ECC mode in which the GPU runs",
                options=[
                    self.EccMode.DISABLED,
                    self.EccMode.ENABLED,
                    self.EccMode.NONE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.EccMode,
                default=self.EccMode.NONE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="computeMode",
                kind=MetaData.Type.ENUM,
                description="Set the compute mode in which the GPU runs",
                options=[
                    self.ComputeMode.UNRESTRICTED,
                    self.ComputeMode.PROHIBITED,
                    self.ComputeMode.EXCLUSIVE_PROCESS,
                    self.ComputeMode.NONE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.ComputeMode,
                default=self.ComputeMode.NONE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="clockSyncBoostMode",
                kind=MetaData.Type.ENUM,
                description="Set the clock sync boost among the GPUs in group",
                options=[
                    self.ClockSyncBoostMode.DISABLED,
                    self.ClockSyncBoostMode.ENABLED,
                    self.ClockSyncBoostMode.NONE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.ClockSyncBoostMode,
                default=self.ClockSyncBoostMode.NONE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="multiProcessorClockSpeed",
                kind=MetaData.Type.UINT,
                description="Set the streaming multiprocessor clock speed of the GPU",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryClockSpeed",
                kind=MetaData.Type.UINT,
                description="Set the streaming memory clock speed of the GPU",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="migProfiles",
                kind=MetaData.Type.STRING,
                description="MIG profiles that will be applied to the GPU",
                regex_check=r"^(\d+\*)?(\d+|\d+g\.\d+gb(\+me)?)(:\d+c?)*$",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="workloadPowerProfile",
                kind=MetaData.Type.ENUM,
                description="Set the clock workload power profile among the GPUs in group",
                options=[
                    self.WorkloadPowerProfile.MAX_P,
                    self.WorkloadPowerProfile.MAX_Q,
                    self.WorkloadPowerProfile.LLM_INFERENCE,
                    self.WorkloadPowerProfile.LLM_TRAINING,
                    self.WorkloadPowerProfile.UNDEFINED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.WorkloadPowerProfile,
                default=self.WorkloadPowerProfile.UNDEFINED,
            )
        )
        self.meta.add(
            MetaDataField(
                name="secondaryWorkloadPowerProfile",
                kind=MetaData.Type.ENUM,
                description="Set the clock secondary workload power profile among the GPUs in group",
                options=[
                    self.WorkloadPowerProfile.MAX_P,
                    self.WorkloadPowerProfile.MAX_Q,
                    self.WorkloadPowerProfile.LLM_INFERENCE,
                    self.WorkloadPowerProfile.LLM_TRAINING,
                    self.WorkloadPowerProfile.UNDEFINED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.WorkloadPowerProfile,
                default=self.WorkloadPowerProfile.UNDEFINED,
            )
        )
        self.baseType = 'GPUSettings'
        self.childType = 'NvidiaGPUSettings'
        self.service_type = self.baseType
        self.allTypes = ['NvidiaGPUSettings', 'GPUSettings']
        self.top_level = False
        self.leaf_entity = True

