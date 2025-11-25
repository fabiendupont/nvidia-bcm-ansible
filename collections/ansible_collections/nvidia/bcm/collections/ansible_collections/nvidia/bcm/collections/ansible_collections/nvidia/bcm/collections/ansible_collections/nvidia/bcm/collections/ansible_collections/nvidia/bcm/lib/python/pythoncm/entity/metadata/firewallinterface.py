from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class FirewallInterface(Entity):
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
                name="interface",
                kind=MetaData.Type.STRING,
                description="Interface",
                default="eth1",
            )
        )
        self.meta.add(
            MetaDataField(
                name="broadcast",
                kind=MetaData.Type.STRING,
                description="Broadcast",
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
        self.baseType = 'FirewallInterface'
        self.service_type = self.baseType
        self.allTypes = ['FirewallInterface']
        self.top_level = False
        self.leaf_entity = True

