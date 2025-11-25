from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducer import MonitoringDataProducer


class MonitoringDataProducerDPU(MonitoringDataProducer):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="dpuSettings",
                kind=MetaData.Type.ENTITY,
                description="Submode containing DPU settings",
                instance='MonitoringDataProducerDPUSettings',
                create_instance=True,
                default=None,
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerDPU'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerDPU', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

