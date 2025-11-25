from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.wlmcluster import WlmCluster


class SlurmWlmCluster(WlmCluster):
    class AutoDetectType(Enum):
        NONE = auto()
        OFF = auto()
        NVML = auto()
        RSMI = auto()
        ONEAPI = auto()
        BCM = auto()
        NRT = auto()
        NVIDIA = auto()

    class SlurmDrainReasonPolicy(Enum):
        REPLACE = auto()
        APPEND = auto()
        SKIP = auto()

    class CgroupPluginType(Enum):
        CGROUPV1 = auto()
        CGROUPV2 = auto()
        AUTODETECT = auto()
        DISABLED = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="placeholders",
                kind=MetaData.Type.ENTITY,
                description="Job queue node placeholders mode",
                instance='JobQueuePlaceholder',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="cgroups",
                kind=MetaData.Type.ENTITY,
                description="Submode containing Slurm related cgroups settings",
                instance='SlurmCgroupsSettings',
                init_instance='SlurmCgroupsSettings',
                create_instance=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerSavingEnabled",
                kind=MetaData.Type.BOOL,
                description="Enable power saving options into slurm.conf",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="suspendTime",
                kind=MetaData.Type.INT,
                description=" Nodes which remain idle for this number of seconds will be placed into power save mode by SuspendProgram",
                default=300,
            )
        )
        self.meta.add(
            MetaDataField(
                name="suspendTimeout",
                kind=MetaData.Type.UINT,
                description="Maximum time permitted (in second) between when a node suspend request is issued and when the node shutdown",
                default=30,
            )
        )
        self.meta.add(
            MetaDataField(
                name="resumeTimeout",
                kind=MetaData.Type.UINT,
                description="Maximum time permitted (in second) between when a node is resume request is issued and when the node is actually available for use",
                default=60,
            )
        )
        self.meta.add(
            MetaDataField(
                name="suspendProgram",
                kind=MetaData.Type.STRING,
                description="Program that will be executed when a node remains idle for an extended period of time",
                default="/cm/local/apps/slurm/current/scripts/power/poweroff",
            )
        )
        self.meta.add(
            MetaDataField(
                name="resumeProgram",
                kind=MetaData.Type.STRING,
                description="Program that will be executed when a suspended node is needed by a submitted jobs",
                default="/cm/local/apps/slurm/current/scripts/power/poweron",
            )
        )
        self.meta.add(
            MetaDataField(
                name="prologSlurmctld",
                kind=MetaData.Type.STRING,
                description="Fully qualified pathname of a program for the slurmctld daemon to execute before granting a new job allocation",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="epilogSlurmctld",
                kind=MetaData.Type.STRING,
                description="Fully qualified pathname of a program for the slurmctld to execute upon termination of a job allocation",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="prolog",
                kind=MetaData.Type.STRING,
                description="Fully qualified pathname of a program for the slurmd to execute whenever it is asked to run a job step from a new job allocation",
                default="/cm/local/apps/cmd/scripts/prolog",
            )
        )
        self.meta.add(
            MetaDataField(
                name="epilog",
                kind=MetaData.Type.STRING,
                description="Fully qualified pathname of a script to execute as user root on every node when a user's job completes",
                default="/cm/local/apps/cmd/scripts/epilog",
            )
        )
        self.meta.add(
            MetaDataField(
                name="taskProlog",
                kind=MetaData.Type.STRING,
                description="Fully qualified pathname of a script to execute prior to launching job step (invoked by slurmstepd).",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="taskEpilog",
                kind=MetaData.Type.STRING,
                description="Fully qualified pathname of a script to execute after completion of job step (invoked by slurmstepd).",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="srunProlog",
                kind=MetaData.Type.STRING,
                description="Fully qualified pathname of a script to execute prior to launching job step (invoked by srun).",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="srunEpilog",
                kind=MetaData.Type.STRING,
                description="Fully qualified pathname of a script to execute after completion of job step (invoked by srun).",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="gresTypes",
                kind=MetaData.Type.STRING,
                description="A list of generic resources to be managed",
                vector=True,
                default=["gpu"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="prologEpilogTimeout",
                kind=MetaData.Type.UINT,
                description="The interval in seconds Slurm waits for Prolog and Epilog before terminating them (value 0 removes the parameter from slurm.conf)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="batchStartTimeout",
                kind=MetaData.Type.UINT,
                description="The maximum time (in seconds) that a batch job is permitted for launching before being considered missing and releasing the allocation (value 0 removes the parameter from slurm.conf)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="prefix",
                kind=MetaData.Type.STRING,
                description="Slurm root installation directory",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="etc",
                kind=MetaData.Type.STRING,
                description="Slurm configuration files directory",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="stateSave",
                kind=MetaData.Type.STRING,
                description="Directory into which the Slurm controller saves its state",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="version",
                kind=MetaData.Type.STRING,
                description="Major Slurm version",
                options=[
                    '24.05',
                    '24.05-sharp',
                    '24.11',
                    '24.11-sharp',
                    '25.05',
                    '25.05-sharp',
                ],
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="slurmConfFileTemplate",
                kind=MetaData.Type.STRING,
                description="Template for slurm.conf file",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="gresConfFileTemplate",
                kind=MetaData.Type.STRING,
                description="Template for gres.conf file",
                default='',
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
                name="configureMigs",
                kind=MetaData.Type.BOOL,
                description="Detect and configure MIG profiles as GPU types in Slurm",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="slurmdParameters",
                kind=MetaData.Type.STRING,
                description="Parameters specific to the Slurmd",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="scheduler",
                kind=MetaData.Type.STRING,
                description="Scheduler to use in combination with slurm",
                options=[
                    'backfill',
                    'builtin',
                ],
                default="backfill",
            )
        )
        self.meta.add(
            MetaDataField(
                name="schedulerParameters",
                kind=MetaData.Type.STRING,
                description="Parameters specific to the scheduler. The interpretation of them varies by SchedulerType",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="slurmctldParameters",
                kind=MetaData.Type.STRING,
                description="Parameters specific to the Slurmctld",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="prologFlags",
                kind=MetaData.Type.STRING,
                description="Flags to control the prolog behavior",
                vector=True,
                default=["Alloc"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="selectType",
                kind=MetaData.Type.STRING,
                description="The type of resource selection algorithm to be used (slurm: SelectType)",
                default="select/cons_tres",
            )
        )
        self.meta.add(
            MetaDataField(
                name="selectTypeParameters",
                kind=MetaData.Type.STRING,
                description="Parameters specific to Select Type (slurm: SelectTypeParameters)",
                vector=True,
                default=["CR_Core"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="accountingStorageTRES",
                kind=MetaData.Type.STRING,
                description="List of resources you wish to track on the cluster (slurm: AccountingStorageTRES)",
                vector=True,
                default=["gres/gpu"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="accountingStoreFlags",
                kind=MetaData.Type.STRING,
                description="List used to tell the slurmctld to store extra fields that may be more heavy weight than the normal job information (slurm: AccoutingStoreFlags)",
                vector=True,
                default=["job_comment"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="ociSettings",
                kind=MetaData.Type.ENTITY,
                description="OCI container settings for Slurm",
                instance='SlurmOCISettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="drainReasonPolicy",
                kind=MetaData.Type.ENUM,
                description="The policy defines how a new drain reason is applied when another one already presents",
                options=[
                    self.SlurmDrainReasonPolicy.REPLACE,
                    self.SlurmDrainReasonPolicy.APPEND,
                    self.SlurmDrainReasonPolicy.SKIP,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.SlurmDrainReasonPolicy,
                default=self.SlurmDrainReasonPolicy.REPLACE,
            )
        )
        self.meta.add(
            MetaDataField(
                name="topologySettings",
                kind=MetaData.Type.ENTITY,
                description="Topology settings for Slurm",
                instance='SlurmTopologySettings',
                init_instance='SlurmTopologySettings',
                create_instance=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="bcmManagedParameters",
                kind=MetaData.Type.STRING,
                description="Fields in slurm.conf that will be controlled by cmdaemon (case insensitive)",
                vector=True,
                default=["AccountingStorageBackupHost","AccountingStorageHost","AccountingStorageTRES","AccountingStoreFlags","BatchStartTimeout","ClusterName","Epilog","EpilogSlurmctld","GresTypes","Licenses","Prolog","PrologEpilogTimeout","PrologFlags","PrologSlurmctld","ResumeProgram","ResumeTimeout","SchedulerParameters","SchedulerType","SelectType","SelectTypeParameters","SlurmctldAddr","SlurmctldHost","SlurmctldParameters","SlurmdParameters","SrunEpilog","SrunProlog","StateSaveLocation","SuspendProgram","SuspendTime","SuspendTimeout","TaskEpilog","TaskProlog","TopologyParam","TopologyPlugin"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="prsSettings",
                kind=MetaData.Type.ENTITY,
                description="PRS settings for Slurm",
                instance='SlurmPRSSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="licenses",
                kind=MetaData.Type.ENTITY,
                description="Specification of licenses (or other resources available on all nodes of the cluster) which can be allocated to jobs.",
                instance='SlurmLicense',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="cgroupPlugin",
                kind=MetaData.Type.ENUM,
                description="Specify the plugin to be used when interacting with the cgroup subsystem.",
                options=[
                    self.CgroupPluginType.CGROUPV1,
                    self.CgroupPluginType.CGROUPV2,
                    self.CgroupPluginType.AUTODETECT,
                    self.CgroupPluginType.DISABLED,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.CgroupPluginType,
                default=self.CgroupPluginType.AUTODETECT,
            )
        )
        self.baseType = 'WlmCluster'
        self.childType = 'SlurmWlmCluster'
        self.service_type = self.baseType
        self.allTypes = ['SlurmWlmCluster', 'WlmCluster']
        self.top_level = True
        self.leaf_entity = True

