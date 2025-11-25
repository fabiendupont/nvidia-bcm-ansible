from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducerinternal import MonitoringDataProducerInternal


class MonitoringDataProducerProcNetDev(MonitoringDataProducerInternal):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="excludeIf",
                kind=MetaData.Type.STRING,
                description="Exclude interfaces",
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="includeAll",
                kind=MetaData.Type.BOOL,
                description="Include all metrics",
                default=False,
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerProcNetDev'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerProcNetDev', 'MonitoringDataProducerInternal', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

