from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CMDaemonStatus(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="version",
                kind=MetaData.Type.STRING,
                description="CMDaemon version",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="state",
                kind=MetaData.Type.STRING,
                description="CMDaemon state",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="myTime",
                kind=MetaData.Type.TIMESTAMP,
                description="System time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="startTime",
                kind=MetaData.Type.TIMESTAMP,
                description="CMDaemon start time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="uptime",
                kind=MetaData.Type.UINT,
                description="System uptime",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="utime",
                kind=MetaData.Type.FLOAT,
                description="User time spend by CMDaemon",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="stime",
                kind=MetaData.Type.FLOAT,
                description="System time spend by CMDaemon",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="memused",
                kind=MetaData.Type.UINT,
                description="Memory used by CMDaemon",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="sessionCount",
                kind=MetaData.Type.UINT,
                description="Total Number of cmsh/cmgui/python/node sessions",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="activeSessionCount",
                kind=MetaData.Type.UINT,
                description="Number of currently active sessions",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="httpdNumWorkers",
                kind=MetaData.Type.UINT,
                description="Number of threads handing http requests",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="httpdNumFreeWorkers",
                kind=MetaData.Type.UINT,
                description="Number of threads free to handle http requests",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="httpdConnectionCounter",
                kind=MetaData.Type.UINT,
                description="Total number of http connections handled by CMDaemon",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="httpdRequestCounter",
                kind=MetaData.Type.UINT,
                description="Total number of http request handled by CMDaemon",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="httpdBytesRead",
                kind=MetaData.Type.UINT,
                description="Bytes read from http request",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="httpdBytesWritten",
                kind=MetaData.Type.UINT,
                description="Bytes written in response to http requests",
                default=0,
            )
        )
        self.baseType = 'CMDaemonStatus'
        self.service_type = self.baseType
        self.allTypes = ['CMDaemonStatus']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

