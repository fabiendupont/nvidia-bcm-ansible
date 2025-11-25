from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.jobqueue import JobQueue


class SlurmJobQueue(JobQueue):
    """
    Slurm job queues
    """
    class CpuBind(Enum):
        NONE = auto()
        BOARD = auto()
        SOCKET = auto()
        LDOM = auto()
        CORE = auto()
        THREAD = auto()

    class QueueState(Enum):
        NONE = auto()
        UP = auto()
        DOWN = auto()
        DRAIN = auto()
        INACTIVE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="defaultQueue",
                kind=MetaData.Type.BOOL,
                description="Set this as the default queue",
                clone=False,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="minNodes",
                kind=MetaData.Type.STRING,
                description="Minimal nodes one job has to use",
                default="1",
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxNodes",
                kind=MetaData.Type.STRING,
                description="Maximal nodes one job can use",
                default="UNLIMITED",
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultTime",
                kind=MetaData.Type.STRING,
                description="Default job runtime",
                default="UNLIMITED",
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxTime",
                kind=MetaData.Type.STRING,
                description="Maximal job runtime",
                default="UNLIMITED",
            )
        )
        self.meta.add(
            MetaDataField(
                name="priorityJobFactor",
                kind=MetaData.Type.INT,
                description="Partition factor used by priority/multifactor plugin in calculating job priority",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="priorityTier",
                kind=MetaData.Type.INT,
                description="Jobs submitted to a partition with a higher priority tier value will be dispatched before pending jobs in partition with lower priority tier value",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hidden",
                kind=MetaData.Type.BOOL,
                description="Hide from all",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="disableRoot",
                kind=MetaData.Type.BOOL,
                description="Do not allow root to run jobs",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rootOnly",
                kind=MetaData.Type.BOOL,
                description="Only allow root to run jobs",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowGroups",
                kind=MetaData.Type.STRING,
                description="Specify user groups which are allowed to run jobs",
                default="ALL",
            )
        )
        self.meta.add(
            MetaDataField(
                name="overSubscribe",
                kind=MetaData.Type.STRING,
                description="Controls the ability of the partition to execute more than one job at a time on each resource",
                default="NO",
            )
        )
        self.meta.add(
            MetaDataField(
                name="alternate",
                kind=MetaData.Type.STRING,
                description="Partition name of alternate partition to be used if the state of this partition is DRAIN or INACTIVE",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="graceTime",
                kind=MetaData.Type.UINT,
                description="Specifies, in units of seconds, the preemption grace time to be extended to a job which has been selected for preemption",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="defMemPerCPU",
                kind=MetaData.Type.STRING,
                description="Default real memory size available per allocated CPU in MegaBytes",
                default="UNLIMITED",
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxMemPerCPU",
                kind=MetaData.Type.STRING,
                description="Maximum real memory size available per allocated CPU in MegaBytes",
                default="UNLIMITED",
            )
        )
        self.meta.add(
            MetaDataField(
                name="defMemPerNode",
                kind=MetaData.Type.STRING,
                description="Default real memory size available per allocated node in MegaBytes",
                default="UNLIMITED",
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxMemPerNode",
                kind=MetaData.Type.STRING,
                description="Maximum real memory size available per allocated node in MegaBytes",
                default="UNLIMITED",
            )
        )
        self.meta.add(
            MetaDataField(
                name="preemptMode",
                kind=MetaData.Type.STRING,
                description="Mechanism used to preempt jobs from this partition",
                default="OFF",
            )
        )
        self.meta.add(
            MetaDataField(
                name="reqResv",
                kind=MetaData.Type.STRING,
                description="Specifies users of this partition are required to designate a reservation when submitting a job",
                default="NO",
            )
        )
        self.meta.add(
            MetaDataField(
                name="SelectTypeParameters",
                kind=MetaData.Type.STRING,
                description="Partition-specific resource allocation type",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowAccounts",
                kind=MetaData.Type.STRING,
                description="Specify accounts which are allowed to run jobs",
                default="ALL",
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowQos",
                kind=MetaData.Type.STRING,
                description="Specify qos which are allowed to run jobs",
                default="ALL",
            )
        )
        self.meta.add(
            MetaDataField(
                name="denyAccounts",
                kind=MetaData.Type.STRING,
                description="Specify accounts which are denied to run jobs",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="denyQos",
                kind=MetaData.Type.STRING,
                description="Specify qos which are denied to run jobs",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="lln",
                kind=MetaData.Type.BOOL,
                description="Schedule resources to jobs on the least loaded nodes",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxCPUsPerNode",
                kind=MetaData.Type.STRING,
                description="Maximum number of CPUs on any node available to all jobs from this partition",
                default="UNLIMITED",
            )
        )
        self.meta.add(
            MetaDataField(
                name="tresBillingWeights",
                kind=MetaData.Type.STRING,
                description="Billing weights of each TRES type that will be used in calculating the usage of a job",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="defMemPerGPU",
                kind=MetaData.Type.STRING,
                description="Default  real  memory  size  available  per  allocated GPU in megabytes",
                default="UNLIMITED",
            )
        )
        self.meta.add(
            MetaDataField(
                name="defCpuPerGPU",
                kind=MetaData.Type.STRING,
                description="Default count of CPUs allocated per allocated GPU",
                default="UNLIMITED",
            )
        )
        self.meta.add(
            MetaDataField(
                name="cpuBind",
                kind=MetaData.Type.ENUM,
                description="How tasks are bound to allocated CPUs",
                options=[
                    self.CpuBind.NONE,
                    self.CpuBind.BOARD,
                    self.CpuBind.SOCKET,
                    self.CpuBind.LDOM,
                    self.CpuBind.CORE,
                    self.CpuBind.THREAD,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.CpuBind,
                default=self.CpuBind.NONE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="qos",
                kind=MetaData.Type.STRING,
                description="Used to extend the limits available to a QOS on a partition",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="exclusiveUser",
                kind=MetaData.Type.BOOL,
                description="If set to YES then nodes will be exclusively allocated to users",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ordering",
                kind=MetaData.Type.INT,
                description="Positioning of the jobqueue. Smaller values go first in the configuration file.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="allocNodes",
                kind=MetaData.Type.RESOLVE,
                description="Nodes from which users can submit jobs in the partition of managed nodes",
                instance='Node',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="state",
                kind=MetaData.Type.ENUM,
                description="State of partition or availability for use.",
                options=[
                    self.QueueState.NONE,
                    self.QueueState.UP,
                    self.QueueState.DOWN,
                    self.QueueState.DRAIN,
                    self.QueueState.INACTIVE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.QueueState,
                default=self.QueueState.NONE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodesets",
                kind=MetaData.Type.STRING,
                description="List of nodesets that will be added to Slurm partition",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'JobQueue'
        self.childType = 'SlurmJobQueue'
        self.service_type = self.baseType
        self.allTypes = ['SlurmJobQueue', 'JobQueue']
        self.top_level = True
        self.leaf_entity = True

