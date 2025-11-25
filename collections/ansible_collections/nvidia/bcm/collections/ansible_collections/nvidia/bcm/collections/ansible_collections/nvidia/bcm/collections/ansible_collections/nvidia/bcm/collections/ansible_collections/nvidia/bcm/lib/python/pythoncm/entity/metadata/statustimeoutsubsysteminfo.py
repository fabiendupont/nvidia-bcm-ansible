from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.statussubsysteminfo import StatusSubSystemInfo


class StatusTimeoutSubSystemInfo(StatusSubSystemInfo):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="active",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="registered",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="handled",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.baseType = 'SubSystemInfo'
        self.childType = 'StatusTimeoutSubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['StatusTimeoutSubSystemInfo', 'StatusSubSystemInfo', 'SubSystemInfo']
        self.top_level = False
        self.leaf_entity = True

