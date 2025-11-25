from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Job(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_wlm_cluster_uuid",
                kind=MetaData.Type.UUID,
                description="WlmCluster",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_jobqueue_uuid",
                kind=MetaData.Type.UUID,
                description="Queue name",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobID",
                kind=MetaData.Type.STRING,
                description="Job identifier",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="arrayID",
                kind=MetaData.Type.STRING,
                description="Job array identifier",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="taskID",
                kind=MetaData.Type.STRING,
                description="Job array task identifier(s)",
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
                name="jobname",
                kind=MetaData.Type.STRING,
                description="Name of job",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="username",
                kind=MetaData.Type.STRING,
                description="Job owner name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="status",
                kind=MetaData.Type.STRING,
                description="Current job status",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="project",
                kind=MetaData.Type.STRING,
                description="Project name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="priority",
                kind=MetaData.Type.STRING,
                description="Job priority",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="inqueue",
                kind=MetaData.Type.STRING,
                description="Shows whether job has already been queued or not",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.STRING,
                description="Requested nodes",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="cgroup",
                kind=MetaData.Type.STRING,
                description="CGroup allocated for this job on all nodes",
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
                name="executable",
                kind=MetaData.Type.STRING,
                description="File which is executed inside job script",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="arguments",
                kind=MetaData.Type.STRING,
                description="Arguments of executable file",
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
                name="submittime",
                kind=MetaData.Type.STRING,
                description="Job submission time",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="starttime",
                kind=MetaData.Type.STRING,
                description="Job start time (available when job is started)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="endtime",
                kind=MetaData.Type.STRING,
                description="Job end time (available when job is finished or canceled)",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mailOptions",
                kind=MetaData.Type.STRING,
                description="Mail oprions",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mailList",
                kind=MetaData.Type.STRING,
                description="Mail addresses",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mailNotify",
                kind=MetaData.Type.BOOL,
                description="Shows whether mail notification is requested or not",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxWallClock",
                kind=MetaData.Type.STRING,
                description="Maximum available running time",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="runWallClock",
                kind=MetaData.Type.UINT,
                description="Running time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="numberOfProcesses",
                kind=MetaData.Type.UINT,
                description="Number of processes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memoryUse",
                kind=MetaData.Type.UINT,
                description="Memory usage",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="scriptFile",
                kind=MetaData.Type.STRING,
                description="Job script file",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="numberOfNodes",
                kind=MetaData.Type.UINT,
                description="Number of nodes",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="usergroup",
                kind=MetaData.Type.STRING,
                description="Job user group",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="commandLineInterpreter",
                kind=MetaData.Type.STRING,
                description="Command line interpreter",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="dependencies",
                kind=MetaData.Type.STRING,
                description="Job dependencies",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="parallelEnvironment",
                kind=MetaData.Type.STRING,
                description="Parallel environment",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="account",
                kind=MetaData.Type.STRING,
                description="Account name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="resourceList",
                kind=MetaData.Type.STRING,
                description="List of requested resources",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="modules",
                kind=MetaData.Type.STRING,
                description="Environment modules loaded for the script",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="environmentVariables",
                kind=MetaData.Type.STRING,
                description="Additional environment variables",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="debug",
                kind=MetaData.Type.BOOL,
                description="Debug mode (used when new job is submitted via CMDaemon API)",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="userdefined",
                kind=MetaData.Type.STRING,
                description="User defined parameters",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="exitCode",
                kind=MetaData.Type.INT,
                description="Exit code of job",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="minMemPerNode",
                kind=MetaData.Type.UINT,
                description="Minimum memory per node requested",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="comment",
                kind=MetaData.Type.STRING,
                description="Comment set by workload manager",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="placement",
                kind=MetaData.Type.STRING,
                description="Jobs are placed on nodes according to their place statements (useful for PBS, see 'man pbs_resources')",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="pendingReasons",
                kind=MetaData.Type.STRING,
                description="List of pending reasons",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="requestedCPUs",
                kind=MetaData.Type.UINT,
                description="Requested CPUs per node",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="requestedCPUCores",
                kind=MetaData.Type.UINT,
                description="Requested CPU cores per node",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="requestedGPUs",
                kind=MetaData.Type.UINT,
                description="Requested GPUs per node",
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
                name="ref_extra_jobqueue_uuids",
                kind=MetaData.Type.UUID,
                description="Extra queues",
                vector=True,
                default=[],
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
        self.baseType = 'Job'
        self.service_type = self.baseType
        self.allTypes = ['Job']
        self.leaf_entity = False
        self.resolve_field_name = 'jobID'

