from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CMDaemonFailoverGroupStatus(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="failoverStage",
                kind=MetaData.Type.INT,
                description="Failover stage",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="ref_active_node_uuid",
                kind=MetaData.Type.UUID,
                description="Active node key",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="activeUpTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Active up time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="activeDownTime",
                kind=MetaData.Type.TIMESTAMP,
                description="Active down time",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="activeUpCount",
                kind=MetaData.Type.UINT,
                description="Active up count",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="failoverThreadRunning",
                kind=MetaData.Type.BOOL,
                description="Failover thread running",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="infoMessage",
                kind=MetaData.Type.STRING,
                description="Information messages gather during the last failover",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="errorMessage",
                kind=MetaData.Type.STRING,
                description="Error messages gather during the last failover",
                readonly=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="activeGraciousShutdown",
                kind=MetaData.Type.BOOL,
                description="True if the previous active head reported a graceful shutdown",
                readonly=True,
                default=False,
            )
        )
        self.baseType = 'CMDaemonFailoverGroupStatus'
        self.service_type = self.baseType
        self.allTypes = ['CMDaemonFailoverGroupStatus']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

