from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducerinternal import MonitoringDataProducerInternal


class MonitoringDataProducerAggregatePowerShelf(MonitoringDataProducerInternal):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="maxSampleAge",
                kind=MetaData.Type.FLOAT,
                description="Maximal age of switch sample to contribute",
                default=300.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="degradedLimit",
                kind=MetaData.Type.FLOAT,
                description="Number of PSU that need to be down before the rack is degraded",
                default=0.9,
            )
        )
        self.meta.add(
            MetaDataField(
                name="criticalLimit",
                kind=MetaData.Type.FLOAT,
                description="Number of PSU that need to be down before the rack is critical",
                default=0.8,
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludePowerShelves",
                kind=MetaData.Type.RESOLVE,
                description="List of switches to exclude from the total",
                instance='PowerShelf',
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
        self.childType = 'MonitoringDataProducerAggregatePowerShelf'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerAggregatePowerShelf', 'MonitoringDataProducerInternal', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

