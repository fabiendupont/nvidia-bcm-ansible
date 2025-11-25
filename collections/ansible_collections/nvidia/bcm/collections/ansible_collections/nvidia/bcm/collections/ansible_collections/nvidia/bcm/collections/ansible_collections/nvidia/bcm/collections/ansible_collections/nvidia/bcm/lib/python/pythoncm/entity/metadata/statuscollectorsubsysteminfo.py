from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.statussubsysteminfo import StatusSubSystemInfo


class StatusCollectorSubSystemInfo(StatusSubSystemInfo):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="updates",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="merges",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.baseType = 'SubSystemInfo'
        self.childType = 'StatusCollectorSubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['StatusCollectorSubSystemInfo', 'StatusSubSystemInfo', 'SubSystemInfo']
        self.top_level = False
        self.leaf_entity = True

