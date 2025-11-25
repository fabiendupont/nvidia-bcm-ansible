from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiPDUOverview(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_powerdistributionunit_uuid",
                kind=MetaData.Type.UUID,
                default=self.zero_uuid,
            )
        )
        self.meta.add(
            MetaDataField(
                name="model",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="outlets",
                kind=MetaData.Type.ENTITY,
                instance='GuiPDUOutlet',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="banks",
                kind=MetaData.Type.ENTITY,
                instance='GuiPDUBank',
                vector=True,
                default=[],
            )
        )
        self.baseType = 'GuiPDUOverview'
        self.service_type = self.baseType
        self.allTypes = ['GuiPDUOverview']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

