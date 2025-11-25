from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class GuiSwitchOverview(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ref_switch_uuid",
                kind=MetaData.Type.UUID,
                description="Switch",
                default=self.zero_uuid,
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
                name="serialNumber",
                kind=MetaData.Type.STRING,
                description="Serial number",
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
                name="ports",
                kind=MetaData.Type.ENTITY,
                description="Ports",
                instance='GuiSwitchPort',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="info",
                kind=MetaData.Type.JSON,
                description="Additional information",
                default=None,
            )
        )
        self.baseType = 'GuiSwitchOverview'
        self.service_type = self.baseType
        self.allTypes = ['GuiSwitchOverview']
        self.top_level = False
        self.leaf_entity = True
        self.add_to_cluster = False
        self.allow_commit = False

