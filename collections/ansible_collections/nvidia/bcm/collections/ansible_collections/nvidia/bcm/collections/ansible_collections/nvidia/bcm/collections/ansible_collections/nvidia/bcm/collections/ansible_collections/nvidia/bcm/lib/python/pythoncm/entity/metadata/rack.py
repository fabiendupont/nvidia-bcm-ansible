from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Rack(Entity):
    """
    Rack
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="location",
                kind=MetaData.Type.STRING,
                description="Location",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="building",
                kind=MetaData.Type.STRING,
                description="Building",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="room",
                kind=MetaData.Type.STRING,
                description="Room",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="row",
                kind=MetaData.Type.STRING,
                description="Row",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="partNumber",
                kind=MetaData.Type.STRING,
                description="Part number",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="serialNumber",
                kind=MetaData.Type.STRING,
                description="Serial number",
                clone=False,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="model",
                kind=MetaData.Type.STRING,
                description="Model",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="type",
                kind=MetaData.Type.STRING,
                description="Type",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="xCoordinate",
                kind=MetaData.Type.UINT,
                description="Position in the room",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="yCoordinate",
                kind=MetaData.Type.UINT,
                description="Position in the room",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="height",
                kind=MetaData.Type.UINT,
                description="Height",
                default=42,
            )
        )
        self.meta.add(
            MetaDataField(
                name="width",
                kind=MetaData.Type.UINT,
                description="Width",
                default=19,
            )
        )
        self.meta.add(
            MetaDataField(
                name="depth",
                kind=MetaData.Type.UINT,
                description="Depth",
                default=34,
            )
        )
        self.meta.add(
            MetaDataField(
                name="angle",
                kind=MetaData.Type.UINT,
                description="Angle of the rack, 90 face right, 180 face backwards, 270 face left",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="inverted",
                kind=MetaData.Type.BOOL,
                description="Inverted racks have position 1 at the bottom",
                default=False,
            )
        )
        self.meta.add(
            MetaDataField(
                name="notes",
                kind=MetaData.Type.STRING,
                description="Administrator notes",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="twin",
                kind=MetaData.Type.RESOLVE,
                description="Rack twin that makes up the NV link domain",
                clone=False,
                instance='Rack',
                entity_allow_null=True,
                default=None,
            )
        )
        self.baseType = 'Rack'
        self.service_type = self.baseType
        self.allTypes = ['Rack']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

