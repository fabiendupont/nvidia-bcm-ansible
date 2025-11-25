from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.wlmcgroupssettings import WlmCgroupsSettings


class LSFCgroupsSettings(WlmCgroupsSettings):
    """
    LSF cgroups settings
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="resourceEnforce",
                kind=MetaData.Type.STRING,
                description="Controls resource enforcement through the Linux cgroup memory and cpuset subsytem on Linux systems with cgroup support (LSB_RESOURCE_ENFORCE)",
                vector=True,
                default=["memory","cpu"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="processTracking",
                kind=MetaData.Type.BOOL,
                description="Enable this parameter to track processes based on job control functions such as termination, suspension, resume and other signaling, on Linux systems which support cgroups freezer subsystem (LSF_PROCESS_TRACKING)",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="linuxCgroupAccounting",
                kind=MetaData.Type.BOOL,
                description="Enable this parameter to track processes based on CPU and memory accounting for Linux systems that support cgroup's memory and cpuacct subsystems (LSF_LINUX_CGROUP_ACCT)",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobCgroupTemplate",
                kind=MetaData.Type.STRING,
                description="Template for job cgroup path ($CLUSTER will be replaced to LSF cluster name, $JOBID will be replaced to job id)",
                default="lsf/$CLUSTER/job.$JOBID.*",
            )
        )
        self.baseType = 'WlmCgroupsSettings'
        self.childType = 'LSFCgroupsSettings'
        self.service_type = self.baseType
        self.allTypes = ['LSFCgroupsSettings', 'WlmCgroupsSettings']
        self.top_level = False
        self.leaf_entity = True

