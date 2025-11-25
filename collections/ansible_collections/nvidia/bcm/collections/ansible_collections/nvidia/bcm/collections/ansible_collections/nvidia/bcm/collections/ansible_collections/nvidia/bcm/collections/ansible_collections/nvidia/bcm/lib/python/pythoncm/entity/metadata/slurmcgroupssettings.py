from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.wlmcgroupssettings import WlmCgroupsSettings


class SlurmCgroupsSettings(WlmCgroupsSettings):
    """
    Slurm cgroups settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="constrainCores",
                kind=MetaData.Type.BOOL,
                description="If true then constrain allowed cores to the subset of allocated resources",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="constrainRAMSpace",
                kind=MetaData.Type.BOOL,
                description="If true then constrain the job's RAM usage",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="constrainSwapSpace",
                kind=MetaData.Type.BOOL,
                description="If true then constrain the job's swap space usage",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="constrainDevices",
                kind=MetaData.Type.BOOL,
                description="If true constrain the job's allowed devices based on GRES allocated resources",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowedRamSpace",
                kind=MetaData.Type.FLOAT,
                description="Constrain the job cgroup RAM to this percentage of the allocated memory. If the AllowedRAMSpace limit is exceeded, the job steps will be killed and a warning message will be written to standard error. Also see ConstrainRAMSpace.",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="allowedSwapSpace",
                kind=MetaData.Type.FLOAT,
                description="Constrain the job cgroup swap space to this percentage of the allocated memory",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxRAM",
                kind=MetaData.Type.FLOAT,
                description="Set an upper bound of total RAM on the RAM constraint for a job",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxSwap",
                kind=MetaData.Type.FLOAT,
                description="Set an upper bound (of total RAM) on the amount of RAM+Swap that may be used for a job",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="minRAMSpace",
                kind=MetaData.Type.UINT,
                description="Set a lower bound on the memory limits defined by AllowedRAMSpace and AllowedSwapSpace",
                default=30 * 1024 * 1024,
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobCgroupTemplate",
                kind=MetaData.Type.STRING,
                description="Template for job cgroup/v1 path ($UID will be replaced to user ID, $JOBID will be replaced to job id)",
                default="slurm/uid_$UID/job_$JOBID",
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobCgroupV2Template",
                kind=MetaData.Type.STRING,
                description="Template for job cgroup/v2 path ($JOBID will be replaced to job id)",
                default="system.slice/slurmstepd.scope/job_$JOBID",
            )
        )
        self.meta.add(
            MetaDataField(
                name="memorySwappiness",
                kind=MetaData.Type.FLOAT,
                description="Configure the kernel's priority for swapping out anonymous pages (such as program data) verses file cache pages for the job cgroup (either ConstrainRAMSpace or ConstrainSwapSpace must be enabled in order for this parameter to be applied)",
                default=1,
            )
        )
        self.baseType = 'WlmCgroupsSettings'
        self.childType = 'SlurmCgroupsSettings'
        self.service_type = self.baseType
        self.allTypes = ['SlurmCgroupsSettings', 'WlmCgroupsSettings']
        self.top_level = False
        self.leaf_entity = True

