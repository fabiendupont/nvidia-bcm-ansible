from pythoncm.entity.meta_data import MetaData
from pythoncm.entity.meta_data_field import MetaDataField
from pythoncm.entity.metadata.entity import Entity


class LiteMonitoredEntity(Entity):
    """
    Lite monitored entity
    """
    def __init__(self):
        super().__init__()
        self.meta.add(
            MetaDataField(
                name="name",
                kind=MetaData.Type.STRING,
                default='',
            )
        )
        self.meta.add(
            MetaDataField(
                name="types",
                kind=MetaData.Type.STRING,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="resources",
                kind=MetaData.Type.STRING,
                vector=True,
                default=[],
            )
        )
        self.meta.add(
            MetaDataField(
                name="disabled",
                kind=MetaData.Type.BOOL,
                default=False,
            )
        )
        self.baseType = 'LiteMonitoredEntity'
        self.service_type = self.baseType
        self.allTypes = ['LiteMonitoredEntity']
        self.top_level = False
        self.leaf_entity = True
        self.allow_commit = False

