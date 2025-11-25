from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class JupyterHubConfig(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="key",
                kind=MetaData.Type.STRING,
                description="Configuration key",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="value",
                kind=MetaData.Type.STRING,
                description="The value for the given configuration key, needs to be literal (include quotes for strings)",
                default='',
            )
        )
        self.baseType = 'JupyterHubConfig'
        self.service_type = self.baseType
        self.allTypes = ['JupyterHubConfig']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'key'

