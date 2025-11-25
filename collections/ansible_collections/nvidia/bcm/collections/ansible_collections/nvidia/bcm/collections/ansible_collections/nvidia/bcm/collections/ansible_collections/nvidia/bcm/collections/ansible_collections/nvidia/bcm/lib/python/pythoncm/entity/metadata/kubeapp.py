from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class KubeApp(Entity):
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                description="Object name",
                required=True,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="format",
                kind=MetaData.Type.STRING,
                description="Configuration format",
                options=[
                    'Yaml',
                    'Json',
                    'Other',
                ],
                default="Yaml",
            )
        )
        self.meta.add(
            MetaDataField(
                name="enabled",
                kind=MetaData.Type.BOOL,
                description="Enable this application",
                default=True,
            )
        )
        self.meta.add(
            MetaDataField(
                name="config",
                kind=MetaData.Type.STRING,
                description="Yaml or json configuration for the object",
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="extraEnvironment",
                kind=MetaData.Type.ENTITY,
                description="Additional variables for kubernetes apps or kubernetes nodes environment",
                instance='KubeAppEnvironment',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="excludeListSnippets",
                kind=MetaData.Type.ENTITY,
                instance='ExcludeListSnippet',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="state",
                kind=MetaData.Type.INT,
                description="",
                default=0,
            )
        )
        self.baseType = 'KubeApp'
        self.service_type = self.baseType
        self.allTypes = ['KubeApp']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

