from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducer import MonitoringDataProducer


class MonitoringDataProducerJobQueue(MonitoringDataProducer):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="wlmClusters",
                kind=MetaData.Type.RESOLVE,
                description="List of wlm clusters for which to sample, empty for all",
                instance='WlmCluster',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerJobQueue'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerJobQueue', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

