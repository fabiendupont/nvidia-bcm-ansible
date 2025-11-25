from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.subsysteminfo import SubSystemInfo


class MonitoringSubSystemInfo(SubSystemInfo):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="storage",
                kind=MetaData.Type.ENTITY,
                description="Storage",
                instance='MonitoringStorageSubSystemInfo',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="service",
                kind=MetaData.Type.ENTITY,
                description="Service",
                instance='MonitoringServiceSubSystemInfo',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="plotter",
                kind=MetaData.Type.ENTITY,
                description="Plotter",
                instance='MonitoringPlotterSubSystemInfo',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="dataCache",
                kind=MetaData.Type.ENTITY,
                description="DataCache",
                instance='MonitoringDataCacheSubSystemInfo',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="labeledEntityCache",
                kind=MetaData.Type.ENTITY,
                description="LabeledEntityCache",
                instance='MonitoringLabeledEntityCacheSubSystemInfo',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="jobExtraLabelCache",
                kind=MetaData.Type.ENTITY,
                description="JobExtraLabelCache",
                instance='MonitoringJobExtraLabelCacheSubSystemInfo',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="cache",
                kind=MetaData.Type.ENTITY,
                description="Cache",
                instance='MonitoringCacheSubSystemInfo',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="deviceState",
                kind=MetaData.Type.ENTITY,
                description="DeviceState",
                instance='MonitoringDeviceStateSubSystemInfo',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'SubSystemInfo'
        self.childType = 'MonitoringSubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringSubSystemInfo', 'SubSystemInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

