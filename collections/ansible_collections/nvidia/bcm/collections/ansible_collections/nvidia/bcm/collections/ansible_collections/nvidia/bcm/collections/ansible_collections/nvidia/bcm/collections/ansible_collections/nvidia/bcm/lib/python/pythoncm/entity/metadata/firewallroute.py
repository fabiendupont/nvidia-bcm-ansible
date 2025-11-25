from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class FirewallRoute(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="provider",
                kind=MetaData.Type.STRING,
                description="Provider",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="destination",
                kind=MetaData.Type.STRING,
                description="Destination",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="gateway",
                kind=MetaData.Type.STRING,
                description="Gateway",
                default="",
            )
        )
        self.meta.add(
            MetaDataField(
                name="device",
                kind=MetaData.Type.STRING,
                description="Device",
                default="",
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
        self.baseType = 'FirewallRoute'
        self.service_type = self.baseType
        self.allTypes = ['FirewallRoute']
        self.top_level = False
        self.leaf_entity = True

