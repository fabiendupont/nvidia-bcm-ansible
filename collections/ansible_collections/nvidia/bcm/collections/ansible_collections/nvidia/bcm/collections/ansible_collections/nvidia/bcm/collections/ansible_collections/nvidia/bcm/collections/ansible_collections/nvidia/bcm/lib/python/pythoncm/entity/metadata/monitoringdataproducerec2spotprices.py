from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducerinternal import MonitoringDataProducerInternal


class MonitoringDataProducerEC2SpotPrices(MonitoringDataProducerInternal):
    class Select(Enum):
        AUTOMATIC = auto()
        ALL = auto()
        CUSTOM = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="regions",
                kind=MetaData.Type.ENUM,
                description="Regions to collect data for",
                options=[
                    self.Select.AUTOMATIC,
                    self.Select.ALL,
                    self.Select.CUSTOM,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Select,
                default=self.Select.AUTOMATIC,
            )
        )
        self.meta.add(
            MetaDataField(
                name="customRegions",
                kind=MetaData.Type.RESOLVE,
                description="Custom list of regions to collect data from",
                instance='EC2Region',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="types",
                kind=MetaData.Type.ENUM,
                description="Types to collect data for",
                options=[
                    self.Select.AUTOMATIC,
                    self.Select.ALL,
                    self.Select.CUSTOM,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Select,
                default=self.Select.AUTOMATIC,
            )
        )
        self.meta.add(
            MetaDataField(
                name="customTypes",
                kind=MetaData.Type.RESOLVE,
                description="Custom list of types to collect data from",
                instance='EC2Type',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerEC2SpotPrices'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerEC2SpotPrices', 'MonitoringDataProducerInternal', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

