from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.statussubsysteminfo import StatusSubSystemInfo


class StatusTransitionSubSystemInfo(StatusSubSystemInfo):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="handled",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="transitions",
                kind=MetaData.Type.INT,
                description="Transition matrics: from -> to",
                vector=True,
                default=[],
            )
        )
        self.baseType = 'SubSystemInfo'
        self.childType = 'StatusTransitionSubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['StatusTransitionSubSystemInfo', 'StatusSubSystemInfo', 'SubSystemInfo']
        self.top_level = False
        self.leaf_entity = True

