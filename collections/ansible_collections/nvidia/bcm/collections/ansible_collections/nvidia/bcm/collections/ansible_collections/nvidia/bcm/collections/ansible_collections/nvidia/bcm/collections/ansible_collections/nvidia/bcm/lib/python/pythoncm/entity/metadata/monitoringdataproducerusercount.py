from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducerinternal import MonitoringDataProducerInternal


class MonitoringDataProducerUserCount(MonitoringDataProducerInternal):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="customScript",
                kind=MetaData.Type.STRING,
                description="Custom script",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="customScriptTimeout",
                kind=MetaData.Type.UINT,
                description="Custom script timeout",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="minimalUserId",
                kind=MetaData.Type.UINT,
                description="Minumal user ID",
                default=1000,
            )
        )
        self.meta.add(
            MetaDataField(
                name="namesInInfoMessage",
                kind=MetaData.Type.BOOL,
                description="Names in info message, could lead to lots of data",
                default=False,
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerUserCount'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerUserCount', 'MonitoringDataProducerInternal', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

