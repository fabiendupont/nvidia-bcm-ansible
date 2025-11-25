from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.slurmrole import SlurmRole


class SlurmClientRole(SlurmRole):
    """
    Slurm client role
    """
    class CpuBind(Enum):
        NONE = auto()
        BOARD = auto()
        SOCKET = auto()
        LDOM = auto()
        CORE = auto()
        THREAD = auto()

    class AutoDetectType(Enum):
        NONE = auto()
        OFF = auto()
        NVML = auto()
        RSMI = auto()
        ONEAPI = auto()
        BCM = auto()
        NRT = auto()
        NVIDIA = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="slots",
                kind=MetaData.Type.STRING,
                description="Number of slots available on this node/category (set 0 for default)",
                default="0",
            )
        )
        self.meta.add(
            MetaDataField(
                name="queues",
                kind=MetaData.Type.RESOLVE,
                description="Queues this node/nodes in this category belongs to",
                instance='SlurmJobQueue',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="allQueues",
                kind=MetaData.Type.BOOL,
                description="When set, the role will provide all available queues (the queues property will then be ignored)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeAddr",
                kind=MetaData.Type.STRING,
                description="Name that a node should be referred to in establishing a communications path",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="coresPerSocket",
                kind=MetaData.Type.UINT,
                description="Number of cores in a single physical processor socket",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="features",
                kind=MetaData.Type.STRING,
                description="A list of arbitrary strings indicative of some characteristic associated with the node",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="tcpPort",
                kind=MetaData.Type.UINT,
                description="The port number that the Slurm compute node daemon, slurmd, listens to for work on this particular node",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="realMemory",
                kind=MetaData.Type.UINT,
                description="Size of real memory on the node - The value will be truncated to the MiB",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="sockets",
                kind=MetaData.Type.UINT,
                description="Number of physical processor sockets/chips on the node",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="threadsPerCore",
                kind=MetaData.Type.UINT,
                description="Number of logical threads in a single physical core",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="tmpDisk",
                kind=MetaData.Type.UINT,
                description="Total size of temporary disk storage in TmpFS in MegaBytes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="weight",
                kind=MetaData.Type.INT,
                description="The priority of the node for scheduling purposes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="boards",
                kind=MetaData.Type.UINT,
                description="Number of baseboards in nodes with a baseboard controller",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="socketsPerBoard",
                kind=MetaData.Type.UINT,
                description="Number of physical processor sockets/chips on a baseboard",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="reason",
                kind=MetaData.Type.STRING,
                description="Identifies the reason for a node being in a particular state",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="cpuSpecList",
                kind=MetaData.Type.STRING,
                description="A comma delimited list of Slurm abstract CPU IDs on which Slurm compute node daemons (slurmd, slurmstepd) will be confined",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="coreSpecCount",
                kind=MetaData.Type.UINT,
                description="Number of cores in a single physical processor socket",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memSpecLimit",
                kind=MetaData.Type.UINT,
                description="Limit on combined real memory allocation for compute node daemons (slurmd, slurmstepd)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="autoDetect",
                kind=MetaData.Type.ENUM,
                description="Detect NVIDIA (nvml/nvidia) or AMD (rsmi) or Intel (oneapi) GPUs or AWS Trainium/Inferentia devices (nrt) automatically (per node), or use the cluster manager autodetection (bcm). GPU configuration is part of Slurm GRES.",
                options=[
                    self.AutoDetectType.NONE,
                    self.AutoDetectType.OFF,
                    self.AutoDetectType.NVML,
                    self.AutoDetectType.RSMI,
                    self.AutoDetectType.ONEAPI,
                    self.AutoDetectType.BCM,
                    self.AutoDetectType.NRT,
                    self.AutoDetectType.NVIDIA,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.AutoDetectType,
                default=self.AutoDetectType.NONE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodeCustomizations",
                kind=MetaData.Type.ENTITY,
                description="Slurm node custom properties",
                instance='WlmNodeCustomizationEntry',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="genericResources",
                kind=MetaData.Type.ENTITY,
                description="Slurm generic resources settings",
                instance='SlurmGenericResource',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="cpuBind",
                kind=MetaData.Type.ENUM,
                description="Bindings from task to resources",
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
                name="hardwareAutoDetection",
                kind=MetaData.Type.BOOL,
                description="The actual hardware configuration probed by slurmd -C",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryAutoDetectionSlack",
                kind=MetaData.Type.FLOAT,
                description="Autodetected memory will be reduced by this percentage when put in slurm.conf",
                default=0.1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="IMEX",
                kind=MetaData.Type.BOOL,
                description="Start IMEX daemon from prolog/epilog",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="forceWriteProcs",
                kind=MetaData.Type.BOOL,
                description="Always add Procs to autodetected CPU parameters in slurm.conf",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="useProcsOnly",
                kind=MetaData.Type.BOOL,
                description="Whether only Procs parameter (and not autodetected CPU parameters) will be written in slurm.conf",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodesets",
                kind=MetaData.Type.STRING,
                description="List of nodesets where nodes with this role will be added",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodesetFeatures",
                kind=MetaData.Type.STRING,
                description="List of features that will be added to the Slurm nodes, together with nodesets that will be created in Slurm for these features",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="wpps",
                kind=MetaData.Type.ENTITY,
                description="Workload power profile settings mode",
                instance='WorkloadPowerProfileSettings',
                create_instance=True,
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="addToTopology",
                kind=MetaData.Type.BOOL,
                description="When set, the node is added to topology.conf if topology generation is configured",
                default=True,
            )
        )
        self.baseType = 'Role'
        self.childType = 'SlurmClientRole'
        self.service_type = self.baseType
        self.allTypes = ['SlurmClientRole', 'SlurmRole', 'Role']
        self.top_level = False
        self.leaf_entity = True

