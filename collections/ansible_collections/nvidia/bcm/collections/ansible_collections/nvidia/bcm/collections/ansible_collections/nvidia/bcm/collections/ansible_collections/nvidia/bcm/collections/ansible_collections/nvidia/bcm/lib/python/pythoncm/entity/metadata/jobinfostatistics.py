from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class JobInfoStatistics(Entity):
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
                description="Queue",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="user",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="group",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="account",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="accountingInfo",
                kind=MetaData.Type.JSON,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="intervalStart",
                kind=MetaData.Type.TIMESTAMP,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="intervalEnd",
                kind=MetaData.Type.TIMESTAMP,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pending",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="running",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="finished",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="error",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="total",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="pendingTime",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="runningTime",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="finishedTime",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="errorTime",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxRunning",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.baseType = 'JobInfoStatistics'
        self.service_type = self.baseType
        self.allTypes = ['JobInfoStatistics']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

