from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.wlmcluster import WlmCluster


class LSFWlmCluster(WlmCluster):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="version",
                kind=MetaData.Type.STRING,
                description="Major LSF version",
                options=['10.1'],
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="prefix",
                kind=MetaData.Type.STRING,
                description="LSF installation directory",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="var",
                kind=MetaData.Type.STRING,
                description="Var directory location",
                default="/cm/shared/apps/lsf/var",
            )
        )
        self.meta.add(
            MetaDataField(
                name="localVar",
                kind=MetaData.Type.STRING,
                description="Local var directory location",
                default="/cm/local/apps/lsf/var",
            )
        )
        self.meta.add(
            MetaDataField(
                name="logDir",
                kind=MetaData.Type.STRING,
                description="Logging directory location (LSF_LOGDIR in lsf.conf)",
                default="/cm/local/apps/lsf/var/log",
            )
        )
        self.meta.add(
            MetaDataField(
                name="dynamicCloudNodes",
                kind=MetaData.Type.BOOL,
                description="Cloud nodes are added dynamically to LSF",
                default=False,
            )
        )
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
                description="Submode containing LSF related cgroups settings",
                instance='LSFCgroupsSettings',
                init_instance='LSFCgroupsSettings',
                create_instance=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="doBackups",
                kind=MetaData.Type.BOOL,
                description="Backup configuration file before update",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gpuAutoconfig",
                kind=MetaData.Type.BOOL,
                description="Enable GPU autodetection (LSF_GPU_AUTOCONFIG in lsf.conf)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="gpuNewSyntax",
                kind=MetaData.Type.BOOL,
                description="Enable new GPU request syntax (LSB_GPU_NEW_SYNTAX in lsf.conf)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dcgmPort",
                kind=MetaData.Type.UINT,
                description="Enable DCGM features and specifies the port number that LSF uses to communicate with the DCGM daemon (0 for disabled)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="unitForLimits",
                kind=MetaData.Type.STRING,
                description="Enables scaling of large units in the resource usage limits (LSF_UNIT_FOR_LIMITS in lsf.conf)",
                default="MB",
            )
        )
        self.meta.add(
            MetaDataField(
                name="noQueueHostsString",
                kind=MetaData.Type.STRING,
                description="String that is used to replace empty nodes list for a queue",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="enableEgo",
                kind=MetaData.Type.BOOL,
                description="Enable EGO functionality (LSF_ENABLE_EGO in lsf.conf)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="dynamicHostWaitTime",
                kind=MetaData.Type.UINT,
                description="Defines the length of time in seconds that a dynamic host awaits communicating with the master host LIM to either add the host to the cluster or to shut down any running daemons if the host is not added successfully. Note that the time will be truncated to the minute (LSF_DYNAMIC_HOST_WAIT_TIME in lsf.conf)",
                default=5*3600,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hostAddressRange",
                kind=MetaData.Type.STRING,
                description="Identifies the range of IP addresses that are allowed to be LSF hosts that can be dynamically added to or removed from the cluster (LSF_HOST_ADDR_RANGE in lsf.conf)",
                default="*.*",
            )
        )
        self.meta.add(
            MetaDataField(
                name="manageMIG",
                kind=MetaData.Type.BOOL,
                description="enable dynamic MIG scheduling (LSF_MANAGE_MIG in lsf.conf)",
                default=False,
            )
        )
        self.baseType = 'WlmCluster'
        self.childType = 'LSFWlmCluster'
        self.service_type = self.baseType
        self.allTypes = ['LSFWlmCluster', 'WlmCluster']
        self.top_level = True
        self.leaf_entity = True

