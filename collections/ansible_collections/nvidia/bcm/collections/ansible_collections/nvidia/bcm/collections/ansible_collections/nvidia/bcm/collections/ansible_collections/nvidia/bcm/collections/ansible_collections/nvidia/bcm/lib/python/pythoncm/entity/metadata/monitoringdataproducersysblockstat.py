from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.monitoringdataproducerinternal import MonitoringDataProducerInternal


class MonitoringDataProducerSysBlockStat(MonitoringDataProducerInternal):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="excludeVirtualDisks",
                kind=MetaData.Type.BOOL,
                description="Exclude virtual disks",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeDisks",
                kind=MetaData.Type.STRING,
                description="Exclude disks",
                vector=True,
                default=["/sr.*/", "/loop.*/", "/ram.*/", "cdrom", "/nvme\\d+c\\d+n\\d+/"],
            )
        )
        self.baseType = 'MonitoringDataProducer'
        self.childType = 'MonitoringDataProducerSysBlockStat'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerSysBlockStat', 'MonitoringDataProducerInternal', 'MonitoringDataProducer']
        self.top_level = True
        self.leaf_entity = True

