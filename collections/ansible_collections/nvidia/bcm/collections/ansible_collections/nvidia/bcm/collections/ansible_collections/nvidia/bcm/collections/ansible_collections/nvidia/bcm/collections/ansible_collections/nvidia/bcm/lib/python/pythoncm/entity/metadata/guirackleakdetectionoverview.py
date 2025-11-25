from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiRackLeakDetectionOverview(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_rack_uuid",
                kind=MetaData.Type.UUID,
                description="Rack",
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="leakDetect",
                kind=MetaData.Type.UINT,
                description="Leak detect",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="leakDetectTray",
                kind=MetaData.Type.UINT,
                description="Leak detect in tray",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="leakSensorFault",
                kind=MetaData.Type.UINT,
                description="Leak sensor fault",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="liquidIsolationStatus",
                kind=MetaData.Type.UINT,
                description="Liquid isolation status, 0 means none",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="liquidIsolationRequest",
                kind=MetaData.Type.UINT,
                description="Liquid isolation request, 0 means none",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="liquidIsolationRequestBCM",
                kind=MetaData.Type.UINT,
                description="Liquid isolation request as known by BCM, 0 means none",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="electricalIsolationStatus",
                kind=MetaData.Type.UINT,
                description="Electrical isolation status, 0 means none",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="electricalIsolationRequest",
                kind=MetaData.Type.UINT,
                description="Electrical isolation request, 0 means none",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="electricalIsolationRequestBCM",
                kind=MetaData.Type.UINT,
                description="Electrical isolation request as known by BCM, 0 means none",
                default=0,
            )
        )
        self.baseType = 'GuiRackLeakDetectionOverview'
        self.service_type = self.baseType
        self.allTypes = ['GuiRackLeakDetectionOverview']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

