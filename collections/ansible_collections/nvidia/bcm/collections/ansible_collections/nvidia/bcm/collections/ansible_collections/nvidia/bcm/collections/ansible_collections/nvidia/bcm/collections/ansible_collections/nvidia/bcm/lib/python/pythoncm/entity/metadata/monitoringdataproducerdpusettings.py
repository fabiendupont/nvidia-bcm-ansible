from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class MonitoringDataProducerDPUSettings(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="enable_pcie0",
                kind=MetaData.Type.BOOL,
                description="Enable pcie0 metrics",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="enable_pcie1",
                kind=MetaData.Type.BOOL,
                description="Enable pcie0 metrics",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="enable_ecc",
                kind=MetaData.Type.BOOL,
                description="Enable ecc metrics",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="configured_events",
                kind=MetaData.Type.ENTITY,
                description="Configured of the event",
                instance='MonitoringDataProducerDPUSettingsEvent',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'MonitoringDataProducerDPUSettings'
        self.service_type = self.baseType
        self.allTypes = ['MonitoringDataProducerDPUSettings']
        self.top_level = False
        self.leaf_entity = True

