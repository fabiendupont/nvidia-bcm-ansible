from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class ZTPNewSwitchSettings(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="ztpScriptTemplate",
                kind=MetaData.Type.STRING,
                description="ZTP script template for new switches",
                default="new-switch-ztp.sh",
            )
        )
        self.meta.add(
            MetaDataField(
                name="switchImage",
                kind=MetaData.Type.STRING,
                description="Image loaded via ONIE",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="keyValueSettings",
                kind=MetaData.Type.ENTITY,
                description="Key value settings which can be passed to the ZTP script",
                instance='KeyValueSettings',
                entity_allow_null=True,
                default=None,
            )
        )
        self.baseType = 'ZTPNewSwitchSettings'
        self.service_type = self.baseType
        self.allTypes = ['ZTPNewSwitchSettings']
        self.top_level = False
        self.leaf_entity = True

