from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiPDUBank(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="bank",
                kind=MetaData.Type.UINT,
                description="Bank",
                default=0,
            )
        )
        self.meta.add(
            MetaDataField(
                name="load",
                kind=MetaData.Type.FLOAT,
                description="Load",
                default=0.0,
            )
        )
        self.baseType = 'GuiPDUBank'
        self.service_type = self.baseType
        self.allTypes = ['GuiPDUBank']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

