from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiNetworkInterface(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Interface name",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="rx",
                kind=MetaData.Type.UINT,
                description="Number of bytes received since startup",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="tx",
                kind=MetaData.Type.UINT,
                description="Number of bytes transmitted since startup",
                default=0,
            )
        )
        self.baseType = 'GuiNetworkInterface'
        self.service_type = self.baseType
        self.allTypes = ['GuiNetworkInterface']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

