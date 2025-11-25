from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class JobInfo(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_wlm_cluster_uuid",
                kind=MetaData.Type.UUID,
                description="The workload cluster on which this node is scheduled",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_jobqueue_uuid",
                kind=MetaData.Type.UUID,
                description="Queue",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobId",
                kind=MetaData.Type.STRING,
                description="Job ID",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobName",
                kind=MetaData.Type.STRING,
                description="Job name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="arrayId",
                kind=MetaData.Type.STRING,
                description="Job array ID",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="taskId",
                kind=MetaData.Type.STRING,
                description="Job task ID",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="user",
                kind=MetaData.Type.STRING,
                description="User name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="group",
                kind=MetaData.Type.STRING,
                description="User group name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="account",
                kind=MetaData.Type.STRING,
                description="Job account",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="accountingInfo",
                kind=MetaData.Type.JSON,
                description="Accounting info",
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.UUID,
                description="List of job's nodes",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_node_monitoring_uuids",
                kind=MetaData.Type.UUID,
                description="Reference to all nodes monitoring UUIDs",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="cgroup",
                kind=MetaData.Type.STRING,
                description="Relative cgroup path",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="submitTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Job submit time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="startTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Job start time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="endTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Job end time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="persistent",
                kind=MetaData.Type.BOOL,
                description="Whether job is persistent in DB or not",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="exitCode",
                kind=MetaData.Type.INT,
                description="Jobscript exit code",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="state",
                kind=MetaData.Type.STRING,
                description="Job status",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="requestedCPUs",
                kind=MetaData.Type.UINT,
                description="Requested CPUs",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="requestedCPUCores",
                kind=MetaData.Type.UINT,
                description="Requested CPU cores",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="requestedGPUs",
                kind=MetaData.Type.UINT,
                description="Requested GPU per node",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="requestedMemory",
                kind=MetaData.Type.UINT,
                description="Requested memory per node",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="requestedSlots",
                kind=MetaData.Type.UINT,
                description="Requested slots",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="monitoring",
                kind=MetaData.Type.BOOL,
                description="Whether job still has monitoring data",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="comment",
                kind=MetaData.Type.STRING,
                description="Comment",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="rundirectory",
                kind=MetaData.Type.STRING,
                description="Job work directory",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="stdinfile",
                kind=MetaData.Type.STRING,
                description="Standard input file",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="stdoutfile",
                kind=MetaData.Type.STRING,
                description="Standard output file",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="stderrfile",
                kind=MetaData.Type.STRING,
                description="Standard error file",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalPowerUsage",
                kind=MetaData.Type.FLOAT,
                description="Total power usage over all nodes in the job over the runtime of the job",
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalPowerUsageGPU",
                kind=MetaData.Type.FLOAT,
                description="Total power usage over all GPUs in the job over the runtime of the job",
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalPowerUsageCPU",
                kind=MetaData.Type.FLOAT,
                description="Total power usage over all CPUs in the job over the runtime of the job",
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="totalPowerUnderAllocation",
                kind=MetaData.Type.FLOAT,
                description="Total power under alloction of devices over the runtime of the job",
                default=-1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="qos",
                kind=MetaData.Type.STRING,
                description="Quality of service",
                default='',
            )
        )
        self.baseType = 'JobInfo'
        self.service_type = self.baseType
        self.allTypes = ['JobInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

