from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducer import MonitoringDataProducer


class MonitoringDataProducerJobMetadata(MonitoringDataProducer):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="allowPreAllocate",
                kind=MetaData.Type.BOOL,
                description="Allow pre-allocate of monitoring structures, speeds up for large number of jobs. Disable if measurables per node differ a lot",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeMetrics",
                kind=MetaData.Type.STRING,
                description="Exclude metrics by name from collection",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="includeMetrics",
                kind=MetaData.Type.STRING,
                description="Only these metrics will be samples if the set is not empty",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeUsers",
                kind=MetaData.Type.STRING,
                description="Exclude usage data for the specified users",
                vector=True,
                default=["nfsnobody","nobody"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="includeUsers",
                kind=MetaData.Type.STRING,
                description="Only include usage data for the specified users",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeShell",
                kind=MetaData.Type.STRING,
                description="Exclude usage data for the specified shells",
                vector=True,
                default=["/sbin/nologin","/usr/sbin/nologin"],
            )
        )
        self.meta.add(
            MetaDataField(
                name="minimalUserId",
                kind=MetaData.Type.UINT,
                description="Minumal user ID",
                default=1000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="userCode",
                kind=MetaData.Type.STRING,
                description="Lua code for calculation of extra metric per user",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="storeLastChangeTimestamp",
                kind=MetaData.Type.BOOL,
                description="Add extra metric to store last change timestamp",
                default=False,
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerJobMetadata'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerJobMetadata', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

