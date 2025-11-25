from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.subsysteminfo import SubSystemInfo


class StatusSubSystemInfo(SubSystemInfo):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="stopped",
                kind=MetaData.Type.BOOL,
                description="Stopped",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="suspended",
                kind=MetaData.Type.BOOL,
                description="Suspended",
                default=False,
            )
        )
        self.baseType = 'SubSystemInfo'
        self.childType = 'StatusSubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['StatusSubSystemInfo', 'SubSystemInfo']
        self.leaf_entity = False

