from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class Sensor(Entity):
    class Type(Enum):
        TEMPERATURE = auto()
        TEMPERATURE_AND_HUMIDITY = auto()
        PRESSURE = auto()
        UNKNOWN = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="type",
                kind=MetaData.Type.ENUM,
                description="Sensor type",
                options=[
                    self.Type.TEMPERATURE,
                    self.Type.TEMPERATURE_AND_HUMIDITY,
                    self.Type.PRESSURE,
                    self.Type.UNKNOWN,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.Type,
                default=self.Type.UNKNOWN,
            )
        )
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Sensor name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="port",
                kind=MetaData.Type.UINT,
                description="Sensor port",
                default=0,
            )
        )
        self.baseType = 'Sensor'
        self.service_type = self.baseType
        self.allTypes = ['Sensor']
        self.top_level = False
        self.leaf_entity = True

