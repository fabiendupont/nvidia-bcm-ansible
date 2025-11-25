from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ChassisPosition(Entity):
    """
    Chassis position
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="chassis",
                kind=MetaData.Type.RESOLVE,
                description="Name of the chassis in which the device resides",
                instance='Chassis',
                entity_allow_null=True,
                default=None,
            )
        )
        self.meta.add(
            MetaDataField(
                name="slot",
                kind=MetaData.Type.STRING,
                description="Slot of device inside the chassis",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="position",
                kind=MetaData.Type.UINT,
                description="Position of the device in the chassis",
                default=1,
            )
        )
        self.meta.add(
            MetaDataField(
                name="width",
                kind=MetaData.Type.UINT,
                description="Width of the device",
                default=1,
            )
        )
        self.baseType = 'ChassisPosition'
        self.service_type = self.baseType
        self.allTypes = ['ChassisPosition']
        self.top_level = False
        self.leaf_entity = True

