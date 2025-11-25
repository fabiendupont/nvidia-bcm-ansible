from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.device import Device


class LiteNode(Device):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="services",
                kind=MetaData.Type.ENTITY,
                description="Manage operating system services",
                instance='OSServiceConfig',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'Device'
        self.childType = 'LiteNode'
        self.service_type = self.baseType
        self.allTypes = ['LiteNode', 'Device']
        self.top_level = True
        self.leaf_entity = True

