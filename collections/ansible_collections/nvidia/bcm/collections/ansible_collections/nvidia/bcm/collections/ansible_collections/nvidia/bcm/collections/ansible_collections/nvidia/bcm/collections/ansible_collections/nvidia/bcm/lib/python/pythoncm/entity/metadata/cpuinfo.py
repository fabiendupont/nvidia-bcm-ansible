from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class CPUInfo(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="physicalID",
                kind=MetaData.Type.UINT,
                description="Physical ID",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="vendor",
                kind=MetaData.Type.STRING,
                description="Vendor",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="model",
                kind=MetaData.Type.STRING,
                description="Model",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="cores",
                kind=MetaData.Type.UINT,
                description="Cores",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="speed",
                kind=MetaData.Type.FLOAT,
                description="Speed",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="cacheSize",
                kind=MetaData.Type.UINT,
                description="Cache size",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="bogomips",
                kind=MetaData.Type.FLOAT,
                description="Bogomips",
                default=0.0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="powerCapEnabled",
                kind=MetaData.Type.BOOL,
                description="Power cap enabled",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="minPowerLimit",
                kind=MetaData.Type.UINT,
                description="Minimal power limit",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="maxPowerLimit",
                kind=MetaData.Type.UINT,
                description="Maximal power limit",
                default=0,
            )
        )
        self.baseType = 'CPUInfo'
        self.service_type = self.baseType
        self.allTypes = ['CPUInfo']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

