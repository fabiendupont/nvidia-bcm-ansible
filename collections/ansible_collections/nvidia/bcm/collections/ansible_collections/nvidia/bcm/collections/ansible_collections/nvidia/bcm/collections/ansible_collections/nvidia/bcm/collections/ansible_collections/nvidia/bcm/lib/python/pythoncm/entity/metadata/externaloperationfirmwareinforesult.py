from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.externaloperationresult import ExternalOperationResult


class ExternalOperationFirmwareInfoResult(ExternalOperationResult):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="firmwareInfo",
                kind=MetaData.Type.ENTITY,
                description="Firmware info",
                instance='FirmwareInfo',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'ExternalOperationResult'
        self.childType = 'ExternalOperationFirmwareInfoResult'
        self.service_type = self.baseType
        self.allTypes = ['ExternalOperationFirmwareInfoResult', 'ExternalOperationResult']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

