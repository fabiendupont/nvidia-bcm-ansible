from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducer import MonitoringDataProducer


class MonitoringDataProducerTrustedTool(MonitoringDataProducer):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="port",
                kind=MetaData.Type.UINT,
                description="Port",
                default=18000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="localhost",
                kind=MetaData.Type.BOOL,
                description="Only listen on localhost",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="secret",
                kind=MetaData.Type.STRING,
                description="Secret",
                default='',
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerTrustedTool'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerTrustedTool', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

