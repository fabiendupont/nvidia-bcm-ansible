from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.statussubsysteminfo import StatusSubSystemInfo


class StatusControllerSubSystemInfo(StatusSubSystemInfo):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="updates",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="reports",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="nodes",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="icmpPingCount",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="checkUrlCount",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="customScriptCount",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="customFunctionCount",
                kind=MetaData.Type.UINT,
                default=0,
            )
        )
        self.baseType = 'SubSystemInfo'
        self.childType = 'StatusControllerSubSystemInfo'
        self.service_type = self.baseType
        self.allTypes = ['StatusControllerSubSystemInfo', 'StatusSubSystemInfo', 'SubSystemInfo']
        self.top_level = False
        self.leaf_entity = True

