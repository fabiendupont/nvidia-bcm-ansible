from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducerinternal import MonitoringDataProducerInternal


class MonitoringDataProducerProcPidStat(MonitoringDataProducerInternal):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="pid",
                kind=MetaData.Type.UINT,
                description="PID to sample",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="process",
                kind=MetaData.Type.STRING,
                description="Process name",
                default='',
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerProcPidStat'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerProcPidStat', 'MonitoringDataProducerInternal', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

