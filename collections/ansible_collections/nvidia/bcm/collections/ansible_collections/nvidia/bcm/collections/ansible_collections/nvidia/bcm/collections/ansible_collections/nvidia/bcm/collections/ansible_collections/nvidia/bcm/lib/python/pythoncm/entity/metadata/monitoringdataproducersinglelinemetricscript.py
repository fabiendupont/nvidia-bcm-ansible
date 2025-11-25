from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducersinglelinescript import MonitoringDataProducerSingleLineScript


class MonitoringDataProducerSingleLineMetricScript(MonitoringDataProducerSingleLineScript):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="minimum",
                kind=MetaData.Type.FLOAT,
                description="Minimum",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maximum",
                kind=MetaData.Type.FLOAT,
                description="Maximum",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cumulative",
                kind=MetaData.Type.BOOL,
                description="Cumulative",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="unit",
                kind=MetaData.Type.STRING,
                description="Unit",
                default='',
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerSingleLineMetricScript'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerSingleLineMetricScript', 'MonitoringDataProducerSingleLineScript', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

