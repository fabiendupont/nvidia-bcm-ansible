from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class RackPosition(Entity):
    """
    Rack position
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="rack",
                kind=MetaData.Type.RESOLVE,
                description="Name of the rack in which the device resides",
                instance='Rack',
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="position",
                kind=MetaData.Type.UINT,
                description="Position of the device in the rack, top is 1",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="height",
                kind=MetaData.Type.UINT,
                description="Height of the device",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="trayId",
                kind=MetaData.Type.STRING,
                description="ID",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="trayName",
                kind=MetaData.Type.STRING,
                description="ID",
                default='',
            )
        )
        self.baseType = 'RackPosition'
        self.service_type = self.baseType
        self.allTypes = ['RackPosition']
        self.top_level = False
        self.leaf_entity = True

