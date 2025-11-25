from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.statussubsysteminfo import StatusSubSystemInfo


class StatusRuleSubSystemInfo(StatusSubSystemInfo):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="rules",
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
                name="checks",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.baseType = 'SubSystemInfo'
        self.childType = 'StatusRuleSubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['StatusRuleSubSystemInfo', 'StatusSubSystemInfo', 'SubSystemInfo']
        self.top_level = False
        self.leaf_entity = True

