from enum import Enum
from enum import auto

from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class FirewallZone(Entity):
    class ZoneType(Enum):
        ipv4 = auto()
        ipv6 = auto()

    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="zone",
                kind=MetaData.Type.STRING,
                description="Zone",
                default="loc",
            )
        )
        self.meta.add(
            MetaDataField(
                name="zone_type",
                kind=MetaData.Type.ENUM,
                description="Type",
                options=[
                    self.ZoneType.ipv4,
                    self.ZoneType.ipv6,
                ],
                diff_type=MetaDataField.Diff.enum,
                enum_type=self.ZoneType,
                default=self.ZoneType.ipv4,
            )
        )
        self.meta.add(
            MetaDataField(
                name="options",
                kind=MetaData.Type.STRING,
                description="Options",
                default="",
            )
        )
        self.baseType = 'FirewallZone'
        self.service_type = self.baseType
        self.allTypes = ['FirewallZone']
        self.top_level = False
        self.leaf_entity = True

