from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.device import Device


class Chassis(Device):
    """
    Chassis
    """
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
        self.meta.add(
            MetaDataField(
                name="layout",
                kind=MetaData.Type.STRING,
                description="Layout definition for rackview (Format: [|-]x,y   e.g: |8,3 or -2,6)",
                regex_check=r"^(|[-|]\d+,\d+)$",
                default='',
            )
        )
        self.baseType = 'Device'
        self.childType = 'Chassis'
        self.service_type = self.baseType
        self.allTypes = ['Chassis', 'Device']
        self.top_level = True
        self.leaf_entity = True

