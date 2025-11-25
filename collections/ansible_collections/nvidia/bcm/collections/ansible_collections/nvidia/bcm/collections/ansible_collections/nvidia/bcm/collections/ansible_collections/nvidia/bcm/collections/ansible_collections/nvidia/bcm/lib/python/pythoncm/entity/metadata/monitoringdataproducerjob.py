from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducer import MonitoringDataProducer


class MonitoringDataProducerJob(MonitoringDataProducer):
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
                name="metricSettings",
                kind=MetaData.Type.ENTITY,
                description="Submode containing job metric settings",
                instance='MonitoringJobMetricSettings',
                init_instance='MonitoringJobMetricSettings',
                create_instance=True,
                default=None,
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerJob'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerJob', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

