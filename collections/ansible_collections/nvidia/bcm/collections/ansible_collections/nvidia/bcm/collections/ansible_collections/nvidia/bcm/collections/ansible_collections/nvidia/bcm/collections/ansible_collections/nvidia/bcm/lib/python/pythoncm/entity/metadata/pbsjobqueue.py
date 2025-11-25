from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.jobqueue import JobQueue


class PBSJobQueue(JobQueue):
    """
    PBS job queue
    """
    class PbsProQueueType(Enum):
        EXECUTION = auto()
        ROUTE = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="queueType",
                kind=MetaData.Type.ENUM,
                description="Pbs Pro queue type",
                options=[
                    self.PbsProQueueType.EXECUTION,
                    self.PbsProQueueType.ROUTE,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.PbsProQueueType,
                default=self.PbsProQueueType.EXECUTION,
            )
        )
        self.meta.add(
            MetaDataField(
                name="fromRouteOnly",
                kind=MetaData.Type.BOOL,
                description="Receive jobs from route queues only",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="routeHeldJobs",
                kind=MetaData.Type.BOOL,
                description="Specifies whether jobs in the held state can be routed from this queue",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="routeWaitingJobs",
                kind=MetaData.Type.BOOL,
                description="Specifies whether jobs whose execution_time attribute value is in the future can be routed from this queue",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="routeLifetime",
                kind=MetaData.Type.UINT,
                description="The maximum time a job is allowed to reside in a routing queue",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="routeRetryTime",
                kind=MetaData.Type.UINT,
                description="Route retry time in routing queue",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="routes",
                kind=MetaData.Type.STRING,
                description="Route of queue path (route_destination parameter in qmgr)",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultQueue",
                kind=MetaData.Type.BOOL,
                description="Specifies the queue which is to accept jobs when no queue is requested",
                clone=False,
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="minWalltime",
                kind=MetaData.Type.STRING,
                description="Minimum runtime of jobs running in a queue",
                default="00:00:00",
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxWalltime",
                kind=MetaData.Type.STRING,
                description="Maximum runtime of jobs running in a queue",
                default="240:00:00",
            )
        )
        self.meta.add(
            MetaDataField(
                name="defaultWalltime",
                kind=MetaData.Type.STRING,
                description="Default maximum runtime of jobs running in a queue",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxQueued",
                kind=MetaData.Type.UINT,
                description="Maximum number allowed to reside in a queue at any given time (0 is the same as infinite)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxRunning",
                kind=MetaData.Type.UINT,
                description="Maximum number of jobs allowed to run at any given time (0 is the same as infinite)",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="priority",
                kind=MetaData.Type.INT,
                description="Priority of a queue against other queues of the same type [-1024; 1024]",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="enabled",
                kind=MetaData.Type.BOOL,
                description="When true, a queue will accept new jobs; when false, a queue is disabled and will not accept jobs",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="started",
                kind=MetaData.Type.BOOL,
                description="Jobs may be scheduled for execution from this queue; when false, a queue is considered stopped",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="aclHostEnable",
                kind=MetaData.Type.BOOL,
                description="When true directs the server to use the acl_hosts access list for the named queue",
                default=False,
            )
        )
        self.baseType = 'JobQueue'
        self.childType = 'PBSJobQueue'
        self.service_type = self.baseType
        self.allTypes = ['PBSJobQueue', 'JobQueue']
        self.leaf_entity = False

