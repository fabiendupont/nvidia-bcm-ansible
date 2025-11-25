from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringmeasurable import MonitoringMeasurable


class MonitoringMeasurableMetric(MonitoringMeasurable):
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
                name="integer",
                kind=MetaData.Type.BOOL,
                description="Only integers values will be reporter, interpolate accordingly",
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
        self.baseType = 'MonitoringMeasurable'
        self.childType = 'MonitoringMeasurableMetric'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringMeasurableMetric', 'MonitoringMeasurable']
        self.top_level = True
        self.leaf_entity = True

