from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.jobqueue import JobQueue


class LSFBaseJobQueue(JobQueue):
    """
    LSF base job queues
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="administrators",
                kind=MetaData.Type.STRING,
                description="List of queue administrators.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="corelimit",
                kind=MetaData.Type.UINT,
                description="The per-process core file size limit (in KB) for all of the processes belonging to a job from this queue.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cpulimit",
                kind=MetaData.Type.STRING,
                description="Maximum normalized CPU time and optionally, the default normalized CPU time allowed for all processes of a job running in this queue; value format: [default_limit] maximum_limit.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="chkPnt",
                kind=MetaData.Type.STRING,
                description="Enables automatic checkpointing; value format: dir [period], where dir is the directory where the checkpoint files are created (do not use environment variables); period is the checkpoint period in minutes.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="datalimit",
                kind=MetaData.Type.UINT,
                description="The per-process data segment size limit (in KB) for all of the processes belonging to a job from this queue.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="description",
                kind=MetaData.Type.STRING,
                description="Description of the queue that will be displayed by 'bqueues -l'",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="default_host_spec",
                kind=MetaData.Type.STRING,
                description="The default CPU time normalization host for the queue.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="dispatch_window",
                kind=MetaData.Type.STRING,
                description="The time windows in which jobs from this queue are dispatched.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="exclusive",
                kind=MetaData.Type.STRING,
                description="If Y, specifies an exclusive queue. Jobs submitted to an exclusive queue with 'bsub -x' will only be despatched to a host that has no other LSF jobs running.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="filelimit",
                kind=MetaData.Type.UINT,
                description="The per-process file size limit (in KB) for all of the processes belonging to a job from this queue.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hjob_limit",
                kind=MetaData.Type.UINT,
                description="Maximum number of job slots that this queue can use on any host.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="hosts",
                kind=MetaData.Type.STRING,
                description="A space-separated list of hosts, host groups, and host partitions on which jobs from this queue can be run.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ignore_deadline",
                kind=MetaData.Type.STRING,
                description="If Y, disables deadline constraint scheduling (starts all jobs regardless of deadline constraints).",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="interactive",
                kind=MetaData.Type.STRING,
                description="Causes the queue to reject interactive batch jobs (NO) or accept nothing but interactive batch jobs (ONLY). Interactive batch jobs are submitted via 'bsub -I'.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="job_accept_interval",
                kind=MetaData.Type.UINT,
                description="The number of dispatch turns to wait after dispatching a job to a host, before dispatching a second job to the same host.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="job_controls",
                kind=MetaData.Type.STRING,
                description="Changes the behaviour of the SUSPEND, RESUME, and TERMINATE actions.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="pre_post_exec_user",
                kind=MetaData.Type.STRING,
                description="Username for prolog and epilog execution.",
                default="root",
            )
        )
        self.meta.add(
            MetaDataField(
                name="prolog",
                kind=MetaData.Type.STRING,
                description="Path to prolog script (pre_exec).",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="epilog",
                kind=MetaData.Type.STRING,
                description="Path to epilog script (post_exec).",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="hostProlog",
                kind=MetaData.Type.STRING,
                description="Path to per host prolog script (host_pre_exec).",
                default="/cm/local/apps/cmd/scripts/prolog",
            )
        )
        self.meta.add(
            MetaDataField(
                name="hostEpilog",
                kind=MetaData.Type.STRING,
                description="Path to per host epilog script (host_post_exec).",
                default="/cm/local/apps/cmd/scripts/epilog",
            )
        )
        self.meta.add(
            MetaDataField(
                name="job_starter",
                kind=MetaData.Type.STRING,
                description="Creates a specific environment for submitted jobs prior to execution.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="load_index",
                kind=MetaData.Type.STRING,
                description="Scheduling and suspending thresholds for the specifed dynamic load index.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="memlimit",
                kind=MetaData.Type.STRING,
                description="The per-process memory resident set size limit (in KB) for all of the processes belonging to a job from this queue. Format is '[default_limit] maximum_limit'.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mig",
                kind=MetaData.Type.UINT,
                description="Enables automatic job migration and specifies the migration threshold, in minutes.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="new_job_sched_delay",
                kind=MetaData.Type.UINT,
                description="The maximum or minimum length of time that a new job waits before being dispatched; the behavior depends on whether the delay period specified is longer or shorter than a regular dispatch interval (MBD_SLEEP_TIME in lsb.params, 60 seconds by default).",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nice",
                kind=MetaData.Type.UINT,
                description="Adjusts the Unix scheduling priority at which jobs from this queue execute.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pjob_limit",
                kind=MetaData.Type.UINT,
                description="The per-processor job slot limit for the queue.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="processlimit",
                kind=MetaData.Type.STRING,
                description="Limits the number of concurrent processes that can be part of a job.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="proclimit",
                kind=MetaData.Type.STRING,
                description="Limits the number of processors that can be allocated to the job.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="priority",
                kind=MetaData.Type.UINT,
                description="Queue priority.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="qjob_limit",
                kind=MetaData.Type.UINT,
                description="Job slot limit for the queue. Total number of job slots this queue can use.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="rerunnable",
                kind=MetaData.Type.STRING,
                description="If yes, enables automatic job rerun (restart).",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="require_exit_values",
                kind=MetaData.Type.STRING,
                description="The exit codes that will cause the job to be requeued.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="res_req",
                kind=MetaData.Type.STRING,
                description="Resource requirements used to determine eligible hosts.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="resume_cond",
                kind=MetaData.Type.STRING,
                description="Use the select section of the resource requirement string to specify load thresholds. All other sections are ignored.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="run_window",
                kind=MetaData.Type.STRING,
                description="Time period during which jobs in the queue are allowed to run.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="runlimit",
                kind=MetaData.Type.STRING,
                description="The maximum run limit and optionally the default run limit. Value format: [default_limit] maximum_limit.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="slot_reserve",
                kind=MetaData.Type.UINT,
                description="Enables processor reservation and specifies the number of dispatch turns over which a parallel job can reserve job slots.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="stacklimit",
                kind=MetaData.Type.UINT,
                description="The per-process stack segment size limit (in KB) for all of the processes belonging to a job from this queue.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="stop_cond",
                kind=MetaData.Type.STRING,
                description="Use the select section of the resource requirement string to specify load thresholds. All other sections are ignored.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="swaplimit",
                kind=MetaData.Type.UINT,
                description="The amount of total virtual memory limit (in KB) for a job from this queue.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="terminate_when",
                kind=MetaData.Type.STRING,
                description="Configures the queue to invoke the TERMINATE action instead of the SUSPEND action in the specified circumstance.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ujob_limit",
                kind=MetaData.Type.UINT,
                description="The per-user job slot limit for the queue. Maximum number of slots that each user can use in this queue.",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="users",
                kind=MetaData.Type.STRING,
                description="A list of users or user groups that can submit jobs to this queue. Use the reserved word all to specify all users.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="r15s",
                kind=MetaData.Type.STRING,
                description="Built-in load index: run queue length (15 sec average).",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="r1m",
                kind=MetaData.Type.STRING,
                description="Built-in load index: run queue length (1 min average).",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="r15m",
                kind=MetaData.Type.STRING,
                description="Built-in load index: run queue length (15 min average).",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="it",
                kind=MetaData.Type.STRING,
                description="Built-in load index: idle time.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="io",
                kind=MetaData.Type.STRING,
                description="Built-in load index: disk I/O.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ut",
                kind=MetaData.Type.STRING,
                description="Built-in load index: CPU utilization.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="mem",
                kind=MetaData.Type.STRING,
                description="Built-in load index: available memory (in MB).",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="pg",
                kind=MetaData.Type.STRING,
                description="Built-in load index: pages in + pages out.",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="tmp",
                kind=MetaData.Type.STRING,
                description="Built-in load index: available space in temporary file system (MB).",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="swp",
                kind=MetaData.Type.STRING,
                description="Built-in load index: available swap space (in MB).",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="ls",
                kind=MetaData.Type.STRING,
                description="Built-in load index.",
                default='',
            )
        )
        self.baseType = 'JobQueue'
        self.childType = 'LSFBaseJobQueue'
        self.service_type = self.baseType
        self.allTypes = ['LSFBaseJobQueue', 'JobQueue']
        self.leaf_entity = False

