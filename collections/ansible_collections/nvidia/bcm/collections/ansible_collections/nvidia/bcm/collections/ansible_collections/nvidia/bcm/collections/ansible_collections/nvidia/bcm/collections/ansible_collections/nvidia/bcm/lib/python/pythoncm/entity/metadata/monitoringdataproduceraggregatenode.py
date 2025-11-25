from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducerinternal import MonitoringDataProducerInternal


class MonitoringDataProducerAggregateNode(MonitoringDataProducerInternal):
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
                name="excludeNodes",
                kind=MetaData.Type.RESOLVE,
                description="List of nodes to exclude from the total",
                instance='Node',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeCategories",
                kind=MetaData.Type.RESOLVE,
                description="List of node groups to exclude from the total",
                instance='Category',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeNodeGroups",
                kind=MetaData.Type.RESOLVE,
                description="List of node groups to exclude from the total",
                instance='NodeGroup',
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
        self.childType = 'MonitoringDataProducerAggregateNode'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerAggregateNode', 'MonitoringDataProducerInternal', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

