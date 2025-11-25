from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class KubeAppGroup(Entity):
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
                name="applications",
                kind=MetaData.Type.ENTITY,
                description="Kubernetes applications managed by cmdaemon",
                instance='KubeApp',
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="enabled",
                kind=MetaData.Type.BOOL,
                description="Enable this application group",
                default=True,
            )
        )
        self.baseType = 'KubeAppGroup'
        self.service_type = self.baseType
        self.allTypes = ['KubeAppGroup']
        self.top_level = False
        self.leaf_entity = True
        self.resolve_field_name = 'name'

