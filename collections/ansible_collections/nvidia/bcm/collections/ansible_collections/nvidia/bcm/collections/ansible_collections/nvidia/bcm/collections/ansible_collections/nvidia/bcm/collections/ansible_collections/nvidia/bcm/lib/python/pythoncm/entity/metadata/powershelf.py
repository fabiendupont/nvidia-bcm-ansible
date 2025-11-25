from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.device import Device


class PowerShelf(Device):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="model",
                kind=MetaData.Type.STRING,
                description="Device model name",
                default='',
            )
        )
        self.baseType = 'Device'
        self.childType = 'PowerShelf'
        self.service_type = self.baseType
        self.allTypes = ['PowerShelf', 'Device']
        self.top_level = True
        self.leaf_entity = True

