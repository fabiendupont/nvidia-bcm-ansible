from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class PowerCircuit(Entity):
    """
    Power circuit
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
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="serialNumber",
                kind=MetaData.Type.STRING,
                description="Serial number",
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
                name="racks",
                kind=MetaData.Type.RESOLVE,
                description="List of racks powered by this unit",
                instance='Rack',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'PowerCircuit'
        self.service_type = self.baseType
        self.allTypes = ['PowerCircuit']
        self.top_level = True
        self.leaf_entity = True
        self.resolve_field_name = 'name'

