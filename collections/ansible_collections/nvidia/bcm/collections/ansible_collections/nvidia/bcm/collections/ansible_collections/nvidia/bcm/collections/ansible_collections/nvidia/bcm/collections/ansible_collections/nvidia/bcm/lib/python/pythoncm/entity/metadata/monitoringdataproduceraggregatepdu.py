from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducerinternal import MonitoringDataProducerInternal


class MonitoringDataProducerAggregatePDU(MonitoringDataProducerInternal):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="maxSampleAge",
                kind=MetaData.Type.FLOAT,
                description="Maximal age of node sample to contribute",
                default=300.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludePDUs",
                kind=MetaData.Type.RESOLVE,
                description="List of PDUs to exclude from the total",
                instance='PowerDistributionUnit',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="extraMeasurables",
                kind=MetaData.Type.RESOLVE,
                description="List of additional measurables to calculate totals for",
                instance='MonitoringMeasurable',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerAggregatePDU'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerAggregatePDU', 'MonitoringDataProducerInternal', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

