from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class BeeGFSHelperConnectionSettings(Entity):
    """
    BeeGFS helper connection settings entry
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="portTCP",
                kind=MetaData.Type.UINT,
                description="TCP port for the service",
                default=8006,
            )
        )
        self.baseType = 'BeeGFSHelperConnectionSettings'
        self.service_type = self.baseType
        self.allTypes = ['BeeGFSHelperConnectionSettings']
        self.top_level = False
        self.leaf_entity = True

