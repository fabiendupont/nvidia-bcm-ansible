from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.wlmcgroupssettings import WlmCgroupsSettings


class PbsProCgroupsSettings(WlmCgroupsSettings):
    """
    PBS pro cgroups settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="jobCgroupTemplate",
                kind=MetaData.Type.STRING,
                description="Template for job cgroup/v1 path ($ESCAPE_JOBID will be replaced by systemd-escape of job id)",
                default="pbspro.slice/pbspro-$ESCAPE_JOBID.slice",
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobCgroupV2Template",
                kind=MetaData.Type.STRING,
                description="Template for job cgroup/v2 path ($PBS_CGROUPV2_JOBID will be replaced by the proper value in cgroup fs)",
                default="$CGROUP_PREFIX.service/jobs/$PBS_CGROUPV2_JOBID",
            )
        )
        self.meta.add(
            MetaDataField(
                name="cgroupPrefix",
                kind=MetaData.Type.STRING,
                description="Cgroup prefix that used by PBS when the cgroup is created",
                default="pbspro",
            )
        )
        self.meta.add(
            MetaDataField(
                name="enabled",
                kind=MetaData.Type.BOOL,
                description="When set the cgroups hook is enabled (in the hook config: enabled)",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nvidiaSmi",
                kind=MetaData.Type.STRING,
                description="The location of the nvidia-smi command (in the hook config: nvidia-smi)",
                readonly=True,
                default="/usr/bin/nvidia-smi",
            )
        )
        self.meta.add(
            MetaDataField(
                name="killTimeout",
                kind=MetaData.Type.UINT,
                description="Maximum number of seconds the hook spends attempting to kill job processes before destroying cgroups (in the hook config: kill_timeout)",
                default=10,
            )
        )
        self.meta.add(
            MetaDataField(
                name="serverTimeout",
                kind=MetaData.Type.UINT,
                description="Maximum number of seconds the hook spends attempting to fetch node info from the server (in the hook config: server_timeout)",
                default=15,
            )
        )
        self.meta.add(
            MetaDataField(
                name="useHyperthreads",
                kind=MetaData.Type.BOOL,
                description="All CPU threads are made available to jobs (in the hook config: use_hyperthreads)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ncpusAreCores",
                kind=MetaData.Type.BOOL,
                description="ncpus of a vnode is the number of cores, and the hook assigns all threads of each core to a job (in the hook config: ncpus_are_cores)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cpuacctEnabled",
                kind=MetaData.Type.BOOL,
                description="Enable cpuacct cgroup controller for jobs",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cpusetEnabled",
                kind=MetaData.Type.BOOL,
                description="Enable cpuset cgroup controller for jobs",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="devicesEnabled",
                kind=MetaData.Type.BOOL,
                description="Enable devices cgroup controller for jobs",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="devicesAllow",
                kind=MetaData.Type.STRING,
                description="Parameter specifies how access to devices will be controlled",
                vector=True,
                default=["b *:* rwm", "c *:* rwm"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="hugetlbEnabled",
                kind=MetaData.Type.BOOL,
                description="Enable hugetlb cgroup controller for jobs",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hugetlbDefault",
                kind=MetaData.Type.UINT,
                description="The amount of huge page memory assigned to the cgroup when the job does not request hpmem",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hugetlbReservePercent",
                kind=MetaData.Type.UINT,
                description="The percentage of available huge page memory (hpmem) that is not to be assigned to jobs",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hugetlbReserveAmount",
                kind=MetaData.Type.UINT,
                description="An amount of available huge page memory (hpmem) that is not to be assigned to jobs",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryEnabled",
                kind=MetaData.Type.BOOL,
                description="Enable memory cgroup controller for jobs",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memorySoftLimit",
                kind=MetaData.Type.BOOL,
                description="If false PBS uses hard memory limits which prevent the processes from ever exceeding their requested memory usage",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryDefault",
                kind=MetaData.Type.UINT,
                description="Amount of memory assigned to the job if it doesn't request any memory",
                default=256 * 1024 * 1024,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryReservePercent",
                kind=MetaData.Type.UINT,
                description="The percentage of available physical memory that is not to be assigned to jobs",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryReserveAmount",
                kind=MetaData.Type.UINT,
                description="A specific amount of available physical memory that is not to be assigned to jobs",
                default=64 * 1024 * 1024,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memswEnabled",
                kind=MetaData.Type.BOOL,
                description="Enable memsw cgroup controller for jobs",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memswDefault",
                kind=MetaData.Type.UINT,
                description="Specifies the amount of memory + swap assigned to the job if it doesn't request any memory",
                default=256 * 1024 * 1024,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memswReservePercent",
                kind=MetaData.Type.UINT,
                description="Percentage of available swap that is not to be assigned to jobs",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memswReserveAmount",
                kind=MetaData.Type.UINT,
                description="An amount of available swap that is not to be assigned to jobs",
                default=64 * 1024 * 1024,
            )
        )
        self.baseType = 'WlmCgroupsSettings'
        self.childType = 'PbsProCgroupsSettings'
        self.service_type = self.baseType
        self.allTypes = ['PbsProCgroupsSettings', 'WlmCgroupsSettings']
        self.top_level = False
        self.leaf_entity = True

